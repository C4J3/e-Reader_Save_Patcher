# GBA eReader(+) Save File Patcher. Version 0.2.0-a.

# Import required libraries
import os
import json

# Constants
Script_Version = "0.2.0-a"
Config_file = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0] + '.json'

# Try and make sure there is something resembling a valid config file available. If so load it into memory. If not, run config_maker.
def config_init():

    # If there is no config file, make a new one.
    if not os.path.exists(Config_file):
        return config_maker()
    
    # If there is a config file, try and load it. If it gives this error, make a new one. If it doesn't give the error AND it has the write version number. Then we can actually use it. Hooray!
    with open(Config_file, 'r') as cfg:
        try:
            dat = json.load(cfg)
        except json.JSONDecodeError:
            return config_maker()
        
        if dat['Metadata']['script_version'] == Script_Version and dat['Flags']['initialised']:
            return dat
    
    # If all else fails, just make a new one.
    return config_maker()

# Make a config following my default config format and then pass it to config_writer.
def config_maker():

    # This is what the json file should look like, formatted and all.
    cfg = {
    'Metadata':
    {
        'script_version':   Script_Version
    },
    'Flags': 
    {
        'initialised':       False,
        'datad':             False,
        'filed':             False,
        'completed':         False
    },
    'Files': 
    {
        'calli_save_file':   None,
        'last_patched_file': None, 
        'patched_save_file': None
    },
    'Ranges': 
    {
        'callibration' : 
        {
            'lower_start':   0xD000,
            'lower_end':     0xD04F,
            'upper_start':   0xE000,
            'upper_end':     0xE04F
        },
        
    },
    'Data': 
    {
        'calli_bytes':       None
    }
}
    # Give it to the config writer to actually put it on disk. Then return our shiny new config to use in memory.
    config_file_writer(cfg)
    return cfg

# Literally just write the config to disk.
def config_file_writer(dat):
    with open(Config_file, 'w') as f:
        json.dump(dat, f, indent=3)

# Sanity checking! Makes sure the file name provided matches a file in right of the right size. So I can pretend I tried...
def get_valid_file(prompt):
    while True:
        file_name = input(prompt)
        if os.path.exists(file_name) and os.path.getsize(file_name) == 131072:
            return file_name
        else:
            print(f"Invalid file: {file_name}. Please make sure it exists and is 128KB.")

# Asks the user if they want to reuse whichever file(name) they used last time.
def reuse(file):
    print(f"Save file '{file}' was used last time. Would you like to reuse it?")
    while True:
        resp = input("(Y/N): ").upper()
        if resp == "N":
            return False
        elif resp == "Y":
            return True

# Reads a bin file and returns the read bites as a bytearray.
def read_bytes_from_file(file, start, end):
    with open(file, 'rb') as f:
        f.seek(start)
        return bytearray(f.read(end - start))

# Handles the callibration save file. 
def callif(cfg):
    # Get variables we want to know.
    file = cfg['Files']['calli_save_file']
    binl = cfg['Ranges']['callibration']

    # If we have old data want to reuse it, load it as 'bind'. Otherwise, get a valid file, read the callibration data from it and save it to the config as well as confirm we have succesfully 'datad'. Then write the data changes to disk. Lastly, update the config with the new file. (We don't write that to disk because I decided to write all of them at the same time.)
    if file and reuse(file):
        bind = eval(cfg['Data']['calli_bytes'])
    else:
        file = get_valid_file("Please enter the name of the file you want to use: ")
        bind = read_bytes_from_file(file, binl['lower_start'], binl['lower_end'])
        cfg['Data']['calli_bytes'] = str(bind)
        cfg['Flags']['datad'] = True
        config_file_writer(cfg)
        cfg['Files']['calli_save_file'] = file
    
    # Return the updated config, the binary data, and the bin location. (We need this later and getting it here means if I want to try and make this cursed tool handle card saves onto callibration saves, the reverse of what we're doing, I can give it a similar function and use the card address locations instead.)
    return cfg, bind, binl

# Handles the file we want to patch. Assumed to be one of Im a blissy's 'DLC Hacks' for the GBA Generation three Pokémon games but could be any valid dump such as a friends e-Reader with a cool card they lost in memory.
def inf(cfg):
    # Same as callif, only need the one this time.
    file = cfg['Files']['last_patched_file']

    # Opposite of callif, if we don't have a file or they don't want to reuse it we ask for a new one and add it to the config.
    if not file or not reuse(file):
        file = get_valid_file("Please enter the name of the file you want to use: ")
        cfg['Files']['last_patched_file'] = file

    # Now we have our file, grab the contents and return that along with the updated config again.    
    bind = read_bytes_from_file(file, 0, 131072)
    return cfg, bind

# Handles the 'out file'. The file we will create with our specific e-Readers callibration data AND the swanky e-Card data from the other save.
def outf(cfg):
    #We know this one by now.
    file = cfg['Files']['patched_save_file']

    # Same as infile only we don't care if this one is valid or not.
    if not file or not reuse(file):
        file = input("Please enter the name of the file to write the patched save data: ")
        cfg['Files']['patched_save_file'] = file

    # Now we have our file we can just pass the name and the updated cfg back to the main function again.
    return cfg, file

# Does what it says on the tin (funtion)
def write_bytes_to_file(data, file):
    with open(file, 'wb') as f:
        f.write(data)

# The meat (or protein if you don't like that stuff) of this... thing. Actually does all the stuff!
def main():
    # My very own "Hello World!".
    print(f"eReader Save Patcher V{Script_Version}.")

    # Get the configuration data into memory.
    cfg = config_init()

    # If the config is new, confirm succesful initation of script and completion of config file.
    if cfg['Flags']['initialised'] == False:
        cfg['Flags']['initialised'] = True
        config_file_writer(cfg)

    # Get the callibration data from a save file.
    print("Program will take the callibration data from this save file.")
    cfg, cal_bin, cal_loc = callif(cfg)

    # Get the rest of the data from another save file.
    print("Program will patch callibration data onto this save file.")
    cfg, in_bin = inf(cfg)

    # Find out what we want to call the patched save file.
    print("Program will write the patched save to this save file.")
    cfg, out_file = outf(cfg)

    # Update our configs to remember that we have files available. Should probably use this in the actual code somewhere... huh...
    cfg['Flags']['filed'] = True
    config_file_writer(cfg)

    # Overwrite the new save with the callibration data in memory.
    in_bin[cal_loc['lower_start']:cal_loc['lower_end']] = cal_bin
    in_bin[cal_loc['upper_start']:cal_loc['upper_end']] = cal_bin

    # Write the patched save data to disk.
    write_bytes_to_file(in_bin, out_file)

    # Update our completed flag and write out the config one last time.
    cfg['Flags']['completed'] = True
    config_file_writer(cfg)
    
    # Window dressing so the user knows we didn't just terminate randomly.
    print(f"Success! Your patched save file is called: {out_file}")

# Chat GPT decided to run the script like this instead of just typing 'main()' and either this is genious or dumb. Either way I'm keeping it.
if __name__ == "__main__":
    main()
