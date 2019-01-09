eXceed 3: Jade Penetrate -Black Package- has an unskippable popup on start. This is a (bad) attempt to remove it.

The two relevant functions are at 412AD0 and 412C80. Attempt to NOP out 412AD0 will make the game crash immediately.

Function 412A00 seems to DISPLAY the textbox after it's initialized.
