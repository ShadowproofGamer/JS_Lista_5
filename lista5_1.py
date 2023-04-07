import re, copy

# 2a
def to_dict(line:str):
    # Znacznik czasowy, nazwę hosta, komponent aplikacji i numer PID, opis zdarzenia
    # np. Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186
    date_pattern = r'^[A-Z][a-z]{2} [0-9]{2} \w{2}:\w{2}:\w{2}'
    user_pattern = r'(?<=:\w\w )\w*'
    #komponent_and_pid_pattern = r'[A-Za-z]+\[\w*]:'
    komponent_pattern = r'[A-za-z]+(?=\[\w*]:)'
    pid_pattern = r'(?<=\[)\w*(?=]:)'
    description_pattern = r'(?<=: ).*$'
    #temp = copy.deepcopy(line)
    temp = line
    result = {
        "date": re.search(date_pattern, line).group(0),
        "user": re.search(user_pattern, line).group(0),
        "komponent": re.search(komponent_pattern, line).group(0),
        "pid": re.search(pid_pattern, line).group(0),
        "description": re.search(description_pattern, line).group(0)
    }
    
    return result

# 2b
def get_ipv4s_from_log(log:dict):
    description = log.get("description")
    ipv4_pattern = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    result = re.findall(ipv4_pattern, description)
    return result

# 2c
def get_user_from_log(log:dict):
    return log.get("user")


try: 
    file_path = input()
    file = open(file_path, "r")
    data_lines = [tmp.strip() for tmp in file.readlines()]
    for line in data_lines:
        #print(line)
        newl = to_dict(line)
        #print(newl)
        #print(get_ipv4s_from_log(newl))
        #print(get_user_from_log(newl))
        #print("\n")
        pass


except Exception:
    print(Exception.with_traceback())