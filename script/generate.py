import json
import os
import header_gen
import source_gen
import test_gen

path = "./lib/canbus"
path_test = "./test"

with open("data.json", "r") as file:
    try:
        data = json.load(file)
    except Exception as err:
        print("Error loading data.json: ", err)

defines = data["defines"]
messages = data["messages"]


path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
if not os.path.isdir(path):
    try:
        os.mkdir(path)
    except Exception as err:
        print("Error creating path", err)
if not os.path.isdir(path_test):
    try:
        os.mkdir(path_test)
    except Exception as err:
        print("Error creating path", err)
try:
    header_gen.build_header(path, defines, messages)
    source_gen.build_source(path, defines, messages)
    test_gen.build_test(path_test, defines, messages)
except Exception as err:
    print("Error generating files: ", err)
