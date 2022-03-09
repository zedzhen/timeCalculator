import tkinter
import os
import ctypes
from sys import platform, argv, exit
from tkinter import messagebox
from queue import Queue
from threading import Thread

root = tkinter.Tk()
root.withdraw()

if platform != 'win32':
    if platform == 'cygwin':
        messagebox.showwarning('ОС', 'Данная программа не тестировалась на cygwin')
    else:
        messagebox.showerror('ОС', 'Данная программа работает только на windows')
        exit(1)

try:
    import keyboard
    import pystray
    from PIL import Image
    import requests
except ImportError:
    if messagebox.askokcancel('Модули', '''Необходимо установить библиотеки keyboard, pystray, Pillow и requests
Попробовать устанвить библиотеки автоматически?'''):
        if os.system('python -m pip install keyboard pystray==0.19.1 Pillow requests') == 0:
            messagebox.showinfo('Модули', '''Модули успешно установлены
Программа будет перезапущена''')
            os.system('start start.exe')
            exit(-1)
        messagebox.showinfo('Модули', '''Как минимум один из модулей не был установлен
Программа будет закрыта
Установите модули вручную
см README.txt''')
    messagebox.showinfo('Модули', '''Программа будет закрыта
Установите модуль вручную
см README.txt''')
    exit(1)

import setting
import help_tk
from constant import *

class Button(tkinter.Button):
    def __init__(self, root, frame, text, insert = None, key = None, width=1):
        if insert is None:
            insert = text
        if key is None:
            key = text
        super().__init__(frame, text = text, command = self.add, width=width, bd=1)
        root.bind(key, self.add)
        self.insert = insert

    def add(self, *_):
        add(self.insert)

def add(text):
    if text[:2]==text[-2:]=='//':
        command(text[2:-2])
        return
    if root.focus_get() is in_text:
        return
    if not clear:
        command('CLEAR')
    in_text.insert('end', text)

def command(com):
    global clear
    if com == 'ENTER':
        s = in_text.get()
        if s == '':
            return
        if not validate(s):
            return TimeError('Math')
        s2 = ''
        colon = 0
        for i in range(len(s)-1, -1, -1):
            if s[i] == ':':
                if colon <= 1:
                    s2 = ')*60+'+s2
                elif colon == 2:
                    s2 = ')*24+'+s2
                else:
                    return TimeError('Math')
                colon += 1
            elif s[i] in (MATH_SYMBOL + '()'):
                s2 = s[i] + '('*colon + s2
                colon = 0
            else:
                s2 = s[i] + s2
        s2 = '('*colon + s2
        s3 = ''
        for i in range(len(s2)):
            if s2[i] == '(' and i != 0 and s2[i-1] not in MATH_SYMBOL_FULL:
                s3+='*'
                s3+=s2[i]
            elif s2[i] == ')' and i != len(s2)-1 and s2[i+1] not in MATH_SYMBOL_FULL:
                s3+=s2[i]
                s3+='*'
            elif s2[i] in DIGIT and i !=0 and s2[i-1] in LETTER:
                s3+='+'
                s3+=s2[i]
            else:
                s3+=s2[i]
        s3=s3.replace('d', '*24h')
        s3=s3.replace('h', '*60m')
        s3=s3.replace('m', '*60s')
        s3=s3.replace('s', '')
        ans = round(eval(s3))

        out_text['state']='normal'
        out_text.delete('0', 'end')
        out_text.insert('0', format_time(ans))
        out_text['state']='disabled'

        clear = False
    if com == 'CLEAR':
        in_text.delete('0', 'end')
        clear = True
    if com == 'BACKSPACE':
        if root.focus_get() is in_text:
            return
        in_text.delete(len(in_text.get())-1)

def TimeError(type_str):
    out_text['state']='normal'
    out_text.delete('0', 'end')
    out_text.insert('0', type_str+'Error')
    out_text['state']='disabled'

def format_time(second, f = None):
    if f is None:
        f = setting.load()['time_format']
    if f in (0, 1):
        ans = ''
        if second % 60 != 0 or f == 0 or second == 0:
            ans = str(second % 60)+'s'+ans
        second//=60
        if second % 60 != 0 or f == 0:
            ans = str(second % 60)+'m'+ans
        second//=60
        if second % 60 != 0 or f == 0:
            ans = str(second % 24)+'h'+ans
        second//=24
        if second != 0 or f == 0:
            ans = str(second)+'d'+ans
        return ans
    if f in (2, 3):
        if second == 0:
            return '0s'
        ans = ''
        ans = str(second % 60)
        second//=60
        ans = str(second % 60)+':'+ans
        second//=60
        if second or f == 2:
            ans = str(second % 24)+':'+ans
            second//=24
            if second or f == 2:
                ans = str(second)+':'+ans
        return ans
    if f == 4:
        return str(second // (60*60*24))+'d+'+format_time(second % (60*60*24), 2)
    if f == 5:
        if second % (60*60*24) == 0:
            return str(second // (60*60*24))+'d'
        elif second // (60*60*24) == 0:
            return format_time(second % (60*60*24), 3)

        return str(second // (60*60*24))+'d+'+format_time(second % (60*60*24), 3)
    if f == 6:
        return str(second)+'s'
    if f == 7:
        return str(second/60)+'m'
    if f == 8:
        return str(second/(60*60))+'h'
    #if f == 9:
    return str(second/(60*60*24))+'d'

def close():
    if local_setting['tray']:
        root.quit()
    else:
        full_exit()

def full_exit(code=0):
    root.destroy()
    icon.stop()
    exit(code)

setting.full_exit = full_exit

def validate(P):
    last_is_digit = False
    last_is_letter = False
    last_is_math_symbol = False
    bracket = 0
    for i in range(len(P)):
        s = P[i]
        if s not in (DIGIT+LETTER+MATH_SYMBOL_FULL):
            return False

        if s == '(':
            bracket += 1
        if s == ')':
            bracket -=1
            if bracket < 0:
                return False

        if s in ':.':
            if not last_is_digit:
                return False
            if i == len(P)-1 or P[i+1] not in DIGIT:
                return False

        if s in LETTER:
            if last_is_LETTER or (not last_is_digit):
                return False
            last_is_LETTER = True
        else:
            last_is_LETTER = False

        if s in MATH_SYMBOL:
            if last_is_math_symbol:
                return False
            last_is_math_symbol = True
        else:
            last_is_math_symbol = False

        last_is_digit = s in DIGIT
    if bracket or last_is_math_symbol:
        return False

    if P.find(':') == -1:
        return True

    colon = False
    letter = False
    for i in range(len(P)):
        s=P[i]
        if s in MATH_SYMBOL+'()':
            colon = letter = False
        if s in LETTER:
            letter = True
        if s == ':':
            colon = True
        if colon and letter:
            return False
    if last_is_digit and not colon:
        return False
    return True

def val(P):
    for i in P:
        if i not in (DIGIT+LETTER+MATH_SYMBOL_FULL):
            return False
    return True

if not os.path.isdir(DATA_PATH):
    os.mkdir(DATA_PATH)

local_setting = setting.load()

openning = Queue()
openning.put(True)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(NAME)

#main tkinter window
root.title('Калькулятор времени')
root.protocol("WM_DELETE_WINDOW", close)
root.iconbitmap('icon.ico')
root.resizable(False, False)

vc = (root.register(val), '%P')

in_text = tkinter.Entry(width=50, validate='all', validatecommand=vc)
in_text.grid(column=0, row=0, sticky='w', padx=5, pady=(10, 2))
clear = True

out_text = tkinter.Entry(width=30, state='disabled')
out_text.grid(column=0, row=1, sticky='w', padx=5, pady=2)

fr = tkinter.Frame(root)
fr.grid(column=0, row=2, sticky='w', padx=5, pady=2)

Button(root, fr, '1').grid(column=0, row=0)
Button(root, fr, '2').grid(column=1, row=0)
Button(root, fr, '3').grid(column=2, row=0)
Button(root, fr, '4').grid(column=0, row=1)
Button(root, fr, '5').grid(column=1, row=1)
Button(root, fr, '6').grid(column=2, row=1)
Button(root, fr, '7').grid(column=0, row=2)
Button(root, fr, '8').grid(column=1, row=2)
Button(root, fr, '9').grid(column=2, row=2)
Button(root, fr, '0').grid(column=0, row=3)
Button(root, fr, '.').grid(column=1, row=3)
Button(root, fr, '.', key=',')
Button(root, fr, ':').grid(column=2, row=3)

tkinter.Label(fr).grid(column=3, row=0)

Button(root, fr, '+').grid(column=4, row=0)
Button(root, fr, '-').grid(column=5, row=0)
Button(root, fr, '*').grid(column=6, row=0)
Button(root, fr, '/').grid(column=7, row=0)
Button(root, fr, '(').grid(column=4, row=1)
Button(root, fr, ')').grid(column=5, row=1)
Button(root, fr, 'd').grid(column=4, row=2)
Button(root, fr, 'h').grid(column=5, row=2)
Button(root, fr, 'm').grid(column=6, row=2)
Button(root, fr, 's').grid(column=7, row=2)

Button(root, fr, 'C', insert='//CLEAR//').grid(column=4, row=3)
Button(root, fr, 'c', insert='//CLEAR//')
Button(root, fr, '←', insert='//BACKSPACE//', key='<BackSpace>').grid(column=5, row=3)
Button(root, fr, '=', insert='//ENTER//', key='<Return>').grid(column=6, row=3)
Button(root, fr, '=', insert='//ENTER//')

#menu
menu = tkinter.Menu(root)
root['menu'] = menu

mainmenu = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label='Основное', menu=mainmenu)

mainmenu.add_command(label='Настройки', command=setting.create)
mainmenu.add_command(label='Сбросить настройки', command=setting.reset)
mainmenu.add_separator()
mainmenu.add_command(label='Закрыть окно', command=close, accelerator='Alt+F4')
mainmenu.add_command(label='Выход', command=full_exit, accelerator='Ctrl+Q')

keyboard.add_hotkey('ctrl+q', full_exit)


aboutmenu = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label='О программе', menu=aboutmenu)

aboutmenu.add_command(label='Помощь', command=help_tk.create_help)
aboutmenu.add_command(label='О программе', command=lambda:help_tk.create_about(root))
aboutmenu.add_command(label='Проверить обновления', command=lambda:help_tk.create_update(root))

#tray
if local_setting['tray']:
    icon = pystray.Icon(NAME,
                        icon = Image.open('icon.ico'),
                        menu = pystray.Menu(pystray.MenuItem('Открыть', lambda:openning.put(True), default = True),
                                            pystray.MenuItem('Выход', full_exit)))
    Thread(target=icon.run).start()
    if local_setting['from_tray'] != '':
        keyboard.add_hotkey(local_setting['from_tray'], lambda:openning.put(True))
    if local_setting['auto_in_tray']  and "-auto" in argv:
        openning.get()

#check_update
if local_setting['update'] and help_tk.check_update():
    data = help_tk.load()
    if data['last_version'] != VERSION:
        help_tk.create_update(root)

#main
while True:
    if openning.qsize() and openning.get():
        root.deiconify()
        root.mainloop()
        root.withdraw()
        while openning.qsize():
            openning.get()
