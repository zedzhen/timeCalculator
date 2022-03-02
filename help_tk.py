import tkinter
from tkinter import simpledialog, messagebox
from datetime import datetime
import requests
import webbrowser
from constant import *
import pickle
from os.path import join

path_checked = join(DATA_PATH, 'checked')

def load():
    try:
        f=open(path_checked, 'rb')
        data = pickle.load(f)
        f.close()
    except:
        data = {'last_version':None,
                'last_version_checked':None,
                'last_version_url':None}
    return data

def save(data):
    f=open(path_checked, 'wb')
    pickle.dump(data, f)
    f.close()

def create_help():
    w = tkinter.Toplevel()
    w.iconbitmap('icon.ico')
    w.title('Справка')
    w.resizable(False, False)

    h = tkinter.Text(w, width=60, height=30, wrap='word', font='Arial 10')
    h.grid(row=0, column=0)
    scroll = tkinter.Scrollbar(w, command=h.yview)
    scroll.grid(row=0, column=1, sticky='ns')
    h['yscrollcommand'] = scroll.set
    h.insert('0.0', '''"Калькулятор времени" создан для удобства подсчёта времени.
Формат ввода
<число>d - кол-во дней
<число>h - кол-во часов
<число>m - кол-во минут
<число>s - кол-во секунд (букву s можно пропустить, но не рекомендуется)

[[<число1>:]<число2>:]<число3>:<число4> аналогично <число1>d<число2>h<число3>m<число4>s
<число1> и <число2> можно пропустить

Формат вывода
{d} заменяеться на дни
{h} заменяеться на часы
{m} заменяеться на минуты
{s} заменяеться на секунды

"Без нулей" при выводе через ":" дни/часы опускаются, если в них 0
при выводе с буквами опускается всё с 0 (если ответ 0s, то он так и выводится)

при смешанном выводе, 0s выводится как 0d
при целом числе дней, часть через ":" опускатся

при выборе s ответ выводится в секундах
при выборе m, h, d ответ выводиться как дробное число минут/часов/дней соответственно

Быстрое развёртывание
Одна или несколько клавиш через +
Для отключения оставьте поле пустым

Тихий запуск
При автозапуске приложение будет запущено в трее (без показа окна).

картики взяты с pixabay.com/ru''')
    h['state'] = 'disabled'
    h.tag_config('title', font='Arial 12 bold')
    h.tag_config('title2', font='Arial 10 bold')
    h.tag_add('title2', '1.0', '1.21')
    h.tag_add('title', '2.0', '2.end')
    h.tag_add('title', '11.0', '11.end')
    h.tag_add('title2', '17.0', '17.11')
    h.tag_add('title', '26.0', '26.end')
    h.tag_add('title', '30.0', '30.end')

    strs = h.get("0.0", "end").split('\n')
    for i in range(len(strs)):
        for j in range(len(strs[i])):
            if strs[i][j] == ':':
                h.tag_add('title', f'{i+1}.{j}', f'{i+1}.{j+1}')

class create_about(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'О программе')

    def body(self, master):
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        h = tkinter.Text(master, width=45, height=3, wrap='word', font='Arial 10')
        h.pack()
        h.insert('0.0', f'''"Калькулятор времени"
Версия {VERSION} ({VERSION_DATE})
Страница проекта {HOME_URL}''')
        h['state'] = 'disabled'


    def buttonbox(self):
        fr = tkinter.Frame(self)
        fr.pack()
        tkinter.Button(fr, text='OK', command=self.destroy).grid(row=0, column=1, padx=10)
        tkinter.Button(fr, text='Открыть проект', command=lambda:webbrowser.open('https://'+HOME_URL)).grid(row=0, column=2,padx=10)

class create_update(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'Обновления')

    def body(self, master):
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        self.h = tkinter.Text(master, width=33, height=2, wrap='word', font='Arial 10')
        self.h.grid(row=0, column=0)
        self.insert()

    def insert(self):
        data = load()
        self.h['state']='normal'
        self.h.delete('0.0', 'end')
        self.h.insert('0.0', f'''Последняя версия {data['last_version']}
Последняя проверка {data['last_version_checked']}''')
        self.h['state'] = 'disabled'

    def buttonbox(self):
        self.frame = frame = tkinter.Frame(self)
        frame.pack()
        tkinter.Button(frame, text='Проверка обновлений', command=self.check_update).grid(row=0, column=1)
        tkinter.Button(frame, text='Закрыть', command=self.destroy).grid(row=0, column=2)
        data=load()
        if data['last_version_url'] is not None and data['last_version'] != VERSION:
            tkinter.Button(frame, text='Скачать последнюю версию', command=lambda:webbrowser.open(data['last_version_url'])).grid(row=1, column=1, columns=2)

    def check_update(self):
        r = check_update()
        self.insert()
        data = load()
        if r:
            if data['last_version'] != VERSION:
                tkinter.Button(self.frame, text='Скачать последнюю версию', command=lambda:webbrowser.open(data['last_version_url'])).grid(row=1, column=1, columns=2)
        else:
            messagebox.showwarning('Проверка обновлений', 'При проверке обновлений возникла ошибка')
        
def check_update():
    try:
        last = requests.get(UPDATE_URL+'/last.txt', timeout=(3, 1))
        url = requests.get(UPDATE_URL+'/url.txt', timeout=(3, 1))
    except requests.exceptions.RequestException:
        return False
    else:
        data = load()
        if last.status_code == 200:
            data['last_version']=last.text[:-1]
            data['last_version_checked']=datetime.now().strftime('%H:%M %d/%m/%Y')
        if url.status_code == 200:
            data['last_version_url']=url.text[:-1]
        save(data)
        return last.status_code == url.status_code == 200
