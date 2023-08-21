import pyautogui as pag
import pandas as pd
import time
import clipboard
from functions import excel_writer as ew
import functions.variables as config


def locate_solver():
    gto_coord = pag.locateCenterOnScreen('.\\assets\\gtoicon.PNG', confidence=0.9)
    # gto_coord = pag.locateCenterOnScreen('.\\assets\\gtoicon.PNG')
    if gto_coord is None:
        print("Solver not found, run GTO+ and make sure it is maximized before running the program again")
    pag.click(gto_coord)
    time.sleep(config.delay_time)
    pag.moveTo(config.mouse_locations["start"])
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
    pag.press('esc')
    time.sleep(config.delay_time)

    # select the outcomes window, copy everything, paste into dataframe
    ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG', confidence=0.9)
    # ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG')
    if ac_loc is None:
        time.sleep(config.delay_time)
        ac_loc = pag.locateCenterOnScreen('.\\assets\\all_combos.PNG', confidence=0.9)

    # ac_loc = (1363,234)
    pag.click(ac_loc)
    pag.keyDown('ctrl')
    time.sleep(config.delay_time)
    pag.press('c')
    pag.keyUp('ctrl')
    bigdf = pd.read_clipboard(sep='\t')
    pag.press('esc')
    pag.moveTo(config.mouse_locations["start"])
    print(bigdf)
    return df, bigdf


def get_statistic(_df, stat):
    try:
        if (stat == 'set') and (len(_df[_df['Statistic'] == stat]) == 0):  # special case to handle 3oac/set
            stat = '3 of a kind'
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
        options = config.options_mt
    else:
        options = config.options_2t
    for key, value in options.items():
        setattr(_sim, key, get_statistic(df2, value))
    fa = [df1['d'][1], df1['c'][1], df1['b'][1]]
    fa_clean = [item for item in fa if
                not (pd.isnull(item)) is True]  # if there is a nan, drop it, when only 1 bet size
    setattr(_sim, 'first_action', fa_clean)
    setattr(_sim, 'combos', [df1['b'][0]])


def openfile(filename: str, sim_instance):  # read the filename and define board structure from it
    file = filename[-6:]
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
    time.sleep(config.delay_time)
    pag.write(filename)
    pag.press('enter')
    pag.sleep(config.delay_time)
    pag.press('n')


def capture_and_write(screen_loc, excel_loc, sim, ws):
    pag.moveTo(config.mouse_locations[screen_loc])
    pag.click()
    time.sleep(config.delay_time)
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    ew.sim_to_excel(excel_loc, sim, ws)


def process_sim(filename, sim, ws):
    # main flow starts. click on the first action and read data, write them into excel. needs refactoring
    global donk_mode
    pag.moveTo(config.mouse_locations["start"])
    pag.click()
    time.sleep(config.delay_time)
    df1, df2 = scrape_solve()
    populate_class(sim, df1, df2)
    if sim.is_monotone:
        columnoffset = 52  # extra columns = flush, 2 pair
    elif sim.is_rainbow:
        columnoffset = 44  # no flush draw, added 2 pair
    else:
        columnoffset = 48  # added 2 pair
    loc = ew.find_excel_location(filename, sim, ws)
    print("Excel write location is", loc)
    ew.sim_to_excel(loc, sim, ws)

    if donk_mode:
        actions = config.donk_actions
    else:
        actions = config.normal_actions
    for screen_loc, offset in actions:
        if offset in [3,5]: #return to start for actions 3 and 5
            pag.moveTo(config.mouse_locations["start"])
            pag.click()
            time.sleep(config.delay_time)
        if offset == 8: #return to bet 1 for action 8
            pag.moveTo(config.mouse_locations["col2top"])
            pag.click()
            time.sleep(config.delay_time)
        print(f"offset:{offset}, column offset: {columnoffset}")
        capture_and_write(screen_loc, loc.offset(column=offset * columnoffset), sim, ws)

