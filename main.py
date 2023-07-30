import pyautogui as pag
import pandas as pd
import time
import openpyxl as op

from functions import excel_writer as ew, parser as p
from functions.parser import mouse_locations

pag.FAILSAFE = False

wb = op.load_workbook('expanded template.xlsx')
ws = wb.active

    #print(sheet_ranges)



class Sim: #class that will contain all sim results to be populated in excel later
    def __init__(self, board):
        self.board = board
    is_monotone = False
    is_two_tone1 = False
    is_two_tone2 = False
    is_two_tone3 = False
    is_rainbow = False
    ace_high = []
    overpair = []
    top_pair = []
    mid_pair = []
    first_action =[]
    gutshot = []
    oesd = []
    overcards = []
    nut_fd = []
    weak_fd = []
    sets = []
    combos = []



sim = Sim #initiate class
filename = "AKJm" #filename to open, change to the conventional

p.openfile(filename, sim)

#main flow starts. click on the first action and read data, write them into excel. needs refactoring
pag.moveTo(mouse_locations["start"])
pag.click()
time.sleep(0.5)
df1, df2 = p.scrape_solve()
p.populate_class(sim, df1, df2)
loc = ew.find_excel_location(filename, sim, ws)
ew.sim_to_excel(loc,sim,ws)

#click on the second action, read, write to excel
pag.moveTo(mouse_locations["bet1"])
pag.click()
time.sleep(0.5)
df1, df2 = p.scrape_solve()
p.populate_class(sim, df1, df2)
loc = loc.offset(column=44) #second batch of data is inserted 44 columns later
ew.sim_to_excel(loc, sim, ws)

#click on second, then third action, write into excel
pag.moveTo(mouse_locations["bet1"])
pag.click()
time.sleep(0.5)
pag.moveTo(mouse_locations["bet1raise"])
pag.click()
df1, df2 = p.scrape_solve()
p.populate_class(sim, df1, df2)
loc = loc.offset(column=44)
ew.sim_to_excel(loc, sim, ws)


wb.save('test.xlsx') #save file

