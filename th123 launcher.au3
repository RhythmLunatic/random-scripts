#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         RhythmLunatic

 Script Function:
	1. Launch th123 voice mod and auto select wav
	2. Launch game
	3. close voice mod application when game is closed

#ce ----------------------------------------------------------------------------

; Launch voice mod
Local $iPID = Run("Touhou voice mod\th123vB13.exe")
; Wait for window to appear
WinWait("[CLASS:hspwnd0]", "")
; Click wav button
ControlClick("東方非想天則に魂を以下略","wav音声", 16384)
; Wait
Sleep(100)
; Launch th123.exe
Run("th123e.exe")
; Wait (Window has to appear)
WinWait("[CLASS:th123_110a]", "")
; Wait for th123 to close
WinWaitClose("[CLASS:th123_110a]")
; Kill voice mod
ProcessClose($iPID)
