import re, logging, sys, random, datetime, statistics

# 2a
def to_dict(line:str):
    # Znacznik czasowy, nazwę hosta, komponent aplikacji i numer PID, opis zdarzenia (w tym user)
    # np. Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186
    date_pattern = r'^[A-Z][a-z]{2} {1,2}[0-9]{1,2} \w{2}:\w{2}:\w{2}'
    user_pattern = r'(?<=user )\w*|(?<= user=)\w*|(?<=Failed password for )\w*|(?<=Accepted password for )\w*' 
    #komponent_and_pid_pattern = r'[A-Za-z]+\[\w*]:'
    komponent_pattern = r'[A-za-z]+(?=\[\w*]:)'
    pid_pattern = r'(?<=\[)\w*(?=]:)'
    description_pattern = r'(?<=: ).*$'
    #temp = copy.deepcopy(line)
    temp = line
    result = {
        "date": re.search(date_pattern, line).group(0),
        "user": "",
        "komponent": re.search(komponent_pattern, line).group(0),
        "pid": re.search(pid_pattern, line).group(0),
        "description": re.search(description_pattern, line).group(0)
    }
    if(re.search(user_pattern, line)): result["user"] = re.search(user_pattern, line).group(0)
    #print(result)
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
    login_successful_pattern = r'Accepted password for' #?
    login_failed_pattern = r'authentication failure'
    connection_closed = r'^Connection closed|^Received disconnect'
    wrong_password = r'^Failed password for'
    wrong_username = r'^Invalid user'
    breach_attempt = r'POSSIBLE BREAK-IN ATTEMPT!'
    if(re.search(string=desc, pattern=breach_attempt)): return "breach attempt"
    elif(re.search(string=desc, pattern=wrong_username)): return "wrong username"
    elif(re.search(string=desc, pattern=wrong_password)): return "wrong password"
    elif(re.search(string=desc, pattern=connection_closed)): return "connection closed"
    elif(re.search(string=desc, pattern=login_failed_pattern)): return "login failed"
    elif(re.search(string=desc, pattern=login_successful_pattern)): return "login successful"
    else: return "other"

# 4a
def rand_logs(data:list, n:int):
    user_logs = {}
    users = []

    for line in data:
        temp_dict = to_dict(line)
        temp_user = get_user_from_log(temp_dict)
        if(temp_user==""):continue
        if(user_logs.get(temp_user)):
            user_logs.get(temp_user).append(line)
        else:
            user_logs[temp_user]=[line]
            users.append(temp_user)

    user = users[int(random.random()*len(users))] 
    logs = []

    for i in user_logs.get(user):
        logs.append(i)

    if(len(logs)>n):
        for j in logs:
            if(random.random()>=0.5 and len(logs)>n):
                logs.remove(j)
            elif(len(logs)<=n):
                break
    return logs


# 4b
def log_stat(data:list):
    user_logs = {}  # "user": [(start, end), (start, end)]
    user_ip = {}    # "ip": "user"
    users = []
    logged = {}
    for line in data:
        temp_dict = to_dict(line)
        temp_ip = get_ipv4s_from_log(temp_dict)[0]
        temp_user = get_user_from_log(temp_dict)
        #dt.datetime.strptime(temp, '%d/%b/%Y').strftime('%a')=="Fri"
        date = datetime.datetime.strptime(temp_dict.get("date"))
        if(not logged.get(temp_ip)): 
            logged[temp_ip]=True
            user_ip[temp_ip]=temp_user
            if(not users.__contains__(temp_user)):users.append(temp_user)

        if(temp_user==""):continue

        if(user_logs.get(temp_user)):
            user_logs[temp_user].append(line)
        else:
            user_logs[temp_user]=[line]
            users.append(temp_user)

    #TODO
    pass

# 4c
def log_user_frequency(data:list):
    user_logs = {}
    for line in data:
        temp_dict = to_dict(line)
        temp_user = get_user_from_log(temp_dict)
        #if(temp_user==""):continue
        temp_type = get_message_type(temp_dict.get("description"))
        #print(temp_type, temp_user, temp_dict)
        if(temp_type == "login successful" or temp_type == "login failed"):
            if(user_logs.get(temp_user)):
                user_logs[temp_user]+=1
            else:
                user_logs[temp_user]=1
    
    #print(user_logs)
    user_max = ""
    count_max = -1
    user_min = ""
    count_min = 99999999

    for key in user_logs:
        temp = user_logs.get(key)
        if(temp>count_max):
            count_max=temp
            user_max=key
        if(temp<count_min):
            count_min=temp
            user_min=key
    
    print("most frequent user: ", user_max, " least frequent user: ", user_min)

# 1
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
        print(line)
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
    
    print(rand_logs(data_lines, 2))
    log_user_frequency(data_lines)



except Exception:
    print(Exception.with_traceback())