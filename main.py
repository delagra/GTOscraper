import pyautogui as pag
import openpyxl as op

from functions import parser as p, sim_runner as sr


pag.FAILSAFE = False

wb = op.load_workbook('expanded template.xlsx')
ws = wb.active


class Sim:  # class that will contain all sim results to be populated in excel later
    def __init__(self, board):
        self.board = board

    is_monotone = False
    is_two_tone1 = False
    is_two_tone2 = False
    is_two_tone3 = False
    is_rainbow = False
    is_ttp = False
    ace_high = []
    overpair = []
    top_pair = []
    mid_pair = []
    first_action = []
    gutshot = []
    oesd = []
    overcards = []
    nut_fd = []
    weak_fd = []
    sets = []
    combos = []


print(sr.read_sim_status_list())

filename = "AKJm"  # filename to open, change to the conventional

sim = Sim
p.openfile(filename, sim)

#p.process_sim(filename, sim, ws)

#wb.save('test.xlsx')  # save file
