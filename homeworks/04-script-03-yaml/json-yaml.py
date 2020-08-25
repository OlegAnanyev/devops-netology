#!/usr/bin/env python3

import sys
import yaml
import json


def is_json(myjson):
    try:
        json_object = json.load(myjson)
    except ValueError as e:
        return False
    return True


def is_yaml(myyaml):
    try:
        yaml_object = yaml.safe_load(myyaml)
    except yaml.YAMLError as e:
        return False
    return True


def json_to_yaml(json_file_name):
    j = open(json_file_name, "r")
    yaml_file_name = json_file_name.split(".")[0] + ".yaml"
    y = open(yaml_file_name, "w")
    yaml.dump(json.load(j), y)
    j.close()
    y.close()
    return


def yaml_to_json(yaml_file_name):
    y = open(yaml_file_name, "r")
    json_file_name = yaml_file_name.split(".")[0] + ".json"
    j = open(json_file_name, "w")
    json.dump(yaml.safe_load(y), j)
    y.close()
    j.close()
    return


if len(sys.argv) < 2:
    print("Need file name to convert!")
    exit(-1)

filename = sys.argv[1]
f = open(filename, "r")

if is_json(f):
    print("JSON!")
    json_to_yaml(filename)
elif is_yaml(f):
    print("YAML!")
    yaml_to_json(filename)
else:
    print("This file isn't JSON or YAML!")
    exit(-1)
f.close()
