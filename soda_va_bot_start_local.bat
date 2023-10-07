@echo off
taskkill /F /IM RBTray.exe
taskkill /F /IM speedtest.exe

echo pip install -r requirements.txt > packages.ps1
powershell.exe -ExecutionPolicy Bypass -File ".\packages.ps1"
del packages.ps1
cls

cd C:\Soda_VA_BOT
start /min "Soda VA Bot Monitor" python .\soda_va_bot.py 2> .\logs\error_bat.txt
start .\resource\RBTray\64bit\RBTray.exe
echo pause