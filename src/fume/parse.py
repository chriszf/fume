def break_line(line):
    space = line.find(" ")
    if space == -1:
        command = line.strip().lower()
        rest = ""
    else:
        command = line[:space].strip().lower()
        rest = line[space:].strip()
    return command, rest
