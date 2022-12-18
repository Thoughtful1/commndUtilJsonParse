import sys
import logging
import time
import random
import string
import uuid
import os
import json

log = logging.getLogger(None)
logging.basicConfig(format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("sample.log"),
                              logging.StreamHandler()],
                    level=logging.DEBUG)


def name_generator():
    """Generate random names with length from 5 to 9 letters"""
    size = random.randint(5, 9)
    chars = string.ascii_letters
    name_var = ''.join(random.choice(chars) for _ in range(size))
    return name_var.capitalize()


def age_generator():
    """Generate random age"""
    return random.randint(1, 100)


def generate_uuid():
    """Generate random uuid"""
    return str(uuid.uuid4())


def save_file(json_file, path, name_of_file):
    """save json file in specified path"""
    complete_path_w_name = os.path.join(path, name_of_file + ".json")
    with open(complete_path_w_name, "a") as file1:
        file1.write(str(json_file) + '\n')
        # print("***successfully saved a json file***")
        log.info("***successfully saved a json file***")


def clear_path(path, name_of_file):
    """clear all files which start with following name_of_file in given path"""
    # print("***cleaning of json files with same name***")
    log.info("***cleaning of json files with same name***")
    for fname in os.listdir(path):
        if not fname.startswith(name_of_file):
            continue
        os.remove(os.path.join(path, fname))


def count_data_lines(path, name_of_file, prefix):
    """count text lines in .json files"""
    line_count = 0
    complete_path_w_name = os.path.join(path, name_of_file + "_" + prefix + ".json")
    with open(complete_path_w_name) as file1:
        for line in file1:
            if line != "\n":
                line_count += 1
    return str(line_count)


def count_lines(path, file, prefix):
    """Wrapper for lines counting def. Formats returning message"""
    if data_linesBool:
        # print("Quantity of lines:" + count_data_lines(os.path.realpath(path), file, prefix))
        log.info("Quantity of lines:" + count_data_lines(os.path.realpath(path), file, prefix))


def check_if_config_exist():
    """As def name suggest it's checking if config exist..."""
    if os.path.isfile("config.ini"):
        return True
    return False


def validate_count_value(value):
    """Validates if given arg is an Integer"""
    try:
        value = int(value)
        return value
    except ValueError:
        log.info("Wrong count value. Setting default 0")
        # print("Wrong count value. Setting default 0")
        return 0


def check_first_args(args=None):
    """In the beginning def is checking if config.ini file exist.
    If not it create a new one with default values.
    Process all long arguments given by user while starting python json processing script."""
    import argparse
    import configparser
    config_object = configparser.RawConfigParser()
    if check_if_config_exist():
        config_object.read('config.ini')
        config_object.get('WHOLE_DEFAULT_CONFIGURATION', 'path_to_save_files')
        config_object.get('WHOLE_DEFAULT_CONFIGURATION', 'files_count')
        config_object.get('WHOLE_DEFAULT_CONFIGURATION', 'file_name')
        config_object.get('WHOLE_DEFAULT_CONFIGURATION', 'file_prefix')
        config_object.get('WHOLE_DEFAULT_CONFIGURATION', 'data_schema')

    elif not check_if_config_exist():
        config_object.add_section('WHOLE_DEFAULT_CONFIGURATION')
        config_object.set('WHOLE_DEFAULT_CONFIGURATION', 'path_to_save_files', '')
        config_object.set('WHOLE_DEFAULT_CONFIGURATION', 'files_count', '0')
        config_object.set('WHOLE_DEFAULT_CONFIGURATION', 'file_name', 'example')
        config_object.set('WHOLE_DEFAULT_CONFIGURATION', 'file_prefix', 'random')
        config_object.set('WHOLE_DEFAULT_CONFIGURATION', 'data_schema', '*no path*')
        with open("config.ini", "w") as file1:
            config_object.write(file1)
            file1.close()
    parser = argparse.ArgumentParser()
    default_values = config_object['WHOLE_DEFAULT_CONFIGURATION']

    parser.add_argument('--path_to_save_files',
                        help="Where all files need to save. It's either relative or absolute"
                             " path default is script's location",
                        default=default_values['path_to_save_files'])
    parser.add_argument('--files_count',
                        help='How many json files to generate. Default is 0',
                        default=int(default_values['files_count']))
    parser.add_argument('--file_name',
                        help='Base file_name. If no prefix, final file name will be file_name.json.'
                             ' With prefix full file name will be file_name_file_prefix.json',
                        default=default_values['file_name'])
    parser.add_argument('--file_prefix',
                        choices=['count', 'random', 'uuid'],
                        default=default_values['file_prefix'],
                        help='What prefix for file name to use if more than 1 file needs to be generated')
    parser.add_argument('--data_schema',
                        help="It's a string with json schema or path to json file, last line in a file will be picked "
                             "as a json file",
                        default=default_values['data_schema'])
    parser.add_argument('--data_lines',
                        help='Count of lines for each file',
                        action='store_true', )
    parser.add_argument('--clear_path',
                        action='store_true',
                        help='All files in provided path with file_name same as provided '
                             'will be deleted. Default is false')
    results = parser.parse_args(args)
    return (results.path_to_save_files,
            results.files_count,
            results.file_name,
            results.file_prefix,
            results.data_schema,
            results.data_lines,
            results.clear_path)


def file_prefix_adder(prefix):
    """Validates if prefix value is one of three allowed types. Which is either: uuid, random, count"""
    if prefix == "uuid":
        return "uuid"
    if prefix == "random":
        return "random"
    if prefix == "count":
        return "count"


def verify_kind(kind):
    """Validates if kind value is one of three allowed types. Which is either: client, partner, government"""
    while True:
        print("type in kind from [client, partner, government]")
        kind = input()
        if kind not in ['client', 'partner', 'government']:
            print("wrong input data")
        if kind in ['client', 'partner', 'government']:
            break
    return kind


def specify_json_schema_values(name: str, count: int, path: str, file_name: str, file_prefix: str):
    """"Forge a new json string.
    Can create multiple json strings with certain count digit arg.
    Def create json in a path given by the user.
    Same thing goes for file and prefix name"""
    timestamp = time.time()
    count = int(count)
    kind = ""
    kind = verify_kind(kind)
    custom_dict = {"date": timestamp, "name": name, "type": kind, "age": str(age_generator())}
    custom_dict = json.dumps(custom_dict)
    if count < 0:
        # print("Quantity can't be negative")
        log.warning("Quantity can't be negative")
        return
    elif count == 0:
        log.info("Following args were logged:" + str(custom_dict))
        # print("Following args were logged:" + str(custom_dict))
        return
    log.info("Following args were logged:" + str(custom_dict))
    # print("Following args were logged:" + str(custom_dict))
    save_file(custom_dict, os.path.realpath(path), (str(file_name) + "_" + str(file_prefix)))
    count = count - 1
    while count > 0:
        count = count - 1
        kind = verify_kind(kind)
        age = age_generator()
        custom_dict = {"date": timestamp, "name": name, "type": kind, "age": str(age)}
        custom_dict = json.dumps(custom_dict)
        log.info("Following args were logged:" + str(custom_dict))
        # print("Following args were logged:" + str(custom_dict))
        save_file(custom_dict, os.path.realpath(path), (str(file_name) + "_" + str(file_prefix)))


def check_path_to_file(data_schema: str, name_of_file: str, prefix: str):
    """Check if given data_schema is in fact a path to a json file"""
    try:
        log.info("Not correct json string. Proceeding to verifying the path")
        complete_path_w_name = os.path.join(data_schema + name_of_file + "_" + prefix + ".json")
        with open(complete_path_w_name) as file1:
            for line in file1:
                if line != "\n":
                    json_line = str(line)
                    log.info("Following args were read from json file:" + str(json_line))
                    # print("Following args were read from json file:" + str(json_line))
        return True
    except IOError:
        log.info("DataSchema Path not found")
        # print("DataSchema Path not found")
        return False


def check_data_schema(data_schema: str, path: str, name_of_file: str, prefix: str):
    """Check if data_schema is in fact a string var with a json inside"""
    json_arg = str(data_schema)
    try:
        if not data_schema:
            log.info("Data_schema is not a json")
            # print("Data_schema is not a json")
            return check_path_to_file(data_schema, name_of_file, prefix)
        json.loads(data_schema)
    except ValueError:
        log.info("Data_schema is not a json")
        # print("Data_schema is not a json")
        return check_path_to_file(data_schema, name_of_file, prefix)
    json_object = json.loads(json_arg)
    if "date" in json_object:
        if "name" in json_object:
            if "type" in json_object:
                if "age" in json_object:
                    save_file(json_object, os.path.realpath(path), (str(name_of_file) + "_" + str(prefix)))
                    log.info("Successfully read json from data_schema. "
                             "Following args were logged:" + str(json_object))
                    # print("Successfully read json from data_schema. "
                    #      "Following args were logged:" + str(json_object))
                    return True
    return False


if __name__ == '__main__':

    path_to_files_saving, files_count, file_name, file_prefix,\
        data_schema, data_linesBool, clear_pathBool \
        = check_first_args(sys.argv[1:])
    files_count = validate_count_value(files_count)
    if clear_pathBool:
        clear_path(os.path.realpath(path_to_files_saving), (file_name + "_" + file_prefix))
    # print("input path is: " + str(path_to_files_saving))
    name = str(generate_uuid())

    if not check_data_schema(data_schema, path_to_files_saving, file_name, file_prefix):
        specify_json_schema_values(name, files_count, path_to_files_saving, file_name, file_prefix)

    if data_linesBool:
        count_lines(os.path.realpath(path_to_files_saving), file_name, file_prefix)
