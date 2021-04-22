import json

class Config:
    def __init__(self):
        self.groups = []
        with open('json/parameters.json') as f:
            parameters = json.load(f)
        for group_num in parameters.keys():
            group = Group(group_num, parameters[group_num]['name'])
            self.groups.append(group)
            for param_num in parameters[group_num].keys():
                if param_num != 'name':
                    group.parameters.append(
                        Parameter(
                            group,
                            param_num,
                            parameters[group_num][param_num].get('name',''),
                            parameters[group_num][param_num].get('default',''),
                            parameters[group_num][param_num].get('unit','')
                        ))
        self.sets = []
        with open('json/parameter_sets.json') as f:
            parameter_sets = json.load(f)
        for set_name in parameter_sets.keys():
            set = Group(None, set_name)
            self.sets.append(set)
            for group_param in parameter_sets[set_name]:
                (group_num,param_num) = group_param.split('-')
                set.parameters.append(self.group(group_num).parameter(param_num))

    def group(self, num):
        for group in self.groups:
            if group.num == num:
                return group

class Group:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        self.parameters = []

    def parameter(self, param_num, group_num=None):
        if group_num == None:
            group_num = self.num
        for parameter in self.parameters:
            if parameter.num == param_num and parameter.group.num == group_num:
                return parameter

class Parameter:
    def __init__(self, group, num, name, default, unit):
        self.group = group
        self.num = num
        self.name = name
        self.default = default
        self.unit = unit
