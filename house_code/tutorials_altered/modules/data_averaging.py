class DataAveraging:

    @staticmethod
    def add_sensor_data_to_total(sensor_data, previous_total):
        new_total = previous_total
        for i in range(0,len(sensor_data)):
            data_point = sensor_data[i]
            if type(data_point) == int or type(data_point) == float:
                new_total[i] = sensor_data[i]

        return new_total

    @staticmethod
    def get_average_sensor_data(total_sensor_data, index):
        averaged_sensor_data = total_sensor_data
        for i in range(0, len(averaged_sensor_data)):
            data_point = averaged_sensor_data[i]
            if type(data_point) == int or type(data_point) == float:
                averaged_sensor_data[i] = averaged_sensor_data[i] / index

        return averaged_sensor_data