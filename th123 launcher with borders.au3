#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         RhythmLunatic

 Script Function:
	1. Launch th123 voice mod and auto select wav
	2. Add borders to game using https://github.com/RhythmLunatic/DrawImageXNA
	3. Launch game using a custom DxWnd profile which makes the game window fit to screen
	4. close voice mod application & fake borders when game is closed

#ce ----------------------------------------------------------------------------

; Launch voice mod
Local $iPID = Run("Touhou voice mod\th123vB13.exe")
; Wait for window to appear
Local $hWnd = WinWait("[CLASS:hspwnd0]", "")
; Click wav button
ControlClick("東方非想天則に魂を以下略","wav音声", 16384)
; Apparently the window won't launch unless I wait 1ms
Sleep(1)
WinSetState($hWnd, "", @SW_MINIMIZE)
; Launch th123.exe
;Run("th123e.exe")
Local $PID2 = Run("DrawBorder\XNADrawImage.exe 1920 1080 DrawBorder\bg.jpg")
Run("DxWnd\dxwnd.exe /r:5", "DxWnd")
; Wait for window appear to get handle
Local $hWnd2 = WinWait("[CLASS:th123_110a]", "")
; Set window as always on top
WinSetOnTop($hWnd2, "", 1)
;DrawBorder can take some time to start up, wait so th123 can be the active application and DrawImage doesn't take it away
WinWaitActive("XNADrawImage")
WinActivate("[CLASS:th123_110a]", "")
;Hide the taskbar
Opt('WINTITLEMATCHMODE', 4)
ControlHide('classname=Shell_TrayWnd', '', '')
; Wait for th123 to close
WinWaitClose("[CLASS:th123_110a]")
; Kill voice mod
ProcessClose($iPID)
;Kill borders
ProcessClose($PID2)
;Show the taskbar
ControlShow('classname=Shell_TrayWnd', '', '')
