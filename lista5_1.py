import re

# Znacznik czasowy, nazwę hosta, komponent aplikacji i numer PID, opis zdarzenia
# np. Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186
date_pattern = r'^[A-Z][a-z]{2} [0-9]{2} \w{2}:\w{2}:\w{2}'
user_pattern = r'(?<=:\w\w )\w*'
komponent_and_pid_pattern = r'[A-Za-z]+\[\w*]:'
komponent_pattern = r'[A-za-z]+(?=\[\w*]:)'
pid_pattern = r'(?<=\[)\w*(?=]:)'
description_pattern = r'(?<=: )[A-Za-z0-9._ ]+$'
#full_pattern = r''

try: 
    file_path = input()
    file = open(file_path, "r")
    data_lines = [tmp.strip() for tmp in file.readlines()]
    #print(data_lines[0])
    converted_lines = []
    for line in data_lines:
        temp = line.split()
        #(dat, host, component, pid, description) = 
        converted_lines.append((" ".join([str(item) for item in temp[:3:]]), temp[3], temp[4], " ".join([str(item) for item in temp[5::]])))
    print(converted_lines[0])
    #print(str(converted_lines[0]))


except Exception:
    print(Exception.with_traceback())


def to_tuple(line:str):
    result = {
        "date": re.match(date_pattern, line),
        "user": re.match(user_pattern, line),
        "komponent": re.match(komponent_pattern, line),
        "pid": re.match(pid_pattern, line),
        "description": re.match(description_pattern, line)
    }
    return result

