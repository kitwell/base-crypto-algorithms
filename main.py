# функция, собирающая входные данные для всех алгоритмов шифрования
def start(num):
    if num > 4:
        return 'такого номера нет!'
    action = input('Введите действие (encrypt / decrypt) --> ')
    alphabet = alph(input('Введите язык сообщения (rus / en) --> '))
    message = input('Введите сообщение --> ').strip()
    if num == 1:
        return caesar(message, alphabet, action)
    elif num == 2:
        return affine(message, alphabet, action)
    elif num == 3:
        return caesar_with_keyword(message, alphabet, action)
    else:
        return trisemus(message, alphabet, action)


# функция выбора алфавита
def alph(language):
    alph_rus = 'аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ'
    alph_en = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
    if language == 'rus':
        return alph_rus
    else:
        return alph_en


# функция для определения взаимно простых чисел
def is_inter_primes(length, key):
    if key == length:
        return False
    for div in range(2, length // 2 + 1):
        if length % div == 0 and key % div == 0:
            return False
    return True


# функция, находящая ключ для расшифровки аффинной подстановкой
def inverter(key, length):
    for i in range(1, length):
        if key * i % length == 1:
            return i


# функция, вставляющая в алфавит ключевую фразу
def new_alph(alphbt, keyword, key, length):
    for sub in keyword:
        keyword = keyword.replace(sub, sub + sub.upper())
        alphbt = alphbt.replace(sub, '').replace(sub.upper(), '')
    if key != 0:
        new_alphbt = alphbt[-key:] + keyword[:length - key] + alphbt[:-key]
        keyword = keyword.replace(keyword[:length - key], '')  # остаётся часть слова, не вместившаяся в алфавит
        new_alphbt = keyword + new_alphbt  # этот остаток добавляется в начало
    else:
        new_alphbt = keyword + alphbt
    return new_alphbt


# функция, удаляющая одинаковые символы из строчки
def del_same_subs(phrase):
    new_phrase = ''
    for sub in phrase:
        if sub not in new_phrase:
            new_phrase += sub
    return new_phrase


# функция, создающая таблицу Трисемуса
def tris_table(rows, columns, alphbt, keyword, length):
    table_size = rows * columns
    for sub in keyword:
        keyword = keyword.replace(sub, sub + sub.upper())
        alphbt = alphbt.replace(sub, '').replace(sub.upper(), '')
    new_alphbt = keyword + alphbt
    if table_size == length:
        table = [new_alphbt[columns * i * 2: columns * (i + 1) * 2] for i in range(rows)]  # * 2 - есть прописные буквы
        new_subs = ''
    else:
        table = [new_alphbt[columns * i * 2: columns * (i + 1) * 2] for i in range(rows)]
        new_subs = input(f'Введите дополнительные символы ({table_size - length}) для зашифровки --> ')
        for sub in new_subs:
            table[-1] += sub + sub.upper()
    print('\nШифрующая таблица:', '-' * columns * 2, sep='\n')
    [print(*el[0::2]) for el in table]
    print('-' * columns * 2)
    return table, new_subs


# функция, кодирующая/декодирующая по шифру Цезарю
def caesar(msge, alphbt, act):
    length_alph = len(alphbt)
    key = int(input('Введите ключ --> ')) * 2 % length_alph  # остаток от деления для цикличности алфавита
    if act == 'encrypt':
        encryption = ''
        for char in msge:
            if char in alphbt:
                index = alphbt.find(char)
                encryption += alphbt[(index + key) % length_alph]  # остаток от деления для цикличности алфавита
            else:
                encryption += char
        return encryption
    else:
        decryption = ''
        for char in msge:
            if char in alphbt:
                index = alphbt.find(char)
                decryption += alphbt[(index - key) % length_alph]
            else:
                decryption += char
        return decryption


# функция, кодирующая/декодирующая по аффинной подстановке Цезаря
def affine(msge, alphbt, act):
    length_alph = len(alphbt) // 2  # алфавит в два раза больше за счёт наличия прописных букв
    key1 = int(input('Введите первый ключ --> '))
    while not is_inter_primes(length_alph, key1):
        print(f'Длина алфавита ({length_alph}) и ключ должны быть взаимно простыми!')
        key1 = int(input('Введите первый ключ --> '))
    key2 = int(input('Введите второй ключ --> '))
    if act == 'encrypt':
        encryption = ''
        for char in msge:
            if char in alphbt:
                index = alphbt.find(char)
                if index % 2 == 0:
                    new_index = (key1 * (index // 2) + key2) % length_alph * 2  # для строчных букв
                else:
                    new_index = (key1 * (index // 2) + key2) % length_alph * 2 + 1  # для прописных букв
                encryption += alphbt[new_index]
            else:
                encryption += char
        return encryption
    else:
        decryption = ''
        decrypt_key1 = inverter(key1, length_alph)
        for char in msge:
            if char in alphbt:
                index = alphbt.find(char)
                if index % 2 == 0:
                    new_index = decrypt_key1 * (index // 2 + length_alph - key2) % length_alph * 2
                else:
                    new_index = decrypt_key1 * (index // 2 + length_alph - key2) % length_alph * 2 + 1
                decryption += alphbt[new_index]
            else:
                decryption += char
        return decryption


# функция, кодирующая/декодирующая по шифру Цезарю с ключевым словом
def caesar_with_keyword(msge, alphbt, act):
    length_alph = len(alphbt)
    key = int(input('Введите ключ --> ')) * 2 % length_alph  # остаток от деления для цикличности алфавита
    keyword = del_same_subs(input('Введите ключевую фразу --> ').replace(' ', '').lower())
    new_alphbt = new_alph(alphbt, keyword, key, length_alph)
    if act == 'encrypt':
        encryption = ''
        for char in msge:
            if char in alphbt:
                index = alphbt.find(char)
                encryption += new_alphbt[index]
            else:
                encryption += char
        return encryption
    else:
        decryption = ''
        for char in msge:
            if char in new_alphbt:
                index = new_alphbt.find(char)
                decryption += alphbt[index]
            else:
                decryption += char
        return decryption


# функция, кодирующая/декодирующая по шифрующей таблице Трисемуса
def trisemus(msge, alphbt, act):
    length_alph = len(alphbt) // 2  # алфавит в два раза больше за счёт наличия прописных букв
    rows = int(input('Введите число строк шифрующей таблицы --> '))
    columns = int(input('Введите число столбцов шифрующей таблицы --> '))
    while rows * columns < length_alph:
        print(f'Таблица не должна быть меньше длины алфавита ({length_alph})!')
        rows = int(input('Введите число строк шифрующей таблицы --> '))
        columns = int(input('Введите число столбцов шифрующей таблицы --> '))
    keyword = del_same_subs(input('Введите ключевую фразу --> ').replace(' ', '').lower())
    table, new_subs = tris_table(rows, columns, alphbt, keyword, length_alph)
    alphbt += new_subs  # добавляем новые символы к алфавиту, если оин есть
    if act == 'encrypt':
        encryption = ''
        for char in msge:
            if char in alphbt:
                for i in range(rows):
                    if char in table[i]:
                        index = table[i].find(char)
                        encryption += table[(i + 1) % rows][index]
                        break
            else:
                encryption += char
        return encryption
    else:
        decryption = ''
        for char in msge:
            if char in alphbt:
                for i in range(rows):
                    if char in table[i]:
                        index = table[i].find(char)
                        decryption += table[(i - 1) % rows][index]
                        break
            else:
                decryption += char
        return decryption


print('~' * 37)
print('0. Выход из программы')
print('1. Шифр Цезаря')
print('2. Аффинная подстановка Цезаря')
print('3. Шифр Цезаря с ключевым словом')
print('4. Система шифрования Трисемуса')
print('~' * 37)

cipher = int(input('Введите порядковый номер шифра --> '))
while cipher != 0:
    print('\nРезультат:', start(cipher), end='\n\n')
    cipher = int(input('Введите порядковый номер шифра --> '))
