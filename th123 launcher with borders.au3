#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         RhythmLunatic

 Script Function:
	1. Launch th123 voice mod
	2. Add borders to game using https://github.com/RhythmLunatic/DrawImageXNA
	3. Launch game in borderless fullscreen using SWRSToys + my mod
	4. close voice mod application & fake borders when game is closed

#ce ----------------------------------------------------------------------------

; Launch voice mod
; To have the voice mod automatically choose wav, decompile the exe using HSP decompiler, then change
; it to skip the menu and goto wav, then install HSP runtime and recompile it.
; Sorry I can't do any better right now...
Local $iPID = Run("Voice\th123vB13_eng_autostart.exe","",@SW_MINIMIZE)
; Wait for window to appear
Local $hWnd = WinWait("[CLASS:hspwnd0]", "")


;Hide the mouse
MouseMove(@DesktopWidth,@DesktopHeight,0)

$isLargerThan43 = @DesktopWidth/@DesktopHeight > 1.34
If $isLargerThan43 == True Then
   ;We can launch this after since we're going to put th123 on top anyways
   Local $PID2 = Run("DrawImage\XNADrawImage.exe "&@DesktopWidth&" "&@DesktopHeight&" DrawImage\bg.jpg")
EndIf

; Launch th123.exe
Run("th123e.exe")
; Wait for window appear to get handle
Local $hWnd2 = WinWait("[CLASS:th123_110a]", "")
; Set window as always on top
WinSetOnTop($hWnd2, "", 1)
WinActivate($hWnd2)
;Hide the taskbar
Opt('WINTITLEMATCHMODE', 4)
ControlHide('classname=Shell_TrayWnd', '', '')
; Wait for th123 to close
WinWaitClose("[CLASS:th123_110a]")
; Kill voice mod
ProcessClose($iPID)
If $isLargerThan43 == True Then
   ;Kill borders
   ProcessClose($PID2)
EndIf
;Show the taskbar
ControlShow('classname=Shell_TrayWnd', '', '')
