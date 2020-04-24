from ant.core import driver, node, event, message, log
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER
#candence_cnt = 0
#candence_time = 0
#candence_cnt_old = -1
#candence_time_old = -1


class CadenceSensorRx(event.EventCallback):

    def __init__(self, antnode, sensor_type):
        self.antnode = antnode
        self.sensor_type = sensor_type
        self.channel = None
        self.cadence_cnt = 0
        self.cadence_time = 0
        self.cadence_cnt_old = -1
        self.cadence_time_old = -1
        self.cadence = 0
        self.stop_cnt1 = 0
        self.stop_cadence_pre = 0

    def start(self):
        print("starting node")
        self._setup_channel()
        self.channel.registerCallback(self)
        print("start listening for cadence events")

    def stop(self):
        if self.channel:
            self.channel.close()
            self.channel.unassign()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

    def _start_antnode(self):
        stick = driver.USB2Driver(self.serial)
        self.antnode = node.Node(stick)
        self.antnode.start()

    def _setup_channel(self):
        self.channel = self.antnode.getFreeChannel()
        self.channel.name = 'C:CADENCE'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(self.sensor_type, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8102)
        self.channel.setFrequency(57)
        self.channel.open()

    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            #print("heart rate is {}".format(ord(msg.payload[-2])))
            # print ord(msg.payload[2])A
            # print ord(msg.payload[3])
            self.cadence_cnt = int(ord(msg.payload[7]))+256*ord(msg.payload[8])
            # print '==========='
            # print self.cadence_cnt
            self.cadence_time = ord(msg.payload[5])+256*ord(msg.payload[6])
            # print self.cadence_time/1024.0
            if self.cadence_cnt == self.cadence_cnt_old:
                return
            if self.cadence_time == self.cadence_time_old:
                return
            if self.cadence_cnt_old == -1:
                self.cadence_cnt_old = self.cadence_cnt
                self.cadence_time_old = self.cadence_time
                return
            if self.cadence_cnt < self.cadence_cnt_old:
                self.cadence_cnt += 65536
            if self.cadence_time < self.cadence_time_old:
                self.cadence_time += 65536
            self.cadence = (self.cadence_cnt-self.cadence_cnt_old) * \
                1024*60.0/(self.cadence_time-self.cadence_time_old)
            # print "cadence="+str(self.cadence)
            if self.cadence_time > 65536:
                self.cadence_time -= 65536
            if self.cadence_cnt > 65536:
                self.cadence_cnt -= 65536
            self.cadence_cnt_old = self.cadence_cnt
            self.cadence_time_old = self.cadence_time

    def getCadence(self):
        if self.stop_cnt1 == 0:
            self.stop_cadence_pre = self.cadence
            # print 'come to zero'
        self.stop_cnt1 = self.stop_cnt1+1
        if self.stop_cnt1 == 2:
            if abs(self.cadence-self.stop_cadence_pre) < 0.00001:
                self.cadence = 0
                # print 'cadence stop!'

            self.stop_cnt1 = 0

        return float(self.cadence)
