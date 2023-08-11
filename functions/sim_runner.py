import json
import os


def parse_filename(filename):
    spaces = []
    for idx, char in enumerate(filename):
        if char == ' ':
            spaces.append(idx)
    res = (filename[spaces[-1] + 1:])
    return res


def transform_filename(file):
    values = file[0] + file[2] + file[4]
    if file[1] == file[3] == file[5]:
        suffix = 'm'
        return values + suffix + '.gto'
    elif file[1] != file[3] and file[1] != file[5] and file[3] != file[5]:
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
            os.rename('./sims/' + file, './sims/' + prefix + newfile)
            file = prefix + newfile
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
        return simname[0:1] + 'h' + simname[1:2] + 'h' + simname[2:3] + 'h'
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


def create_gto_database():
    print("Reading processed sims")
    sims = read_sim_status_list()
    print("Found", len(sims), "solved or processed sims")
    registered = []
    for sim in sims:
        registered.append(sim.split(' ')[2][:-4])
        # print(file2board(sim.split(' ')[2][:-4])) #split filename into readable chunks and only use board part
    print("Reading available boards")
    allboards = read_boards_2t() + read_boards_m() + read_boards_r()
    print("There is a total of", len(allboards), "available boards")
    db = []
    for board in allboards:
        if board not in registered:
            db.append(file2board(board))

    with open('./database.txt', 'w') as database:
        for x in db:
            database.write(str(x) + '\n')
    print("Solver database consisting of", len(db), "boards created")


def read_boards_2t():
    boards2t = []
    with open('./boards_2t.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > 2:  # if there are no blanks
                boards2t.append((line.strip('\n')))
    for i in range(len(boards2t)):
        if boards2t[i - 2] == boards2t[i - 1] == boards2t[i]:
            boards2t[i - 2] = boards2t[i - 2] + '-1'
            boards2t[i - 1] = boards2t[i - 1] + '-2'
            boards2t[i] = boards2t[i] + '-3'
    for idx, item in enumerate(boards2t):
        if item[-2] != '-':
            boards2t[idx] = item + 's'
    return boards2t


def read_boards_m():
    boards_m = []
    with open('./boards_m.txt', 'r') as file:
        lines = lines = file.readlines()
        for line in lines:
            boards_m.append(line.strip('\n') + 'm')
    return boards_m


def read_boards_r():
    boards_r = []
    with open('./boards_r.txt', 'r') as file:
        lines = lines = file.readlines()
        for line in lines:
            boards_r.append(line.strip('\n') + 'r')
    return boards_r


def start_solving_session(range1, range2):
    # click on range 1
    pass
    # enter range

    # click enter

    # click on range 2

    # enter range

    # click enter


def solve_board(board):
    # click on board
    pass
    # click on board field

    # enter board

    # click on build tree

    # click on advanced

    # click on build tree

    # click on build new tree

    # click on run solver

    # wait for "Finalizing"


if __name__ == '__main__':
    create_gto_database()
