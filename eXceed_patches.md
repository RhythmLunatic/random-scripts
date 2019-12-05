# eXceed Collection patches, disassembly, and information

## Graphical fixes for all games

Download WineD3DForWindows_3.0.zip, drop in ddraw.dll, libwine.dll, wined3d.dll. Do not attempt a newer or older version, it will not work.

## Disassembly for all games

### Disassembling the games
Download the decompiler: https://github.com/YSRKEN/HSP-Decompiler/releases

Run the decompiler. First select eXceed3rd-BR.exe. It will warn you that the BMP files are encrypted, press yes and decompile anyway.

This will extract start.ax into a directory named eXceed3rd-BR in the directory that eXceed3rd-BR.exe was in. With the decompiler, browse to this folder and select start.ax. This should yield start.hsp once the process is finished.

To extract the images, download this: https://github.com/gocha/spihsp/releases

Extract hspdiv.exe and undpm32.dll, run it like `hspdiv.exe eXceed3rd-BR.exe`. Done. You have your BMP files.

### Setting up a development environment

Install the HSP compiler: http://hsp.tv/index2.html

Move start.hsp to the same location as the exe file.

Paste the BMP files you had before into the same location as the exe file.

Open start.hsp in the HSP editor and press F5. You have a dev environment!

## eXceed 3rd: Jade Penetrate -Black Package- patches

Note: in a hex editor, do not type the 4 in front. That is for debuggers.

**412A99: Replace 75 05 E8 B0 FC FF FF -> C6 46 08 0D 90 90 90 to make any key start the game.**
- JNZ here is dead code and the function that this replaces is never called in the first place.
- The new code in asm is `mov byte ptr [esi+8], 0D`. 0D = Enter key
- MapVirtualKeyA checks esi+8 a few lines down and then some other functions check the same location.

**412A93: Replace 75 35 -> 90 90 to make it ALWAYS check for a key press.**
- Combining with the above patch, this means it checks for a key press even when there isn't one, and then the location that it checks for a key press has the enter key inserted into it. So it will start the game right away!

### Other research
**This section is old and unnecessary since you can modify the game code with the HSP Disassembler. You should ignore it because the addresses will change when you recompile the game.**

412AD0 handles the popup

412B2C Checks for GAME START using GetMessageA

412A00 Don't remove this function, there is a call to 4047E0 which calls 404550 which seems to be a file handler. Maybe checks last used resolution.


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

Creditz: IDA Pro, Ollydbg, and online x86 disassembler and assemblers.

## eXceed 2nd Vampire REX Launcher Skip
Porting from eXceed 3rd... Please refer to that file if you want the technical explanation.

Same process as ex3. Open Exceed2.exe in a hex editor. Press Ctrl+G to jump to offset. Replace bytes.

12A93: 75 35 83 7E 08 09 75 05 E8 B0 FC FF FF -> 90 90 83 7E 08 09 C6 46 08 0D 90 90 90
