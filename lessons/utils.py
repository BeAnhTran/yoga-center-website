def check_overlap_in_list_lesson(start1, end1, arr):
    data = {'value':True}
    if not arr:
        return data
    for obj in arr:
        if check_time_overlap(start1, end1, obj.start_time, obj.end_time) is False:
            data['value'] = False
            data['object'] = obj
            break
    return data


def check_time_overlap(start1, end1, start2, end2):
    if end1 < start2 or start1 > end2:
        return True
    return False
