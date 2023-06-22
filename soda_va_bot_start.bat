@echo off
taskkill /F /IM RBTray.exe
taskkill /F /IM ShareX.exe
taskkill /F /IM speedtest.exe

cd C:\Soda_VA_BOT
echo git pull > initial_launch.ps1
powershell.exe -ExecutionPolicy Bypass -File ".\initial_launch.ps1"
start /min "Soda VA Bot Monitor" python .\soda_va_bot.py 2> .\logs\error_bat.txt
start .\resource\RBTray\64bit\RBTray.exe
start .\resource\ShareX\ShareX.exe
echo pause