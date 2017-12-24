# -*- coding: utf-8 -*-
import random
for x in range(10):
    x = random.randrange(1,9)
    y = random.randrange(1,9)
    answer = raw_input("{x} × {y}は?".format(x=x,y=y))
    if (answer <> str(x*y)):
        print"はずれ！"
    else:
        print "あたり！"


