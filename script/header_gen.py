
begin_header = "#ifndef CANBUS_H\n#define CANBUS_H\n"
include = "#include <stdbool.h>\n#include <stdint.h>\n"
end_header = "#endif"


def build_header(path, defines, messages):

    with open(path+"/canbus.h", "w") as file:
        try:
            file.write(begin_header)
            file.write(include)
            for key in defines:
                for definition in defines[key]:
                    file.write("#define {} {}\n".format(
                        definition, defines[key].index(definition)))
            for message in messages:
                for signal in message["signals"]:
                    if 'range' in signal.keys():
                        file.write("/**\n*@brief Function to set {name} in the range {min} - {max}.\n*@param {type} value\n*@return True if succesfully set, else False.\n*/\n".format(
                            name=signal["name"], min=signal["range"][0], max=signal["range"][1], type=signal["type"]))
                    elif signal['values'] == "status":
                        file.write("/**\n*@brief Function to set {name} to either of these valid statuses {status}.\n*@param {type} value\n*@return True if succesfully set, else False.\n*/\n".format(
                            name=signal["name"], status=str(defines["status"]), type=signal["type"]))
                    elif signal['values'] == "states":
                        file.write("/**\n*@brief Function to set {name} to either of these valid states {states}.\n*@param {type} value\n*@return True if succesfully set, else False.\n*/\n".format(
                            name=signal["name"], states=str(defines["states"]), type=signal["type"]))
                    file.write(
                        "bool canbus_set_{}({} value);\n".format(signal["name"], signal["type"]))
                    if 'range' in signal.keys():
                        file.write("/**\n*@brief Function to get {name}.\n*@return {type} value in the range {min} - {max}\n*/\n".format(
                            name=signal["name"], min=signal["range"][0], max=signal["range"][1], type=signal["type"]))
                    elif signal['values'] == "status":
                        file.write("/**\n*@brief Function to get {name}.\n*@return A {type} status among these {status} \n*/\n".format(
                            name=signal["name"], status=str(defines["status"]), type=signal["type"]))
                    elif signal['values'] == "states":
                        file.write("/**\n*@brief Function to get {name}.\n*@return A {type} state among these {states} \n*/\n".format(
                            name=signal["name"], states=str(defines["states"]), type=signal["type"]))
                    file.write(
                        "{} canbus_get_{}(void);\n\n".format(signal["type"], signal["name"]))

            file.write(end_header)
        except Exception as err:
            print("Error writing to header", err)
