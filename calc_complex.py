from datetime import datetime
def calc_complex_main(string):
    a, move, b = string.split()

    a, b = complex(a), complex(b)
    if move == '*':
        result = a * b
    elif move == '/':
        result = a / b
    elif move == '+':
        result = a + b
    elif move == '-':
        result = a - b
    else:
        return 'вы ввели некорректные данные'
    with open ('log_calc.txt','a') as output_file:
        data = datetime.now().strftime('%Y.%m.%d %H:%M:%S  ')
        output_file.writelines(f'{data} {a} {move} {b} = {result}\n')
    return f'Результат равен {result}'