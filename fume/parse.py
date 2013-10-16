def break_line(line):
    space = line.find(" ")
    command = line[:space].strip().lower()
    rest = line[space:].strip()
    return command, rest
