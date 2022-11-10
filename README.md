# CAN Implementation

## YrkesAkademin Group Project - Embedded Programming Course



[![Build and Test](https://github.com/jimmybjorkman/CI_assignment_2/actions/workflows/BuildAndTest.yml/badge.svg)](https://github.com/jimmybjorkman/CI_assignment_2/actions/workflows/BuildAndTest.yml)

### Assignment Description:

<div align="justify">As you know, in CAN we need to pack and unpack messages by inserting multiple signals in the data field of a message and extracting the signals from it. And you also know that the data field in a CAN message is an array of max. 8 elements of type uint8_t (unsigned char). To handle packing and unpacking messages a module(buffer) including buffer.h and macos.o/linux.o/windows.o has been provided.<br> <div />

<div align="justify">You also know that if we have a list of messages and signals we can generate a C module automatically using Python in order to get and set the values of signals and in this way we can have a maintainable module. By generating the C module automatically, if we want to change the messages and signals, only we need to change the list and regenerate the module.<div />

<br>

<div align="justify"><b>you are supposed to develop python scripts to automatically generate a module to get and set values of signals based on messages structured in data.json.<b/><div /> 

### Requirements:

- You need to follow Scrum and Github Flow strategy.
- To build and test the module use make and a Makefile. You need to link the right object file in lib/buffer, depending on the OS.
-  In Github Actions automate your workflow using: 
    - A workflow which is triggered when you push or make a pull request from your feature branch to the mainline in order to generate, build and test the module.
    - The workflows shall be run on ubuntu and created by yourself.
- The python script(generate.py) shall automatically:
    - Generate a C module (canbus) in folder lib.
        - The generated module shall have a header file and a source.
        - The module shall have functions to set and get the value of all the signals listed in data.josn.
        - A function name is made of two parts: canbus_set_/canbus_get_ and name of the signal. i.e bool canbus_set_temperature(float value); 
        - In the source file a data type (message_t) shall be created. typedef struct { uint32_t id; uint8_t len; uint8_t buf[8]; } message_t; and an array of message_t based on the number of messages in data.json.
        - For float values, precision of 0.1 is enough. You can multiply float values by 10 and round them when you want to write them to the buffer and in the getter functions of float signals you need to divide the extracted values by 10. 
        - For the implementation of functions you shall use the buffer module to pack and unpack messages in order to get and set the signals value.
        - In the header file (canbus.h) you shall create macros for the defines in data.json based on the indices of elements in the arrays, and in the implementation file you shall use the macros. E.g. OFF is 0 and ON is 1 
    - Generate canbus_test.c in the test folder in order to test the generated canbus module. All the functions in the canbus module shall be tested. To generate test for a setter function you need to have some cases for the argument of the function:
        - A valid value in the range specified in the signal
        - An invalid value which is lesser than the minimum value in the range.
        - An invalid value which is greater than the maximum value in the range.
        - If the type can hold negative values, you need to test both negative and positive values.
- The python scripts shall be able to handle changes in data.json. E.g. If we add a new message, there shall be no need to change the python scripts. 
- The Makefile shall be able to build and run canbus_test.c.
- In the workflows it shall be possible to run generate.py in order to generate canbus and canbus_test.c 
- Use modular programming to develop the python scripts. For example, a module to generate the header file, a module to generate the source file and a
module to generate the test file. In generate.py you can use the modules to make the program.


