
include = '#include "unity.h"\n#include "canbus.h"\n\n'


def build_test(path, defines, messages):

    with open(path+"/canbus_test.c", "w") as file:
        try:
            file.write(include)
            file.write('void setUp() {}\nvoid tearDown(){}\n\n')
            for message in messages:
                for signal in message["signals"]:

                    if signal['type'] != 'float':
                        signal_type = signal['type'][0:-2].upper()
                    else:
                        signal_type = signal['type'].upper()

                    for action in ['set', 'get']:
                        file.write("void test_{}_{}(void)\n{{".format(
                            action, signal["name"]))
                        if 'range' in signal.keys():

                            for j in ([i-2 for i in signal['range']] + [i+5 for i in signal['range']]):
                                if j >= signal['range'][0] and j <= signal['range'][1]:
                                    file.write("\n\tTEST_ASSERT_TRUE(canbus_set_{}({}));".format(
                                        signal["name"], j))
                                    if action == 'get':
                                        file.write("\n\tTEST_ASSERT_EQUAL_{}({} , canbus_get_{}());".format(
                                            signal_type, j, signal["name"]))

                                else:
                                    if action == 'set':
                                        file.write("\n\tTEST_ASSERT_FALSE(canbus_set_{}({}));".format(
                                            signal["name"], j))

                        elif signal['values'] == "status":
                            # ["UNINITIALIZED", "OKAY", "ERROR"]:
                            for stat in defines["status"]:
                                file.write("\n\tTEST_ASSERT_TRUE(canbus_set_{}({}));".format(
                                    signal["name"], stat))
                                if action == 'get':
                                    file.write("\n\tTEST_ASSERT_EQUAL_{}({} , canbus_get_{}());".format(
                                        signal_type, stat, signal["name"]))

                            if action == 'set':
                                for num in [-1, 3]:
                                    file.write("\n\tTEST_ASSERT_FALSE(canbus_set_{}({}));".format(
                                        signal["name"], num))

                        elif signal['values'] == "states":
                            for stat in defines["states"]:  # ["ON", "OFF"]:
                                file.write("\n\tTEST_ASSERT_TRUE(canbus_set_{}({}));".format(
                                    signal["name"], stat))
                                if action == 'get':
                                    file.write("\n\tTEST_ASSERT_EQUAL_{}({} , canbus_get_{}());".format(
                                        signal_type, stat, signal["name"]))

                            if action == 'set':
                                for num in [-1, 2]:
                                    file.write("\n\tTEST_ASSERT_FALSE(canbus_set_{}({}));".format(
                                        signal["name"], num))
                        else:
                            file.write(
                                "\n\t//Unkown type of signal. No test created")

                        file.write('\n}\n')

            file.write('int main(void)\n{')
            file.write('\n\tUNITY_BEGIN();')

            for message in messages:
                for signal in message["signals"]:
                    file.write(
                        "\n\tRUN_TEST(test_set_{});".format(signal["name"]))
                    file.write(
                        "\n\tRUN_TEST(test_get_{});".format(signal["name"]))

            file.write('\n\treturn UNITY_END();')

            file.write('\n}')
        except Exception as err:
            print("Error writing to test: ", err)
