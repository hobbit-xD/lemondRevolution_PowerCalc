class PowerCalculator:

    xp = [0, 10, 17.7, 19.2, 21, 23.2, 24, 26, 26.1, 27.6, 28.6, 29.4,
          31.5, 31.6, 34, 35.3, 36.8, 37.5, 40, 42.9, 46.2, 50, 55, 59, 60]
    # power values
    yp = [0, 25, 45, 50, 67, 80, 95, 110, 115, 125, 145, 147, 180,
          180, 215, 250, 270, 295, 340, 410, 530, 640, 800, 1000, 1050]

    def __init__(self):
        self.power = 0.0


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
        return self.power

    def calculatePower(self, speed, cadence):
        if cadence != 0.0:
            self.power = self.interp(self.xp,self.yp,speed)
        else:
            self.power = 0.0

        return int(self.power)