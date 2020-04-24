import sys
import time
from ant.core import driver, node, event, message, log
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER
#candence_cnt = 0
#candence_time = 0
#candence_cnt_old = -1
#candence_time_old = -1


class SpeedSensorRx(event.EventCallback):

    def __init__(self, antnode, sensor_type):
        self.antnode = antnode
        self.sensor_type = sensor_type
        #self.netkey = netkey
        self.channel = None
        self.speed_cnt = 0
        self.speed_time = 0
        self.speed_cnt_old = -1
        self.speed_time_old = -1
        self.speed = 0
        self.stop_cnt1 = 0
        self.stop_speed_pre = 0
        self.wheel_circumference = 2.07
        self.revs_per_sec = 0.0
        self.kms_per_rev = 0.0

    def start(self):
        print("starting node")
        self._setup_channel()
        self.channel.registerCallback(self)
        print("start listening for speed events")

    def stop(self):
        if self.channel:
            self.channel.close()
            self.channel.unassign()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

    def _setup_channel(self):
        self.channel = self.antnode.getFreeChannel()
        self.channel.name = 'C:SPEED'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(self.sensor_type, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8118)
        self.channel.setFrequency(57)
        self.channel.open()

    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):

            #self.speed_cnt = int(ord(msg.payload[-2])+256*ord(msg.payload[-1]))
            self.speed_cnt = int(ord(msg.payload[7])+256*ord(msg.payload[8]))
            # print self.speed_cnt
            #self.speed_time = int(ord(msg.payload[-4])+256*ord(msg.payload[-3]))
            self.speed_time = int(ord(msg.payload[5])+256*ord(msg.payload[6]))
            # print self.speed_time
            if self.speed_cnt_old == -1:
                self.speed_cnt_old = self.speed_cnt
                self.speed_time_old = self.speed_time
                return
            if self.speed_cnt < self.speed_cnt_old:
                self.speed_cnt += 65536
            if self.speed_time < self.speed_time_old:
                self.speed_time += 65536
                # self.speed=(self.speed_cnt-self.speed_cnt_old)*1024*60.0/(self.speed_time-self.speed_time_old)
#diametro ruota

            self.speed = self.wheel_circumference*3.6 * (self.speed_cnt-self.speed_cnt_old) * 1024/(self.speed_time-self.speed_time_old)
            # print "speed="+str(self.speed)
            if self.speed_cnt > 65536:
                self.speed_cnt -= 65536
            if self.speed_time > 65536:
                self.speed_time -= 65536
            self.speed_cnt_old = self.speed_cnt
            self.speed_time_old = self.speed_time

    def getSpeed(self):

        if self.stop_cnt1 == 0:
            self.stop_speed_pre = self.speed
            #print 'come to zero'
        self.stop_cnt1 = self.stop_cnt1+1
        if self.stop_cnt1 == 2:
            if abs(self.speed-self.stop_speed_pre) < 0.00001:
                self.speed = 0
                #print 'speed stop!'
            self.stop_cnt1 = 0

        return float(self.speed)
