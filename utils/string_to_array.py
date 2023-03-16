def convert(raw_string):
    start = '['
    end = ']'

    data = raw_string[raw_string.index(start)+1:raw_string.index(end)]

    unlocks = [unlock[1:-1] for unlock in data.split(', ')]

    return unlocks
