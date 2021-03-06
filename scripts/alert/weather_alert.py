#!/usr/bin/env python3

name = 'weather_alert'

# ----
import time

import rospy
import std_msgs.msg

WARN = "\033[31m"
END = "\033[0m\n"

class weather_alert(object):

    def __init__(self):

        sub_rain = rospy.Subscriber(
                name = "/weather/rain",
                data_class = std_msgs.msg.Float32,
                callback = self.callback_rain,
                queue_size = 1,
            )

        sub_humi = rospy.Subscriber(
                name = "/weather/outside2_humi",
                data_class = std_msgs.msg.Float32,
                callback = self.callback_humi,
                queue_size = 1,
            )

        sub_wind = rospy.Subscriber(
                name = "/weather/wind_speed",
                data_class = std_msgs.msg.Float32,
                callback = self.callback_wind,
                queue_size = 1,
            )

        pass

    def callback_rain(self, req):
        if req.data > 1.:
            print("[WEATHER] : probably raining \n")
        else: pass
        return

    def callback_humi(self,req):
        if 60 < req.data <=80:
            print("[WEATHER] : out_humi over 60 % \n")
        elif req.data > 80:
            print(WARN + "[WEATHER] : out_humi over 80 % " + END)
        else: pass
        return

    def callback_wind(self, req):
        if 10 < req.data < 15:
            print("[WEATHER] : wind_speed over 10 \n")
        elif 15 <= req.data:
            print(WARN + "[WEATHER] : wind_speed over 15 " + END)
        else: pass
        return


if __name__ == "__main__":
    rospy.init_node(name)
    alert = weather_alert()
    rospy.spin()


