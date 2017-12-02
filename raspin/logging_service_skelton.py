
# ./mjpg_streamer -i "./input_uvc.so -f 2 -r 320x240 -d /dev/video0 -y" -o "./output_http.so -w ./www -p 8080"
import time
import raspin
from datetime import datetime
from multiprocessing import Process
QUEUE_SIZE = 15

def timestp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log(str):
    print("{stp} {str}".format(stp=timestp(), str=str))


class logging_service_skelton:

    def __init__(self):
        self.pvid = ""
        self.p = None
        self.api = raspin.api("localhost",3000)

    def initialize(self, pvname, data_type, unit = "-"):
        self.pvname = pvname
        self.data_type = data_type

        #self.json_stopping = {"pvname": pvname, "queue_size": QUEUE_SIZE,"layout_param":"default-controller@command console",
        #                 "available_message": [{"message_name": "on", "arg": 1},
        #                                       {"message_name": "end".format(pvname=pvname),
        #                                        "arg": 1}]}

        #self.json_running = {"pvname": pvname, "queue_size": QUEUE_SIZE,"layout_param":"default-controller@command console",
        #                "available_message": [{"message_name": "off", "arg": 1},
        #                                      {"message_name": "end".format(pvname=pvname),
        #                                       "arg": 1}]}
        self.json_stopping = {"pvname": pvname, "queue_size": QUEUE_SIZE,
                              "layout_param": "default-controller@command console",
                              "available_message": [{"message_name": "on", "arg": 1}]}

        self.json_running = {"pvname": pvname, "queue_size": QUEUE_SIZE,
                             "layout_param": "default-controller@command console",
                             "available_message": [{"message_name": "off", "arg": 1}]}

        self.data_pv_json = {"pvname": "{pvname}".format(pvname = pvname),"layout_param":"default-data@basic data", "queue_size": QUEUE_SIZE, "type": data_type, "unit": unit}


    def retrieve_value(self):
        raise Exception ("not implemented")

    def subprocess_function(self, data_pvid):
        while True:
            val = self.retrieve_value()
            print(val)
            self.api.add_observation_data(data_pvid, val)
            time.sleep(1)
            self.api.ping()



    def launch_process(self, data_pvid):

        self.p = Process(target=self.subprocess_function, args=[data_pvid])
        self.p.start()

    def __stop_process(self):
        self.p.terminate()
        self.p = None



    def main_process(self):

        self.pvid = self.api.register_controller_provider(
            self.json_stopping["pvname"],
            self.json_stopping["queue_size"],
            self.json_stopping["available_message"],
            self.json_stopping["layout_param"])["pvid"]
        last_req_id = ""
        data_pv_id = ""
        while True:
            mess = self.api.subscribe_control_message(self.pvid, 100)
            log("docs------")
            log(mess)
            if mess["ret"] == "to":
                log("timeout")
                continue
            if mess["message"] == "end_{pvname}_service".format(pvname=self.pvname):
                self.api.acknowledge(self.pvid, mess['req_id'], "1", [], [self.pvid,data_pv_id ])

                break
            else:
                log("pvid:{pv},req_id:{req}".format(req=mess['req_id'], pv=self.pvid))
                if self.p is None:
                    data_pv_id = self.api.register_data_provider(self.data_pv_json["pvname"], self.data_pv_json["queue_size"], self.data_pv_json["type"], self.data_pv_json["unit"], self.data_pv_json["layout_param"])["pvid"]
                    self.launch_process(data_pv_id)
                    self.api.mod_controller_provider(self.pvid,
                                                     self.json_running["pvname"],
                                                     self.json_running["queue_size"],
                                                     self.json_running["available_message"],
                                                     self.json_running["layout_param"]
                                                     )
                    self.api.acknowledge(self.pvid, mess['req_id'], "1", [self.pvid,data_pv_id ], [])

                else:
                    self.api.delete_provider(data_pv_id)
                    self.__stop_process()
                    self.api.mod_controller_provider(self.pvid,
                                                     self.json_stopping["pvname"],
                                                     self.json_stopping["queue_size"],
                                                     self.json_stopping["available_message"],
                                                     self.json_stopping["layout_param"]
                                                     )
                    self.api.acknowledge(self.pvid, mess['req_id'], "1",  [self.pvid],[data_pv_id])
                    data_pv_id = ""

        if data_pv_id <> "":
            self.__stop_process()
            self.api.delete_provider(data_pv_id)
        self.api.delete_provider(self.pvid)


