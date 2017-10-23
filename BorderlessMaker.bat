@echo off
::This script requires nircmd and grep installed in your PATH along with BorderlessGaming (or equivalent)
::It matches the monitor resolution to the resolution of the game, then makes the game borderless, and
::after you close the game it will reset back to the maximum resolution of the display device.
::wmic only gets the max resolution, not the actual resolution according to people online. I don't care about this,
::so if you need a fix, do it yourself.
for /f "tokens=*" %%i in ('wmic desktopmonitor get screenheight  ^| grep -o "[[:digit:]]*"') do set DisplayHeight=%%i
for /f "tokens=*" %%i in ('wmic desktopmonitor get screenwidth  ^| grep -o "[[:digit:]]*"') do set DisplayWidth=%%i
nircmd setdisplay 1280 720 32
start "" "C:\Program Files (x86)\Borderless Gaming\BorderlessGaming.exe"
th145e.exe
taskkill /IM BorderlessGaming.exe /F
nircmd setdisplay %DisplayWidth% %DisplayHeight% 32
