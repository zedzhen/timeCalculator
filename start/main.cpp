#include<iostream>
#include<windows.h>
#include<stdlib.h>
#include<direct.h>

using namespace std;

int main(int argc, char *argv[])
{
    char path[MAX_PATH], drive[MAX_PATH], path2[MAX_PATH];
    GetModuleFileName(NULL, path, MAX_PATH);
    _splitpath(path, drive, path2, NULL, NULL);
    _chdir(strcat(drive, path2));

    bool autostart = false;
    for (int i=1; i<argc; i++)
    {
        if (string(argv[i]) == "-auto")
        {
            autostart = true;
        }
    }

    if (system("python/pythonw -c exit(0)") == 0)
    {
        if (autostart)
        {
            system("start python/pythonw main.pyw -auto");
            return 0;
        }
        system("start python/pythonw main.pyw");
        return 0;
    }
    else
    {
        if (system("pythonw -c exit(0)") != 0)
        {
            if (!autostart)
            {
                MessageBox(NULL, TEXT("Установите python и добавьте в path путь до папки с ним\nИли установите версию со встроенным python"), TEXT("Python"), MB_OK);
            }
            return 1;
        }


        if (autostart)
        {
            system("start pythonw main.pyw -auto");
            return 0;
        }
        system("start pythonw main.pyw");
        return 0;
    }
}
