import pyautogui as pag
import pandas as pd
import time
import clipboard
from functions import excel_writer as ew
from functions.variables import mouse_locations, options_mt, options_2t

delay_time = 0.1

def locate_solver():
    gto_coord = pag.locateCenterOnScreen('.\\assets\\gtoicon.PNG', confidence=0.9)
    # gto_coord = pag.locateCenterOnScreen('.\\assets\\gtoicon.PNG')
    if gto_coord is None:
        print("Solver not found, run GTO+ and make sure it is maximized before running the program again")
    pag.click(gto_coord)
    time.sleep(delay_time)
    pag.moveTo(mouse_locations["start"])
    pag.click()


def scrape_solve():
    pag.keyDown('ctrl')
    pag.keyDown('alt')
    pag.press('o')
    pag.keyUp('ctrl')
    pag.keyUp('alt')
    pag.keyDown('ctrl')
    pag.press('c')
    pag.keyUp('ctrl')
    txt = clipboard.paste()
    cut = txt.index('Combos:')
    new = txt[cut:]
    clipboard.copy(new)
    df = pd.read_clipboard(sep='\t', names=["a", "b", "c", "d", "e"])
    # print(df)
    # ok_loc = pag.locateCenterOnScreen('.\\assets\\ok.PNG', confidence=0.9)
    # ok_loc = pag.locateCenterOnScreen('.\\assets\\ok.PNG')
    # pag.click(ok_loc)
    pag.press('esc')
    time.sleep(delay_time)

    # select the outcomes window, copy everything, paste into dataframe
    ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG', confidence=0.9)
    # ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG')
    if ac_loc is None:
        time.sleep(delay_time)
        ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG', confidence=0.9)

    # ac_loc = (1363,234)
    pag.click(ac_loc)
    pag.keyDown('ctrl')
    time.sleep(delay_time)
    pag.press('c')
    pag.keyUp('ctrl')
    bigdf = pd.read_clipboard(sep='\t')
    pag.press('esc')
    pag.moveTo(mouse_locations["start"])
    print(bigdf)
    return df, bigdf


def get_statistic(_df, stat):
    try:
        calc = _df[_df['Statistic'] == stat].values[0][1:5]
    except IndexError:
        print(stat, "not found")
        return
    output = [round(calc[0])]
    for val in calc[1:]:
        if not pd.isna(val):
            if calc[0] == 0:
                output.append(0)
            else:
                output.append(round(val / calc[0] * 100))
        else:
            output.append(val)
    return output


def populate_class(_sim, df1, df2):  # populate the instance attributes with the values from dataframes

    if _sim.is_monotone:
        options = options_mt
    else:
        options = options_2t
    for key, value in options.items():
        setattr(_sim, key, get_statistic(df2, value))
    fa = [df1['d'][1], df1['c'][1], df1['b'][1]]
    fa_clean = [item for item in fa if
                not (pd.isnull(item)) is True]  # if there is a nan, drop it, when only 1 bet size
    setattr(_sim, 'first_action', fa_clean)
    setattr(_sim, 'combos', [df1['b'][0]])


def openfile(file: str, sim_instance):  # read the filename and define board structure from it
    if "m" in file:
        setattr(sim_instance, 'is_monotone', True)
    if "-1" in file:
        setattr(sim_instance, 'is_two_tone1', True)
    if "-2" in file:
        setattr(sim_instance, 'is_two_tone2', True)
    if "-3" in file:
        setattr(sim_instance, 'is_two_tone3', True)
    if "s" in file:
        setattr(sim_instance, 'is_ttp', True)
    if "r" in file:
        setattr(sim_instance, "is_rainbow", True)

    pag.keyDown('ctrl')
    pag.press('o')
    pag.keyUp('ctrl')
    time.sleep(delay_time)
    pag.write(file)
    pag.press('enter')
    pag.sleep(delay_time)
    pag.press('n')


def process_sim(filename, sim, ws):
    # main flow starts. click on the first action and read data, write them into excel. needs refactoring
    pag.moveTo(mouse_locations["start"])
    pag.click()
    time.sleep(delay_time)
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    if sim.is_monotone:
        columnoffset = 48  # extra column = flush
    elif sim.is_rainbow:
        columnoffset = 40  # no flush draw
    else:
        columnoffset = 44
    loc = ew.find_excel_location(filename, sim, ws)
    print("Excel write location is", loc)
    ew.sim_to_excel(loc, sim, ws)

    # click on the second action, read, write to excel : bet 1
    pag.moveTo(mouse_locations["bet1"])
    pag.click()
    time.sleep(delay_time)
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)  # second batch of data is inserted 44 columns later
    ew.sim_to_excel(loc, sim, ws)

    # click on second, then third action (raise), write into excel bet 1 raise
    ##pag.moveTo(mouse_locations["bet1"])
    # pag.click()
    time.sleep(delay_time)
    pag.moveTo(mouse_locations["bet1raise"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)
    ew.sim_to_excel(loc, sim, ws)

    # click on first, then check (2nd tree branch)
    pag.moveTo(mouse_locations["start"])
    pag.click()
    time.sleep(delay_time)
    pag.moveTo(mouse_locations["check"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset * 3)
    ew.sim_to_excel(loc, sim, ws)

    # click on the second action, read, write to excel :check, bet1
    pag.moveTo(mouse_locations["action3opt3"])
    pag.click()
    time.sleep(delay_time)
    pag.moveTo(mouse_locations["bet1raise"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)
    ew.sim_to_excel(loc, sim, ws)

    # check, bet1, raise
    # pag.moveTo(mouse_locations["bet1"])
    # pag.click()
    time.sleep(delay_time)
    # time.sleep(0.5)
    pag.moveTo(mouse_locations["checkbetraise"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)
    ew.sim_to_excel(loc, sim, ws)

    # check, bet2
    pag.moveTo(mouse_locations["bet1"])
    pag.click()
    time.sleep(delay_time)
    # time.sleep(0.5)
    pag.moveTo(mouse_locations["bet1"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)
    ew.sim_to_excel(loc, sim, ws)

    # check, bet2, raise
    pag.moveTo(mouse_locations["checkbetraise"])
    pag.click()
    #  time.sleep(0.5)
    # time.sleep(0.5)
    # pag.moveTo(mouse_locations["action3opt2"])
    pag.click()
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    loc = loc.offset(column=columnoffset)
    ew.sim_to_excel(loc, sim, ws)
