def log_reader():
    with open ('log_calc.txt','r') as file:
        data = file.read()
    return data