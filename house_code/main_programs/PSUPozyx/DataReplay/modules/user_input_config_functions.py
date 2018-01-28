class UserInputConfigFunctions():
    @staticmethod
    def get_attributes_to_log_from_str(attributes_to_log_str):
        possible_attributes = ["pressure", "acceleration", "magnetic", "angular velocity", "euler angles",
                               "quaternion", "linear acceleration", "gravity"]
        attributes_to_log_list = []
        for idx, char in enumerate(attributes_to_log_str):
            if char is '1':
                attributes_to_log_list.append(possible_attributes[idx])
        return attributes_to_log_list
