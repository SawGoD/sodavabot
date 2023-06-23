@echo off
taskkill /F /IM RBTray.exe
taskkill /F /IM speedtest.exe

cd C:\Soda_VA_BOT
git pull
start /min "Soda VA Bot Monitor" python .\soda_va_bot.py 2> .\logs\error_bat.txt
start .\resource\RBTray\64bit\RBTray.exe
echo pause