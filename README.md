# e-Reader Save Patcher
A hacky tool to allow save data from GBA e-Reader(+)'s (AGB-014) to be used on different GBA eReaders without breaking the 'Scan Card' functionaliy.

Requirements:

Python (3.11+ I think).
A save file you want to use at the end.
A save file that doesn't break your e-Reader.
A terminal interface and folders and such.
Instructions:

# **Note: This is bad and pointless and messy. I wanted to split this to prove I could and it made everything worse. Don't use this version.**

If you still want to download all the `.py` files and run `patcher.py` with the terminal like in the main versions instructions. Should work the same otherwise unless you change the files or the config.

This code comes with less than no guarantees. Not only do I not promise it works, I don't even know what I'm doing. Code is here so read it yourself and be aware that you shoulder all the risk for using this on your own data. By design, it shouldn't edit the files you feed into it unless you give the output file the same name as one of your other files so I don't recommend doing that. Also, to maintain maximum compatibility, it does nothing to the file names. So you must give it the full filename e.g. mysave.sav, save.bin, user.fla etc.

Most of this code from me misunderstanding ChatGPT and a lot of duckduckgoing...

Please don't submit pull requests unless they are simple. I won't understand. Fork this and run wild!

It now creates a JSON file with version numbers for each script present. It also checks which versions are present, which are saved to the config and which the program is expecting. So that's confusing...