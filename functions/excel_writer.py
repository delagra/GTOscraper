import functions.variables as config

def find_excel_location(value, obj, excel):  # calculate where in excel the data will be written
    value = value[0:3]
    print(value)

    colQC = excel[config.twotone_column]  # column that contains all boards, use it as a starting point
    for row in colQC:
        if str(row.value) == value:
            base_loc = row
            print("Base location is", base_loc)
            break
    if obj.is_monotone:
        return base_loc.offset(column=-522) #this many columns between 2tone and monotone boards in excel
    elif obj.is_rainbow:
        try:
            print(base_loc)
        except:
            print("Base_loc not assigned")
        print(f"Trips board?{value[0]==value[1]==value[2]}")
        if value[0] == value[1] == value[2]: #if the board is trips
            colAIR = excel[config.rainbow_column]
            #print(colAIR)
            print(f"board = {value}")
            for row in colAIR:

                if str(row.value) == value:
                    print("Found!")
                    base_loc = row
                    return base_loc.offset(column=1)
            else:
                print("Trips board not found")
        return base_loc.offset(column=484) #this many columns between 2tone and rainbow columns in excel
    elif obj.is_two_tone2:
        return base_loc.offset(column=1, row=1)
    elif obj.is_two_tone3:
        return base_loc.offset(column=1, row=2)
    elif obj.is_ttp:
        return base_loc.offset(column=1)
    else:
        return base_loc.offset(column=1)


def sim_to_excel(base_location, _sim, excel):  # write values into the location in excel
    excel_order = ["first_action"]
    if _sim.is_monotone:
        excel_order.extend(list(config.options_mt.keys()))
    elif _sim.is_rainbow:
        excel_order.extend(list(config.options_r.keys()))
    else:
        excel_order.extend(list(config.options_2t.keys()))
    excel_order.append("combos")

    for idx, val in enumerate(excel_order): #iterating through stats
        curr_combo = getattr(_sim, val)
        # print(curr_combo)

        if curr_combo is not None:
            print("Writing", val)
            for index, value in enumerate(curr_combo): #iterating through numbers inside a stat
                if idx == 0:
                    coeff = 0
                else:
                    coeff = -1
                    if index > 0:
                        value = float(value) / 100
                # print(base_location.offset(column=idx*4+index))
                # print(idx,index, idx*4+index+coeff)
                write_loc = base_location.offset(column=idx * 4 + index + coeff)
                print("Writing", value, "to", write_loc)
                write_loc.value = value
