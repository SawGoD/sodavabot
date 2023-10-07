@echo off
color 81
echo pip install -r requirements.txt > packages.ps1
powershell.exe -ExecutionPolicy Bypass -File ".\packages.ps1"
del packages.ps1
cls

color 87
IF NOT EXIST "C:\Soda_VA_BOT" (
    mkdir "C:\Soda_VA_BOT"
    xcopy "%~dp0*" "C:\Soda_VA_BOT\" /s /i /y
)
cd C:\Soda_VA_BOT
start "Soda creator" python .\blocks\s_file_gen.py
cls

color 81
call :colored "Types of registry entry:" Red
call :colored "1. soda_va_bot_start.bat - auto-update 'git pull' / recommended if installed via 'git clone'" White
call :colored "2. soda_va_bot_start_local.bat - no auto-update / recommended if installed from archive" White
CHOICE /C 12 /M "Select registry entry: soda_va_bot_start.bat / soda_va_bot_start_local.bat"
IF ERRORLEVEL 2 (
    REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /V "Soda VA Bot" /t REG_SZ /F /D "C:\Soda_VA_BOT\soda_va_bot_start_local.bat"
) ELSE (
    REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /V "Soda VA Bot" /t REG_SZ /F /D "C:\Soda_VA_BOT\soda_va_bot_start.bat"
)
call :colored "Complete" Green
call :colored "Press any button to exit" White
pause >nul
exit
:colored
%Windir%\System32\WindowsPowerShell\v1.0\Powershell.exe write-host -foregroundcolor %2 %1
