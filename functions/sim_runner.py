import json
import os


def parse_filename(filename):
    spaces = []
    for idx, char in enumerate(filename):
        if char == ' ':
            spaces.append(idx)
    res = (filename[spaces[-1]+1:])
    return res

def transform_filename(file):
    values = file[0]+file[2]+file[4]
    if file[1] == file[3] == file[5]:
        suffix = 'm'
        return values + suffix + '.gto'
    elif file[1]!= file[3] and file[1]!= file[5] and file[3]!=file[5]:
        suffix = 'r'
        return values + suffix + '.gto'
    elif file[0] == file[2] or file[2] == file[4]:
        if file[1] == file[3] or file[3] == file[5] or file[1] == file[5]:
            suffix = 's'
            return values + suffix + '.gto'
    elif file[1] == file[5]:
        suffix = '-2'
        return values + suffix + '.gto'
    elif file[3] == file[5]:
        suffix = '-1'
        return values + suffix + '.gto'
    elif file[1] == file[3]:
        suffix = '-3'
        return values + suffix + '.gto'
    else:
        return ''

def rename_sim_files(files, prefix):
    for file in files:
        if len(file) == 10:
            newfile = transform_filename(file)
            print(file, "is a GTO+ file, renaming to", newfile)
            os.rename('./sims/'+file, './sims/'+prefix+newfile)
            file = prefix+newfile
    return files

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
        return simname[0:1] + 'h' + simname[1:2] + 'c' + simname[2:3] + 'd'
    elif simname[-1] == "1":
        return simname[0:1] + 'h' + simname[1:2] + 'c' + simname[2:3] + 'c'
    elif simname[-1] == "2":
        return simname[0:1] + 'h' + simname[1:2] + 'c' + simname[2:3] + 'h'
    elif simname[-1] == "3":
        return simname[0:1] + 'h' + simname[1:2] + 'h' + simname[2:3] + 'c'
    elif simname[-1] == "s":
        return simname[0:1] + 'h' + simname[1:2] + 'h' + simname[2:3] + 'c'
    else:
        raise TypeError

def start_solving_session(range1, range2):
        #click on range 1
    pass
        #enter range

        #click enter

        #click on range 2

        #enter range

        #click enter

def solve_board(board):

        #click on board
    pass
        #click on board field

        #enter board

        #click on build tree

        #click on advanced

        #click on build tree

        #click on build new tree

        #click on run solver

        #wait for "Finalizing"








