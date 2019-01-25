# -*- coding: UTF-8 -*-


class ParamParser(object):

    def get_args(self, path):
        """
        data_structure: each line of the file is a configuration list,
        and it would be broken down into a dictionary and act as one list node
        :param path:
        :return: a list whose nodes are dictionaries
        """
        dict_list = []
        config = open(path)
        print type(config)
        # each line is a testset configuration
        for line in config:
            line = line.strip(" \n")
            config_list = line.split(",")
            args_dict = {}
            for element in config_list:
                first_position = element.find("=")
                args_dict.update({str(element[0:first_position]): str(element[first_position + 1:])})
            dict_list.append(args_dict)
        return dict_list