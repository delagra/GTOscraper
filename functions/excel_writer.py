
def find_excel_location(value,obj,excel): #calculate where in excel the data will be written
    value = value[0:3]

    colQC = excel['QC'] #column that contains all boards, use it as a starting point
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


def sim_to_excel(base_location,_sim, excel): #write values into the location in excel
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
                if idx == 0:
                    coeff = 0
                else:
                    coeff = -1
                #print(base_location.offset(column=idx*4+index))
                #print(idx,index, idx*4+index+coeff)
                base_location.offset(column=idx*4+index+coeff).value = value
