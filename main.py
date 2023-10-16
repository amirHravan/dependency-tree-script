import os
import re
import consts
from graph import Graph, Node


class KotlinInterface:
    FUNCTION_REGEX = '([\\w]*\\s)?fun\\s*([\\w<>]*)\\s*[(][@\\w\\d\\s]*:*([\\w\\d\\s]*)[)]'
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

    def get_signature(self):
        return f"interface {self.name} " + "{"

    def __str__(self):
        return f"{self.name} : {self.functions} {self.attributes}"

    def __repr__(self):
        return f"{self.name} : {self.functions} {self.attributes}"

    def collect(self, line):
        search_result = re.search(self.FUNCTION_REGEX, line)
        if search_result is not None:
            self._add_function(search_result.group(2))
        else:
            search_result = re.search(self.ATTRIBUTE_REGEX, line)
            if search_result is not None:
                self._add_attribute(search_result.group(4))
        if "}" in line:
            self.shouldContinue = False


class KotlinClass:
    OVER_RIDE_REGEX = 'override\\s+(\\w*\\s*)?((val)|(var)|(fun))\\s+(\\w+)'
    INPUT_REGEX = '(\\w+)\\s*:\\s*(\\w*(<\\w*\\?*>)?)'

    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.inputs = []
        self.overrides = []
        self.shouldContinue = True
        self.checkForInput = True

    def _add_input(self, attribute):
        self.inputs.append(attribute)

    def _add_override(self, function):
        self.overrides.append(function)

    def get_signature(self):
        if self.class_type == "":
            return "class " + self.name + " {"
        else:
            return self.class_type + " class " + self.name + " {"

    def __str__(self):
        return f"{self.name} : {self.inputs} {self.overrides}"

    def __repr__(self):
        return f"{self.name} : {self.inputs} {self.overrides}"

    def collect(self, line):
        search_result = re.search(self.OVER_RIDE_REGEX, line)
        if search_result is not None:
            self._add_override(search_result.group(6))
        search_result = re.search(consts.INJECT_VIEWMODEL_REGEX, line)
        if search_result is not None:
            self._add_input(search_result.group(2))

        elif self.checkForInput:
            search_result = re.search(self.INPUT_REGEX, line)
            if search_result is not None and search_result.group(2) not in EXCLUDE_LIST:
                self._add_input(search_result.group(2))
        if "{" in line:
            self.checkForInput = False



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
    # print(file_path)
    flag = None
    if file_path.split(".").pop() != "kt":
        return
    with open(file_path, 'r') as file:
        for line in file:
            if flag is None:
                search_result = re.search(consts.INTERFACE_NAME_REGEX, line)
                if search_result is not None:
                    flag = KotlinInterface(search_result.group(1))
                    interface_list.append(flag)
                if "//" in line or "/*" in line:
                    continue
                search_result = re.search(consts.CLASS_NAME_REGEX, line)
                if "class " in line:
                    class_type = search_result.group(2)
                    if class_type is not None:
                        if class_type == "data" or class_type == "sealed" or class_type == "enum":
                            continue
                    else:
                        class_type = ""
                    flag = KotlinClass(search_result.group(4), class_type)
                    class_list.append(flag)
                else:
                    continue
            flag.collect(line)
            if not flag.shouldContinue:
                break


def write_data_on_file():

    tree = Graph()
    with open(OUTPUT_FILE_LOAN_PATH, "w") as file:
        file.write("@startuml\n")
        for kt_class in class_list:
            if len(kt_class.overrides) == 0:
                continue
            file.write(kt_class.get_signature() + "\n")
            for class_property in kt_class.overrides:
                file.write("overrides " + class_property + "\n")
            file.write("}\n")
        for interface in interface_list:
            if len(interface.functions) == 0 and len(interface.attributes) == 0:
                continue
            file.write(interface.get_signature() + "\n")
            for attribute in interface.attributes:
                file.write(attribute + "\n")
            for func in interface.functions:
                file.write(func + "()" + "\n")
            file.write("}\n")
        file.write("\n\n\n")
        for kt_class in class_list:
            tree.add_node(Node(kt_class.name, ""))
            for dependency in kt_class.inputs:
                tree.add_node(Node(dependency, ""))
                tree.add_edge(kt_class.name, dependency)
        for node in tree.nodes:
            for child in node.children:
                if child.node_name != "" and node.node_name != "":
                    file.write(node.node_name + "-" * (len(node.children)+1) + ">" + child.node_name + "\n")
        file.write("@enduml\n")
        file.close()


interface_list = []
class_list = []
EXCLUDE_LIST = ["CoroutineDispatcherProvider"]
OUTPUT_FILE_LOAN_PATH = "/Users/user/Documents/Android Studio Project/driver-app/feature/loan/src/main/java/loan/utils/loan.puml"

directory_path = "/Users/user/Documents/Android Studio Project/driver-app/feature/loan/src/main/java/loan"
print_files(directory_path)

for item in interface_list:
    print(item)
print('-' * 50)
for item in class_list:
    print(item)

write_data_on_file()
