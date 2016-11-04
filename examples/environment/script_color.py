def divide(val, list):
    less = []
    more = []
    for i in list:
        if i['a'] >= val:
            more.append(i)
        else:
            less.append(i)
    return float(len(more))/len(list), more, less