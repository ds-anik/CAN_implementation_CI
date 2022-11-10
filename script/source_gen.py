include = '#include "canbus.h"\n#include "buffer.h"\n'
struct_message = "typedef struct message\n{\n\tuint32_t id;\n\tuint8_t len;\n\tuint8_t buf[8];\n} message_t;\n\n"


def build_source(path, defines, messages):

    with open(path+"/canbus.c", "w") as file:
        try:
            file.write(include)
            file.write(struct_message)
            file.write("message_t messages[{}]={{".format(len(messages)))
            for idx, message in enumerate(messages):
                bits_sum= sum([i['length'] for i in message["signals"]])
                file.write("{{{id},{len},{{0}}}}".format(id=message["id"], len=((bits_sum)//8 if (bits_sum % 8)==0 else int(bits_sum/8) +1 ) ,))    
                if idx != (len(messages) - 1):
                    file.write(",")
                else:
                    file.write("};\n\n")

            for idx, message in enumerate(messages):
                for signal in message["signals"]:

                    if 'values' in signal.keys():

                        file.write("bool canbus_set_{}({} value)\n{{\n\tbool status=false;".format(
                            signal["name"], signal["type"]))
                        file.write("\n\tif (")
                        for i in range(len(defines[signal['values']])):

                            file.write("(value == {})".format(
                                defines[signal['values']][i]))
                            if i != (len(defines[signal['values']]) - 1):
                                file.write(" || ")
                            else:
                                file.write(")")
                        file.write("\n\t{{\n\t\tbuffer_insert(messages[{}].buf, {}, {}, value);".format(
                            idx, signal["start"], signal["length"]))
                        file.write(
                            "\n\t\tstatus = true;\n\t}\n\treturn status;\n}\n\n")

                        file.write("{type} canbus_get_{name}(void)\n{{\n\treturn buffer_extract(messages[{idx}].buf, {start}, {len});\n}}\n\n ".format(
                            type=signal["type"], name=signal["name"], idx=idx, start=signal["start"], len=signal["length"]))

                    elif 'range' in signal.keys():
                        if 'uint' in signal['type']:

                            file.write("bool canbus_set_{}({} value)\n{{\n\tbool status=false;".format(
                                signal["name"], signal["type"]))
                            file.write("\n\tif ((value >= {}) && (value <= {}))\n\t{{".format(
                                signal['range'][0], signal['range'][1]))
                            file.write("\n\t\tbuffer_insert(messages[{}].buf, {}, {}, value);".format(
                                idx, signal["start"], signal["length"]))
                            file.write(
                                "\n\t\tstatus = true;\n\t}\n\treturn status;\n}\n\n")

                            file.write("{type} canbus_get_{name}(void)\n{{\n\treturn buffer_extract(messages[{idx}].buf, {start}, {len});\n}}\n\n ".format(
                                type=signal["type"], name=signal["name"], idx=idx, start=signal["start"], len=signal["length"]))

                        elif 'float':   # float numbers

                            file.write("bool canbus_set_{}({} value)\n{{\n\tbool status=false;\n".format(
                                signal["name"], signal["type"]))
                            file.write("\n\tif ((value >= {}) && (value <= {}))\n\t{{".format(
                                signal['range'][0], signal['range'][1]))
                            file.write("\n\t\tbuffer_insert(messages[{}].buf, {}, {},(uint64_t)(10*value));".format(
                                idx, signal["start"], signal["length"]))
                            file.write(
                                "\n\t\tstatus = true;\n\t}\n\treturn status;\n}\n\n")

                            file.write("{type} canbus_get_{name}(void)\n{{\n\tint value=(int)buffer_extract(messages[{idx}].buf, {start}, {len});".format(
                                type=signal["type"], name=signal["name"], idx=idx, start=signal["start"], len=signal["length"]))
                            file.write("\n\tif (value > {})\n\t{{\n\t\tvalue = value | (0xFFFFFFFF << {});\n\t}}".format(
                                2 ** (signal["length"]-1)-1, signal["length"]))
                            file.write(
                                "\n\treturn value / 10.0f;\n}\n\n")

        except Exception as err:
            print("Error writing to source", err)
