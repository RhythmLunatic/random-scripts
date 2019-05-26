eXceed 3rd: Jade Penetrate -Black Package- has an unskippable launcher on start. This is a (bad) attempt to remove it.

412AD0 handles the popup

412B2C Checks for GAME START using GetMessageA

412C2B: This is triggered when you press start and is a HSPERROR... But it drops down to 412C42!
- But setting eax to 6 manually just causes an access violation, crashing the game/debugger.

Function 410290 sets up most of the game including loading assets, drawing the launcher window, resizing the window, etc.
- 410693 sets window title

412B4D: Does nothing, set 2 bytes to NOP

405BCE: The JNZ here is dead code and is never encountered normally, so it can be changed to JMP (75 -> EB).

413136: Has no effect on the game, so you can remove it if you want. Maybe a duplicate call to the launcher handler? e8 95 f9 ff ff -> 90 90 90 90 90

Random HSPERROR pitfalls (and the opcodes to patch them out):
* 40910A: 7E 30 -> 90 90
* 402F18: 75 -> EB
* 4090B8: 75 -> EB
* 4045ed: 7D -> EB
* 404632: 7D -> EB
* 412a41: 75 08 -> 90 90
* 412afc: 0F 94 D9 00 00 00 -> 90 90 90 90 90 90
* 412b37: 0f 84 b1 00 00 00 -> 90 90 90 90 90 90
* 412a49: 74 -> EB
* 412a77: 75 -> eb
* 4102aa: 0f 87 91 1c 00 00 -> 90 90 90 90 90 90
* 412c01-412c41: Actually, don't patch these, if you do the game won't close :V
