# timeCalculator
Калькулятор для времени.
С помощью этой программе вы сможете посчитать время.

## Компиляторы
### C++
(Для разработки используется Code::Blocks, cbp - файл проекта) \
Для компиляции C++ используется mingw64 из msys2 64bit
> g++.exe (Rev9, Built by MSYS2 project) 11.2.0 

Команды
> windres.exe   -J rc -O coff -i "path\start\icon.rc" -o obj\start\icon.res \
> g++.exe -Wall -lstdc++fs -Os -std=gnu++17  -c "path\start\main.cpp" -o obj\start\main.o \
> g++.exe  -o ..\start.exe  obj\start\main.o obj\start\icon.res -s -static-libstdc++ -static-libgcc -static   -mwindows

### python
Установщики с python включают embeddable (64-bit) версию python \
В неё добавлен pip (https://bootstrap.pypa.io/get-pip.py) \
Установлены необходимые пакеты \
И скопированные файлы tcl/tkinter из Windows installer (64-bit) \
> папка tcl из корня \
> папка tkinter из Lib \
> файлы _tkinter.pyd, tcl86t.dll, tk86t.dll из папки DLLs \
> 
> Все папки/файлы скопированны в корень

### установщики
Установщики делаютсяпри помощи Inno Setup (.iss файл для inno setup)

## подписи
Все компилированные мной исполняемые файлы (start.exe, setup.exe, uninstall.exe подписываются) \
репозиторий с открытыми ключами (https://github.com/zedzhen/CA)
### Ошибики установки
Возможно при попытки запуска от имени администратора возникнет ошибка ("Сервер возвратил ссылку"), это значит что нельзя запускать от администратора ПО без проверенных подписей.
Решения:
* Запуск через "Администратор: Командная строка" (Для удаления запустить файл unins000.exe)
* Установить только для 1 пользователя
* Установить сертификат
