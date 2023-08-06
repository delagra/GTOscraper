import json
import os


def parse_filename(filename):
    spaces = []
    for idx, char in enumerate(filename):
        if char == ' ':
            spaces.append(idx)
    res = (filename[spaces[-1]:])
    return res.replace('.gto', '')


def get_sim_files(path):
    all_files = os.listdir(path.replace('\\', '/'))
    files_with_extension = [file for file in all_files if file.endswith(".gto")]
    return files_with_extension

def write_sim_status_list(data):
    with open('./processed.json', "w") as f:
        json.dump(data, f)
def read_sim_status_list():
    try:
        with open('./processed.json', "r") as f:
            loaded_data = json.load(f)
            return loaded_data
    except FileNotFoundError:
        write_sim_status_list({})
        return read_sim_status_list()

def file2board(simname):
    if simname[-1] == 'm':
        return simname[0:1]+'h'+simname[1:2]+'h'+simname[2:3]+'h'
    elif simname[-1] == 'r':
        return simname[0:1] + 'h' + simname[1:2] + 'd' + simname[2:3] + 's'
    elif simname[-1] == "1":
        return simname[0:1] + 'h' + simname[1:2] + 'd' + simname[2:3] + 'd'
    elif simname[-1] == "2":
        return simname[0:1] + 'h' + simname[1:2] + 'd' + simname[2:3] + 'h'
    elif simname[-1] == "3":
        return simname[0:1] + 'd' + simname[1:2] + 'd' + simname[2:3] + 'h'
    else:
        raise TypeError





