#include<iostream>
#include<windows.h>
#include<stdlib.h>
#include<direct.h>
#include<string>

using namespace std;

const int MAXPATH = 32767;

unsigned long cmd(string com)
{
    string total = "cmd.exe /c " + com;
    STARTUPINFO si={sizeof(si)};
    PROCESS_INFORMATION pi;
    if(CreateProcess(NULL, total.data(), NULL, NULL, false, CREATE_NO_WINDOW, NULL, NULL, &si, &pi))
    {
        WaitForSingleObject(pi.hProcess, INFINITE);
        unsigned long ExitCode;
        GetExitCodeProcess(pi.hProcess, &ExitCode);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return ExitCode;
    }
    return 1;
}

int main(int argc, char *argv[])
{
    char path[MAXPATH], drive[MAXPATH], path2[MAXPATH];
    GetModuleFileName(NULL, path, MAXPATH);
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

    if (cmd(".\\python\\pythonw.exe -c exit(0)") == 0)
    {
        if (autostart)
        {
            cmd("start .\\python\\pythonw.exe main.pyw -auto");
            return 0;
        }
        cmd("start .\\python\\pythonw.exe main.pyw");
        return 0;
    }
    else
    {
        if (cmd("pythonw.exe -c exit(0)") != 0)
        {
            if (!autostart)
            {
                MessageBox(NULL, TEXT("”становите python и добавьте в path путь до папки с ним\n»ли установите версию со встроенным python"), TEXT("Python"), MB_OK);
            }
            return 1;
        }


        if (autostart)
        {
            cmd("start pythonw.exe main.pyw -auto");
            return 0;
        }
        cmd("start pythonw.exe main.pyw");
        return 0;
    }
}
