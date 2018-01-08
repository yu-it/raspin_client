# -*- coding: utf-8 -*-
import platform



def log(str):
    print(str)

# ピンの名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

#i2cバスオブジェクト
bus = None

#i2cリトライ
I2CRETRY = 5


if platform.system() == "Windows":
    do_drive = False
    print("run as emu")
else:
    do_drive = True

    print("run actually")
    import RPi.GPIO as GPIO
    import smbus

    bus = smbus.SMBus(1)
    GPIO.setmode(GPIO.BCM)
    # SPI通信用の入出力を定義
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICS, GPIO.OUT)

    import wiringpi as wiringpi
    wiringpi.wiringPiSetupGpio() # GPIO名で番号を指定する
    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT) # PWM出力を指定
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS) # 周波数を固定するための設定
    wiringpi.pwmSetClock(375) # 50 Hz。ここには 18750/(周波数) の計算値に近い整数を入れる


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3  # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout



def i2c_write(address,  data, offset = 0x00):

    success = False
    for x in xrange(I2CRETRY):
        try:
            log("to {addr}, comm:{c0}, data[0]:{d0}, data[1]:{d1}, ".format(addr=address, c0=data[0], d0=data[1],
                                                                            d1=data[2]))
            if do_drive:

                bus.write_i2c_block_data(address, offset, data)
        except:
            log("retry...")
            continue
        success = True
        break
    if not success:
        raise Exception("I2C Error")



def read_analog(ch):
    return readadc(ch, SPICLK, SPIMOSI, SPIMISO, SPICS)

def read_analog_volt(ch, rate = 1):
    return read_analog(ch) * (3.3/4096.0) * rate

def clear():
    if do_drive:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
    else:
        log("cleanup")

