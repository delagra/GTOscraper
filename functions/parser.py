import pyautogui as pag
import pandas as pd
import time

mouse_locations = {
    "start": (33,76),
    "bet1": (230,76),
    "bet1raise": (443,76),
    "check": (230,117),
    "action2opt3": (230,137),
    "action3opt2": (443,117),
    "action3opt3": (443,137)
}
def locate_solver():
    gto_coord = pag.locateCenterOnScreen('.\\assets\\gtoicon.PNG', confidence=0.9)
    if gto_coord == None:
        print("Solver not found, run GTO+ and make sure it is maximized before running the program again")
    pag.click(gto_coord)
def scrape_solve():
    #find and click the combos window
    combos_coord = pag.locateCenterOnScreen('.\\assets\\combos.PNG',grayscale=True, confidence = 0.9)
    while combos_coord is None:
        locate_solver()
        time.sleep(0.5)
        combos_coord = pag.locateCenterOnScreen('.\\assets\\combos.PNG', grayscale=True, confidence=0.9)
    print(combos_coord)
    #time.sleep(3)
    #pag.moveTo(combos_coord)
    pag.click(combos_coord)

    #scroll to the end of the window
    scroll_end = pag.locateCenterOnScreen('.\\assets\\scroll_to_end.PNG',confidence = 0.9)
    print(scroll_end)
    for  i in range(20):
        pag.press('end')
    time.sleep(0.5)

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
    ok_loc = pag.locateCenterOnScreen('.\\assets\\ok.PNG', confidence = 0.9)
    pag.click(ok_loc)
    time.sleep(0.5)

    #select the outcomes window, copy everything, paste into dataframe
    ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG', confidence=0.9)
    pag.click(ac_loc)
    pag.keyDown('ctrl')
    time.sleep(0.5)
    pag.press('c')
    pag.keyUp('ctrl')
    bigdf = pd.read_clipboard(sep='\t')
    pag.press('esc')
    pag.moveTo(mouse_locations["start"])
    print(bigdf)
    return df, bigdf

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

def populate_class(_sim,df1, df2): #populate the instance attributes with the values from dataframes
    options = { #values as they are in the class vs as they are in dataframes
        'top_pair': 'top pair',
        'overpair': 'overpair',
        'mid_pair': 'middle pair',
        'ace_high': 'ace high',
        'gutshot': 'gutshot',
        'overcards': 'overcards',
        'nut_fd': 'nut flushdr.',
        'weak_fd': 'weak flushdr.',
        'set': 'set',
        'oesd': 'oesd'
    }
    for key, value in options.items():
        setattr(_sim, key, get_statistic(df2, value))
    setattr(_sim,'first_action', [df1['c'][1],df1['b'][1],df1['d'][1]])
    setattr(_sim,'combos', [df1['b'][0]])

def openfile(file:str, sim_instance): #read the filename and define board structure from it
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
