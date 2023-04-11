import re, logging, sys

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

# 2d
def get_message_type(desc:str):
    login_successful_pattern = r'check pass' #?
    login_failed_pattern = r'authentication failure'
    connection_closed = r'^Connection closed|^Received disconnect'
    wrong_password = r'^Failed password'
    wrong_username = r'^Invalid user'
    breach_attempt = r'POSSIBLE BREAK-IN ATTEMPT!'
    if(re.search(string=desc, pattern=breach_attempt)): return "breach attempt"
    elif(re.search(string=desc, pattern=wrong_username)): return "wrong username"
    elif(re.search(string=desc, pattern=wrong_password)): return "wrong password"
    elif(re.search(string=desc, pattern=connection_closed)): return "connection closed"
    elif(re.search(string=desc, pattern=login_failed_pattern)): return "login failed"
    elif(re.search(string=desc, pattern=login_successful_pattern)): return "login successful"
    else: return "other"



try: 
    file_path = input()
    file = open(file_path, "r")
    data_lines = [tmp.strip() for tmp in file.readlines()]

    # 3
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, encoding='utf-8')
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, encoding='utf-8')
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout, encoding='utf-8')
    logging.basicConfig(level=logging.ERROR, stream=sys.stderr, encoding='utf-8')
    logging.basicConfig(level=logging.CRITICAL, stream=sys.stderr, encoding='utf-8')

    for line in data_lines:
        #print(line)
        newl = to_dict(line)
        print(newl)
        print(get_ipv4s_from_log(newl))
        print(get_user_from_log(newl))
        #
        type = get_message_type(newl.get("description"))
        
        logging.debug(len(line))
        if(type == "login successful" or type == "connection closed"): logging.info(type)
        elif(type == "login failed"): logging.warning(type)
        elif(type == "wrong username" or type == "wrong password"): logging.error(type)
        elif(type == "breach attempt"): logging.critical(type)
        print("\n")
        pass


except Exception:
    print(Exception.with_traceback())