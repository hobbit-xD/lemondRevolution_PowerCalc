import sys
import time


class PowerCalculator:

    xp = [0, 10, 17.7, 19.2, 21, 23.2, 24, 26, 26.1, 27.6, 28.6, 29.4,
          31.5, 31.6, 34, 35.3, 36.8, 37.5, 40, 42.9, 46.2, 50, 55, 59, 60]
    # power values
    yp = [0, 25, 45, 50, 67, 80, 95, 110, 115, 125, 145, 147, 180,
          180, 215, 250, 270, 295, 340, 410, 530, 640, 800, 1000, 1050]

    def __init__(self):
        self.power = 0.0
        self.init_time = time.time()
        self.last_time1 = self.init_time
        self.last_time2 = self.init_time
        self.threeSec_avgPower = 0.0
        self.thirtySec_avgPower = 0.0
        self.cumulativePower1 = 0.0
        self.cumulativePower2 = 0.0

    def interp(self, x_arr, y_arr, x):
        for i, xi in enumerate(x_arr):
            if xi >= x:
                break
        else:
            return 560

        x_min = x_arr[i - 1]
        y_min = y_arr[i - 1]
        y_max = y_arr[i]
        factor = (x - x_min) / (xi - x_min)
        return y_min + (y_max - y_min) * factor

    def getPower(self):
        return int(self.power)

    def getThreeSecAvgPower(self):
        return int(self.threeSec_avgPower)

    def getThirtySecAvgPower(self):
        return int(self.thirtySec_avgPower)

    def threeSecAvgPowerCalc(self):
        currentTime = time.time()
        time_gap = (currentTime - self.last_time1)

        '''
        print "Init Time: " , self.init_time
        print "Last Time: " , self.last_time
        print "Current Time: " , currentTime
        print "Time gap: " , time_gap
        '''

        if int(time_gap) <= 3:
            self.cumulativePower1 += self.power

            #print "Cumulative Power: " , self.cumulativePower1
        else:
            self.threeSec_avgPower = (self.cumulativePower1 / 3)
            self.cumulativePower1 = 0.0
            self.last_time1 = currentTime

            #print "Avg: " , self.threeMin_avgPower

    def thirtySecAvgPowerCalc(self):
        currentTime = time.time()
        time_gap = (currentTime - self.last_time2)

        '''
        print "Init Time: " , self.init_time
        print "Last Time: " , self.last_time
        print "Current Time: " , currentTime
        print "Time gap: " , time_gap
        '''

        if int(time_gap) <= 30:
            self.cumulativePower2 += self.power

            #print "Cumulative Power: " , self.cumulativePower2
        else:
            self.thirtySec_avgPower = (self.cumulativePower2 / 30)
            self.cumulativePower2 = 0.0
            self.last_time2 = currentTime

            #print "Avg: " , self.thirtySec_avgPower

    def calculatePower(self, speed, cadence):
        if cadence != 0.0:
            self.power = self.interp(self.xp, self.yp, speed)
        else:
            self.power = 0.0

        self.threeSecAvgPowerCalc()
        self.thirtySecAvgPowerCalc()
