import json
import pyaudio
import os
import webbrowser
from vosk import Model, KaldiRecognizer

model = Model('small_model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


def number_detect(a):
    words_to_numbers = {
        'один': 1,
        'одна': 1,
        'две': 2,
        'два': 2,
        'три': 3,
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одиннадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20,
        'тридцать': 30,
        'сорок': 40,
        'пятьдесят': 50,
        'шестьдесят': 60,
        'семьдесят': 70,
        'восемьдесят': 80,
        'девяносто': 90,
        'сто': 100,
        'двести': 200,
        'триста': 300,
        'четыреста': 400,
        'пятьсот': 500,
        'шестьсот': 600,
        'семьсот': 700,
        'восемьсот': 800,
        'девятьсот': 900,
    }

    x = a.split()
    number = 0
    final_number = 0
    for i in range(len(x)):
        if (x[i] == 'миллион') or (x[i] == 'миллиона') or (x[i] == 'миллионов'):
            if number == 0:
                final_number += 1000000
            number *= 1000000
            final_number += number
            number = 0

        elif (x[i] == 'тысяча') or (x[i] == 'тысячи') or (x[i] == 'тысяч'):
            if number == 0:
                final_number += 1000
            number *= 1000
            final_number += number
            number = 0
        else:
            number += words_to_numbers[x[i]]

    final_number += number
    return final_number


def calc(str):
    words = str.split()
    x1 = ''
    x2 = ''
    flag = 0
    for i in range(len(words)):
        if words[i] == 'минус':
            flag = 1
        elif flag != 1:
            if x1 == '':
                x1 += words[i]
            else:
                x1 += ' ' + words[i]
        else:
            if x2 == '':
                x2 += words[i]
            else:
                x2 += ' ' + words[i]
    return number_detect(x1) - number_detect(x2)


inet1 = 'найди в интернете'
inet2 = 'поиск в интернете'
inet3 = 'ищи'

for text in listen():
    print(text)
    if ("открой" in text) and ("диспетчер" in text) and ("задач" in text):
        os.system('taskmgr')
        print('Диспетчер задач открыт')

    elif ("открой" in text) and ("панель" in text) and ("управления" in text):
        os.system('control')
        print('Панель управления открыта')

    elif ((inet1 in text)  # поиск в интернете
          or (inet2 in text)
          or (inet3 in text)):
        if inet1 in text:               #inet1 = 'найди в интернете'
            text = text.replace(inet1, '')

        elif inet2 in text:             #inet2 = 'поиск в интернете'
            text = text.replace(inet2, '')

        elif inet3 in text:             #inet3 = 'ищи'
            text = text.replace(inet3, '')
        webbrowser.open_new_tab('https://www.google.com/search?q={}'.format(text))
        print('поисковой запрос на тему "{}" задан'.format(text))

    elif (("открой" in text) and ("файл" in text) and ("хост" in text)) or (("открой" in text) and ("хост" in text)):
        os.system('notepad.exe C:\Windows\System32\drivers\etc\hosts')
        print('Файл hosts открыт')

    elif ("выключи" in text) and ("сетевой" in text) and ("адаптер" in text):
        os.system('netsh interface set interface "Ethernet" disable')
        print('Сетевой адаптер выключен')

    elif ("включи" in text) and ("сетевой" in text) and ("адаптер" in text):
        os.system('netsh interface set interface "Ethernet" enable')
        print('Сетевой адаптер включен')

    elif "минус" in text:
        print(calc(text))

    elif ("выключи" in text) and ("программу" in text):
        exit()
