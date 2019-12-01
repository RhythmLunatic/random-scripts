# eXceed 2nd: Vampire REX patches

## Launcher Skip
Porting from eXceed 3rd... Please refer to that file if you want the technical explanation.

Same process as ex3. Open Exceed2.exe in a hex editor. Press Ctrl+G to jump to offset. Replace bytes.

12A93: 75 35 83 7E 08 09 75 05 E8 B0 FC FF FF -> 90 90 83 7E 08 09 C6 46 08 0D 90 90 90

## Graphical fixes

Download WineD3DForWindows_3.0.zip, drop in ddraw.dll, libwine.dll, wined3d.dll. Do not attempt a newer or older version, it will not work.
