# eReader Save Patcher
A hacky tool to allow save data from GBA eReaders to be used on different GBA eReaders without breaking the 'Scan Card' functionaliy.

Requirements:

Python (3.11+ I think).
A save file you want to use at the end.
A save file that doesn't break your eReader.

Instructions:

1. Stick 'eReader Save Patcher.py' in a folder (preferably somewhere like ./Documents/ereader patcher or ./Downloads/ereader patcher)
2. Put a copy of a save file with your eReaders callibration data in the same location. Basically just dump a save of your card before you do anything that might break it.
3. Put a copy of a save file that you want to use on your eReader in the same location.
4. Open 'eReader Save Patcher.py ' in a terminal window (powershell, command prompt, a linux one probably works)
5. Follow the prompts on screen. It asks for the names of: The callibration data holding save, The save you want to patch, The file you want the output save to be called. In that order.
6. Write the output file onto your eReader with whatever tool you prefer.

This code comes with less than no guarantees. Not only do I not promise it works, I don't even know what I'm doing. Code is here so read it yourself and be aware that you shoulder all the risk for using this on your own data. By design, it shouldn't edit the files you feed into it unless you give the output file the same name as one of your other files so I don't recommend doing that. Also, to maintain maximum compatibility, it does nothing to the file names. So you must give it the full filename e.g. mysave.sav, save.bin, user.fla etc.

Most of this code from me misunderstanding ChatGPT and a lot of duckduckgoing...

Please don't submit pull requests unless they are simple. I won't understand. Fork this and run wild!
