import os
import re


class KotlinInterface:
    FUNCTION_REGEX = 'fun\\s*([\\w<>]*)\\s*[(]'
    ATTRIBUTE_REGEX = '((val)|(var))\\s*(\\w*)'

    def __init__(self, name):
        self.name = name
        self.functions = []
        self.attributes = []
        self.shouldContinue = True

    def _add_attribute(self, attribute):
        self.attributes.append(attribute)

    def _add_function(self, function):
        self.functions.append(function)

    def __str__(self):
        return f"{self.name} : {self.functions} {self.attributes}"

    def __repr__(self):
        return f"{self.name} : {self.functions} {self.attributes}"

    def collect(self, line):
        search_result = re.search(self.FUNCTION_REGEX,line)
        if search_result is not None:
            self._add_function(search_result.group(1))
        else:
            search_result = re.search(self.ATTRIBUTE_REGEX, line)
            if search_result is not None:
                self._add_attribute(search_result.group(4))
        if "}" in line:
            self.shouldContinue = False


class KotlinClass:
    OVER_RIDE_REGEX = 'override\\s+((val)|(var))\\s+(\\w+)'
    INPUT_REGEX = '(\\w*)\\s*:\\s*(\\w*(<\\w*\\?*>)?)'

    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.overrides = []
        self.shouldContinue = True

    def _add_input(self, attribute):
        self.inputs.append(attribute)

    def _add_override(self, function):
        self.overrides.append(function)

    def __str__(self):
        return f"{self.name} : {self.inputs} {self.overrides}"

    def __repr__(self):
        return f"{self.name} : {self.inputs} {self.overrides}"

    def collect(self, line):
        search_result = re.search(self.OVER_RIDE_REGEX, line)
        if search_result is not None:
            self._add_override(search_result.group(4))
        else:
            search_result = re.search(self.INPUT_REGEX, line)
            if search_result is not None:
                self._add_input(search_result.group(2))
        if "{" in line:
            self.shouldContinue = False


interface_list = []
class_list = []


def print_files(path):
    for root, directories, files in os.walk(path):
        for file_name in files:
            if str(root).__contains__("test"):
                continue
            file_name_parts = str(file_name).split(".")
            if file_name_parts[len(file_name_parts) - 1] != "kt":
                continue
            file_path = os.path.join(root, file_name)
            check_file(file_path)


def check_file(file_path):
    CLASS_NAME_REGEX = 'class\\s*(\\w+(<\\w*>)?)\\s*[(]?'
    INTERFACE_NAME_REGEX = 'interface\\s*([\\w<>]+)\\s*[^(]'
    # print(file_path)
    flag = None
    with open(file_path, 'r') as file:
        for line in file:
            if "interface " in line:
                flag = KotlinInterface(re.search(INTERFACE_NAME_REGEX, line).group(1))
                interface_list.append(flag)
            elif "class " in line:
                flag = KotlinClass(re.search(CLASS_NAME_REGEX, line).group(1))
                class_list.append(flag)
            if flag is not None:
                flag.collect(line)
                if not flag.shouldContinue:
                    break


directory_path = "/Users/user/Documents/Android Studio Project/driver-app/feature/loan/src"
print_files(directory_path)
for item in interface_list:
    print(item)
print('-'*50)
for item in class_list:
    print(item)

