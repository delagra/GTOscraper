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
    locate_solver()

    #find and click the combos window
    combos_coord = pag.locateCenterOnScreen('combos.PNG',grayscale=True, confidence = 0.9)
    while combos_coord is None:
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
    print(bigdf)
    return df, bigdf

def generate_excel():
    wb = op.load_workbook('Example 3-  Test all types of data .xlsx')
    ws = wb.active
    print(ws['B3'].value)
    #print(sheet_ranges)

class Sim: #class that will contain all sim results to be populated in excel later
    def __init__(self, board):
        self.board = board
    def is_monotone(self):
        if self.board[1] == self.board[3] == self.board[5]:
            return True
        else:
            return False
    def is_twotone(self):
        if self.board[1] == self.board[3] or self.board[1] == self.board[5] or self.board[3] == self.board[5]:
            return True
        else:
            return False
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
    setattr(_sim, 'combos', [df1['c'][0],df1['d'][0],df1['e'][0]])

def openfile(file:str):
    locate_solver()
    pag.keyDown('ctrl')
    pag.press('o')
    pag.keyUp('ctrl')
    time.sleep(1)
    pag.write(file+".gto")
    pag.press('enter')





sheet_locations = {"monotone": "c2", "twotone1":"f2","twotone2": "x2","twotone3":"x6","rainbow":"aio1"}

#generate_excel()
'''
df1, df2 = scrape_solve()
sim = Sim
populate_class(sim,df1,df2)
print(sim.combos)
'''
df1, df2 = scrape_solve()
df2.to_csv('gto.csv')
#openfile("akqm")