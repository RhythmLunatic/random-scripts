#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         RhythmLunatic

 Script Function:
	1. Launch th123 voice mod
	2. Launch game
	3. close voice mod application & fake borders when game is closed

#ce ----------------------------------------------------------------------------

; Launch voice mod
; To have the voice mod automatically choose wav, decompile the exe using HSP decompiler, then change
; it to skip the menu and goto wav, then install HSP runtime and recompile it.
; Sorry I can't do any better right now...
Local $iPID = Run("Voice\th123vB13_eng_autostart.exe","",@SW_HIDE)
; Wait for window to appear
Local $hWnd = WinWait("[CLASS:hspwnd0]", "")

; Launch th123.exe
Run("th123e.exe")
; Wait for window appear to get handle
Local $hWnd2 = WinWait("[CLASS:th123_110a]", "")
;set it active in case
WinActivate($hWnd2)
; Wait for th123 to close
WinWaitClose("[CLASS:th123_110a]")
; Kill voice mod
ProcessClose($iPID)
