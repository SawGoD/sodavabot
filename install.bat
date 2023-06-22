@echo off
color 81
echo python -m pip install --upgrade pip >> packages.ps1
echo pip install python-telegram-bot==13.7 > packages.ps1
echo pip install telegram >> packages.ps1
echo pip install telegram.ext >> packages.ps1
echo pip install pyautogui >> packages.ps1
echo pip install subprocess >> packages.ps1
echo pip install plyer >> packages.ps1
echo pip install pyperclip >> packages.ps1

powershell.exe -ExecutionPolicy Bypass -File ".\packages.ps1"
del packages.ps1
cls
color 87
cd C:\
mkdir "Soda_VA_BOT"
xcopy "%~dp0*" "C:\Soda_VA_BOT\" /s /i /y
cls
color 81
REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /V "Soda VA Bot" /t REG_SZ /F /D "C:\Soda_VA_BOT\soda_va_bot_start.bat"
call :colored "Complete" Green
call :colored "Press any button to exit" White
pause >nul
exit
:colored
%Windir%\System32\WindowsPowerShell\v1.0\Powershell.exe write-host -foregroundcolor %2 %1
