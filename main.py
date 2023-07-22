import pyautogui as pag
import pandas as pd
import time
import openpyxl as op
import pyperclip
pag.FAILSAFE = False


def scrape_solve():
    #find and click the solver icon
    gto_coord = pag.locateCenterOnScreen('gtoicon.PNG', confidence = 0.9)
    print(gto_coord)
    pag.moveTo(gto_coord)
    pag.click(gto_coord)

    #find and click the combos window
    combos_coord = pag.locateCenterOnScreen('combos.PNG',confidence = 0.9)
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
    df = pd.read_clipboard(sep='\t')
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

def generate_excel():
    wb = op.load_workbook('Example 3-  Test all types of data .xlsx')
    ws = wb.active
    print(ws['B3'].value)
    #print(sheet_ranges)

#generate_excel()

scrape_solve()