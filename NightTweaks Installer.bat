@echo off
SETLOCAL EnableDelayedExpansion

SET /a "count=0"
SET /a "total=15"

echo Installing necessary Python modules...

echo [0%%] Starting installation...

pip install discord.py==1.7.3
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed discord.py 1.7.3...

pip install discord==1.7.3
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed discord 1.7.3...

:: 'tkinter' typically comes with Python. Uncomment below if needed.
:: pip install tk
:: SET /a "count+=1"
:: SET /a "calcPercent=count*100/total"
:: echo [!calcPercent!%%] Installed tk...

pip install urllib3
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed urllib3...

pip install PyQt5
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed PyQt5...

pip install PyQtWebEngine
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed PyQtWebEngine...

pip install keyboard
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed keyboard...

pip install pyautogui
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed pyautogui...

pip install pyperclip
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed pyperclip...

pip install tqdm
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed tqdm...

pip install flask
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed flask...

pip install requests
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed requests...

pip install beautifulsoup4
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed beautifulsoup4...

pip install lxml
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed lxml...

pip install numpy
SET /a "count+=1"
SET /a "calcPercent=count*100/total"
echo [!calcPercent!%%] Installed numpy...

echo [100%%] Installation complete.
pause
