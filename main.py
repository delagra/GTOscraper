import pyautogui as pag
import pandas as pd
import time
import openpyxl as op
import pyperclip
pag.FAILSAFE = False

def locate_solver():
    gto_coord = pag.locateCenterOnScreen('gtoicon.PNG', confidence=0.9)
    if gto_coord == None:
        print("Solver not found, run GTO+ and make sure it is maximized before running the program again")
    pag.click(gto_coord)
def scrape_solve():
    #find and click the solver icon


    #find and click the combos window
    combos_coord = pag.locateCenterOnScreen('combos.PNG',grayscale=True, confidence = 0.9)
    while combos_coord is None:
        locate_solver()
        time.sleep(1)
        combos_coord = pag.locateCenterOnScreen('combos.PNG', grayscale=True, confidence=0.9)
    print(combos_coord)
    #time.sleep(3)
    #pag.moveTo(combos_coord)
    pag.click(combos_coord)

    #scroll to the end of the window
    scroll_end = pag.locateCenterOnScreen('scroll_to_end.PNG',confidence = 0.9)
    print(scroll_end)
    for  i in range(20):
        pag.press('end')
    time.sleep(1)

    #select the bottom lines, copy, paste them into pandas dataframe
    pag.keyDown('shift')
    for i in range(6):
       pag.press('up')
    pag.keyUp('shift')
    pag.keyDown('ctrl')
    pag.press('c')
    pag.keyUp('ctrl')
    df = pd.read_clipboard(sep='\t', names=["a", "b", "c", "d", "e"])
    print(df)
    ok_loc = pag.locateCenterOnScreen('ok.PNG',confidence = 0.9)
    pag.click(ok_loc)

    #select the outcomes window, copy everything, paste into dataframe
    ac_loc = pag.locateCenterOnScreen('all_combos.PNG', confidence=0.9)
    pag.click(ac_loc)
    pag.keyDown('ctrl')
    time.sleep(1)
    pag.press('c')
    pag.keyUp('ctrl')
    bigdf = pd.read_clipboard(sep='\t')
    pag.press('esc')
    print(bigdf)
    return df, bigdf

wb = op.load_workbook('expanded template.xlsx')
ws = wb.active

    #print(sheet_ranges)

def get_statistic(_df,stat):
    try:
        calc = _df[_df['Statistic']==stat].values[0][1:5]
    except IndexError:
        print(stat,"not found")
        return
    output = [round(calc[0])]
    for val in calc[1:]:
        if not pd.isna(val):
            output.append(round(val/calc[0]*100))
        else:
            output.append(val)
    return output

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

def populate_class(_sim,df1, df2):
    options = {
        'top_pair': 'top pair',
        'overpair': 'overpair',
        'mid_pair': 'middle pair',
        'ace_high': 'ace high',
        'gutshot': 'gutshot',
        'overcards': 'overcards',
        'nut_fd': 'nut flushdr.',
        'weak_fd': 'weak flushdr.',
        'set': 'sets',
        'oesd': 'oesd'
    }
    for key, value in options.items():
        setattr(_sim, key, get_statistic(df2, value))
    setattr(_sim,'first_action', [df1['c'][1],df1['b'][1]])
    setattr(_sim,'combos', [df1['b'][0]])
    '''
    setattr(_sim, 'top_pair', get_statistic(df2,'top pair'))
    setattr(_sim, 'overpair', get_statistic(df2, 'overpair'))
    setattr(_sim, 'mid_pair', get_statistic(df2, 'middle pair'))
    setattr(_sim, 'ace_high', get_statistic(df2, 'ace high'))
    setattr(_sim, 'gutshot', get_statistic(df2, 'gutshot'))
    setattr(_sim, 'overcards', get_statistic(df2, 'overcards'))
    setattr(_sim, 'nut_fd', get_statistic(df2, 'nut flushdr.'))
    setattr(_sim, 'weak_fd', get_statistic(df2, 'weak flushdr.'))
    setattr(_sim, 'set', get_statistic(df2, 'sets'))
    setattr(_sim, 'oesd', get_statistic(df2, 'oesd'))
    '''

def openfile(file:str, sim_instance):
    if "m" in file:
        setattr(sim_instance, 'is_monotone', True)
    if "-1" in file:
        setattr(sim_instance, 'is_two_tone1', True)
    if "-2" in file:
        setattr(sim_instance, 'is_two_tone2', True)
    if "-3" in file:
        setattr(sim_instance, 'is_two_tone3', True)
    if "r" in file:
        setattr(sim_instance, "is_rainbow", True)

    locate_solver()
    pag.keyDown('ctrl')
    pag.press('o')
    pag.keyUp('ctrl')
    time.sleep(1)
    pag.write(file+".gto")
    pag.press('enter')


def find_excel_location(value,obj,excel):
    colQC = excel['QC']
    for row in colQC:
        if row.value == value:
            base_loc = row
    if obj.is_monotone:
        return base_loc.offset(column=-442)
    elif obj.is_rainbow:
        return base_loc.offset(column=444)
    elif obj.is_two_tone2:
        return base_loc.offset(column=1, row=1)
    elif obj.is_two_tone3:
        return base_loc.offset(column=1, row=2)
    else:
        return base_loc.offset(column=1)


def sim_to_excel(base_location,_sim, excel):
    excel_order = [
        "first_action",
        "overpair",
        "top_pair",
        "mid_pair",
        "ace_high",
        "gutshot",
        "oesd",
        "overcards",
        "nut_fd",
        "weak_fd",
        "sets",
        "combos"
    ]
    for idx, val in enumerate(excel_order):
        curr_combo = getattr(_sim, val)
        print(curr_combo)
        if curr_combo is not None:
            for index, value in enumerate(curr_combo):
                print(index,idx,value)
                base_location.offset(column=index*idx).value = value








#generate_excel()
#openfile("998r",sim)


sim = Sim
openfile("998r", sim)
df1, df2 = scrape_solve()
populate_class(sim, df1, df2)
print(sim.nut_fd)
print(sim.combos, sim.first_action)

loc = find_excel_location('AAK', sim, ws)
print(loc)
sim_to_excel(loc,sim,ws)
wb.save('test.xslx')
'''
df1, df2 = scrape_solve()
df2.to_csv('gto.csv')

#openfile("akqm")
'''


