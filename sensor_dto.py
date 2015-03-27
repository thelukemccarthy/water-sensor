class SensorDto(object):
    
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class SensorWithRawDto(SensorDto):
    
    def __init__(self, value, raw_value):
        super(SensorWithRawDto, self).__init__(value)
        self.__raw_value = raw_value

    def get_raw_value(self):
        return self.__raw_value

class AirDto:
    
    def __init__(self, air_temperature, humidity):
        self.air_temperature = air_temperature
        self.humidity = humidity

    def get_temperature(self):
        return self.air_temperature

    def get_humidity(self):
        return self.humiditye
