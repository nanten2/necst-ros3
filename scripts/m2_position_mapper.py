#!/usr/bin/env python3

name = "m2_position_mapper"

import math
import time
import struct
import threading
import rospy
import std_msgs.msg


class m2_position_mapper(object):

    def __init__(self):
        self.array = std_msgs.msg.ByteMultiArray()

        self.do1 = rospy.Publisher(
                name = "/necopt/cpz2724_rsw1/do01_08",
                data_class = std_msgs.msg.ByteMultiArray,
                queue_size = 1,
            )

        self.do2 = rospy.Publisher(
                name = "/necopt/cpz2724_rsw1/do09_16",
                data_class = std_msgs.msg.ByteMultiArray,
                queue_size = 1,
            )

        topic_from = rospy.Subscriber(
                name = "pulse",
                data_class = std_msgs.msg.Int64,
                callback = self.callback,
                queue_size = 1,
            )
        
        time.sleep(5) # wait board ready
        self.InitIndexFF()
        pass

    def callback(self, req):
        self.puls = req.data
        return

    def pub_function(self):
        puls_last = None
        while not rospy.is_shutdonw():
            if self.puls != puls_last:
                if self.puls >= -65535 and self.puls <= 65535:
                    #index mode
                    self.array.data = [0,0,0,1,0,0,0,0]
                    self.do1.publish(self.array)
                    Strobe()
                    #step no.
                    self.array.data = [1,1,1,1,1,1,1,1]
                    self.do1.publish(self.array)
                    Strobe()
                    #position set
                    self.array.data = [0,0,0,0,0,0,1,1]
                    self.do1.publish(self.array)
                    Strobe()
                    #direction
                    if puls >= 0:
                        self.array.data = [0,0,0,0,1,0,0,0] #CW
                        self.do1.publish(self.array)
                        Strobe()
                    else:
                        self.array.data = [1,0,0,0,1,0,0,0] #CCW
                        self.do1.publish(self.array)
                        Strobe()
                    #displacement
                    self.array.data = [0,0,0,0,0,0,0,0]
                    self.do1.publish(self.array)
                    Strobe()
                    pls = struct.pack("<I", int(abs(self.puls)/256))
                    self.array.data = list(map(int, "".join([format(b, "08b")[::-1] for b in pls])))[:8]
                    self.do1.publish(self.array)
                    Strobe()
                    pls = struct.pack("<I", int(abs(self.puls)%256))
                    self.array.data = list(map(int, "".join([format(b, "08b")[::-1] for b in pls])))[:8]
                    self.do1.publish(self.array)
                    Strobe()
                    #start
                    self.array.data = [0,0,0,1,1,0,0,0]
                    self.do1.publish(self.array)
                    Strobe()
                    time.sleep((abs(self.puls) / 200 / 10.) + 1.)
                else:
                    pass
                puls_last = self.puls

            else: pass

            time.sleep(0.01)
            continue
        return

    def Strobe(self):
        time.sleep(0.01)
        self.array.data = [1,0,0,0,0,0,0,0]
        self.do2.publish(self.array)
        time.sleep(0.01)
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do2.publish(self.array)
        time.sleep(0.01)
        return

    def StrobeHOff(self):
        time.sleep(0.01)
        self.array.data = [1,0,1,0,0,0,0,0]
        self.do2.publish(self.array)
        time.sleep(0.01)
        self.array.data = [0,0,1,0,0,0,0,0]
        self.do2.publish(self.array)
        time.sleep(0.01)
        return

    def InitIndexFF(self):
        #initialization?
        self.array.data = [0,0,0,1,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #step no.
        self.array.data = [1,1,1,1,1,1,1,1]
        self.do1.publish(self.array)
        StrobeHOff()
        #vs set
        self.array.data = [0,1,0,0,1,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #5(*10=50)
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        self.array.data = [1,0,1,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #vr set
        self.array.data = [0,0,0,0,0,0,1,0]
        self.do1.publish(self.array)
        StrobeHOff()
        
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        self.array.data = [0,0,0,1,0,0,1,1] # MOTOR_SPEED=200
        self.do1.publish(self.array)
        StrobeHOff()
        #su-sd set
        self.array.data = [0,0,0,0,1,0,1,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #100(/10=10)
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        dio.output_byte("OUT1_8", [0,0,0,0,0,0,0,0])
        StrobeHOff()
        self.array.data = [0,0,1,0,0,1,1,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #position set
        self.array.data = [0,0,0,0,0,0,1,1]
        self.do1.publish(self.array)
        StrobeHOff()
        #cw
        self.array.data = [0,0,0,0,1,0,0,0] #CW=0x10
        self.do1.publish(self.array)
        StrobeHOff()
        #0
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        self.array.data = [0,0,0,0,0,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        #start
        self.array.data = [0,0,0,1,1,0,0,0]
        self.do1.publish(self.array)
        StrobeHOff()
        return


if __name__ == "__main__":
    rospy.init_node(name)
    mapper = m2_position_mapper()

    pub_thread = threading.Thread(
            target = mapper.pub_function,
            daemon = True,
            )
    pub_thread.start()
    rospy.spin()

