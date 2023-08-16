import pyautogui as pag
import openpyxl as op
import sys
import asyncio

from functions import parser as p, sim_runner as sr


pag.FAILSAFE = False

wb = op.load_workbook('Simulation Template v2.xlsx')
ws = wb.active
output_file = 'test.xlsx'

prefix = ws['D3'] #read file renaming prefix from excel

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
    flush = []
    combos = []

def save_excel(filename):
    wb.save(filename)
#p.process_sim(filename, sim, ws)
async def async_save(filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_excel, filename)

sims_to_process = (sr.read_sim_status_list())
sim_files = (sr.get_sim_files('./sims'))
sr.rename_sim_files(sim_files, 'vs BB ')
sim_files = (sr.get_sim_files('./sims'))
print("Syncing available sims with the status file")
for sim_file in sim_files:
    if sim_file not in sims_to_process:
        sims_to_process[sim_file] = "Solved"
        print("Sim file", sim_file, "exists but not marked as solved, updating status file")
dict2sort = list(sims_to_process.keys())
dict2sort.sort()
simslist_sorted = {i: sims_to_process[i] for i in dict2sort}
sr.write_sim_status_list(simslist_sorted)
print(sims_to_process)

p.locate_solver()


for filename in sims_to_process:
    try:
        if sims_to_process[filename] == "Processed":
            continue
        sim = Sim
        p.openfile(filename, sim)
        trunc_filename = sr.parse_filename(filename)
        print("Processing", trunc_filename)

        p.process_sim(trunc_filename, sim, ws)
        sims_to_process[filename] = "Processed"
        print(filename, "processed")
        sr.write_sim_status_list(sims_to_process)
    except:
        print("There was an error, saving current progress")
        wb.save(output_file)

wb.save(output_file)




