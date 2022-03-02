import tkinter
from tkinter import ttk, messagebox
import keyboard
import pickle
import os
from os.path import join
import mywinreg
from constant import DATA_PATH

time_format_values = ['{d}d{h}h{m}m{s}s',
                      '{d}d{h}h{m}m{s}s(без нулей)',
                      '{d}:{h}:{m}:{s}',
                      '{d}:{h}:{m}:{s}(без ведущих нулей)',
                      '{d}d+{h}:{m}:{s}',
                      '{d}d+{h}:{m}:{s}(без ведущих нулей)',
                      's',
                      'm',
                      'h',
                      'd']

path_setting = join(DATA_PATH, 'setting')

def load():
    try:
        f=open(path_setting, 'rb')
        data = pickle.load(f)
        f.close()
    except:
        data = {'time_format':1,
                'tray':True,
                'from_tray':'Alt+T',
                'update':False,
                'autostart':False,
                'auto_in_tray':False}
    return data

def save(data):
    f=open(path_setting, 'wb')
    pickle.dump(data, f)
    f.close()

def close():
    if messagebox.askokcancel('Настройки', '''Изменения будут сброшены.
Продолжить?'''):
        w.destroy()

def apply():
    setting = load()
    restart = False
    setting['time_format']=select['time_format'].current()
    setting['update']=select['update'].get()
    if setting['tray'] != select['tray'].get():
        setting['tray'] = select['tray'].get()
        restart = True
    if setting['from_tray'] != select['from_tray'].get():
        if select['from_tray'].get() == '':
            restart = True
            setting['from_tray'] = select['from_tray'].get()
        else:
            try:
                keyboard.add_hotkey(select['from_tray'].get(), lambda:None)
                keyboard.remove_hotkey(select['from_tray'].get())
            except:
                messagebox.showerror('Настройки', 'Неверное сочетание клавиш')
                return
            else:
                restart = True
                setting['from_tray'] = select['from_tray'].get()

    setting['autostart'] = select['autostart'].get()
    if setting['autostart']:
        mywinreg.add(join(os.getcwd(), r'start.exe'))
    else:
        mywinreg.rem()
    setting['auto_in_tray'] = select['auto_in_tray'].get()
    
    save(setting)
    if restart and messagebox.askokcancel('Перезапуск', 'Перезапустить программу?'):
        os.system('start pythonw main.pyw')
        full_exit(-1)
    w.destroy()

def create():
    global w, select

    def val():
        if in_tray.get():
            from_tray['state'] = 'normal'
            if autostart.get():
                start_in_tray_ch['state'] = 'normal'
            else:
                start_in_tray_ch['state'] = 'disabled'
        else:
            from_tray['state'] = 'disabled'
            start_in_tray_ch['state'] = 'disabled'
    
    setting = load()
    
    w = tkinter.Toplevel()
    w.protocol("WM_DELETE_WINDOW", close)
    w.title('Настройки')
    w.iconbitmap('icon.ico')
    w.resizable(False, False)
    w.grab_set()

    tkinter.Label(w, text='Формат вывода').grid(row=1, column=1, padx=(10, 5), pady=5)
    time_format = ttk.Combobox(w, values=time_format_values, width=35, state='readonly')
    time_format.set(time_format_values[setting['time_format']])
    time_format.grid(row=1, column=2, padx=(10, 5), pady=5)

    in_tray = tkinter.BooleanVar(value = setting['tray'])
    tkinter.Checkbutton(w, text='При закрытии сворачивать в трей*', variable = in_tray, onvalue=True, offvalue=False, command=val).grid(row=2, column=1, columns=2, padx=5, pady=5)

    tkinter.Label(w, text='Сочетание для быстрого развёртывания*').grid(row=3, column=1, padx=5, pady=5)
    from_tray = tkinter.Entry(w, width=15)
    from_tray.insert('0', setting['from_tray'])
    from_tray.grid(row=3, column=2, padx=5, pady=5)

    update = tkinter.BooleanVar(value = setting['update'])
    tkinter.Checkbutton(w, text='Проверять наличие обновлений при запуске', variable = update, onvalue=True, offvalue=False).grid(row=4, column=1, columns=2, padx=5, pady=5)

    autostart = tkinter.BooleanVar(value = setting['autostart'])
    tkinter.Checkbutton(w, text='Запускать программу при запуске windows', variable = autostart, onvalue=True, offvalue=False, command=val).grid(row=5, column=1, columns=2, padx=5, pady=5)

    start_in_tray = tkinter.BooleanVar(value = setting['auto_in_tray'])
    start_in_tray_ch = tkinter.Checkbutton(w, text='Тихий запуск', variable = start_in_tray, onvalue=True, offvalue=False)
    start_in_tray_ch.grid(row=6, column=1, columns=2, padx=5, pady=5)

    tkinter.Label(w, text='*Для применения необходимо перезапустить программу').grid(row=7, column=1, columns=2, padx=5, pady=5)

    tkinter.Button(w, text='Закрыть', command=close).grid(row=8, column=1, padx=(5, 10), pady=5)
    tkinter.Button(w, text='Применить', command=apply).grid(row=8, column=2, padx=(5, 10), pady=5)

    select = {'time_format':time_format,
              'tray':in_tray,
              'from_tray':from_tray,
              'update':update,
              'autostart':autostart,
              'auto_in_tray':start_in_tray}
    val()
