def check_overlap_in_list_lesson(start1, end1, arr):
    data = {'value': False}
    if not arr:
        return data
    for obj in arr:
        if check_time_overlap(start1, end1, obj.start_time, obj.end_time) is True:
            data['value'] = True
            data['object'] = obj
            break
    return data


def check_time_overlap(start1, end1, start2, end2):
    if end1 < start2 or start1 > end2:
        return False
    return True
