Script_Version = "1.0"

import myLib
import conf

def calif(cfg, Prompt):
    # Get variables we want to know.
    file = cfg['Files']['cali_save_file']
    binl = cfg['Ranges']['calibration']

    # If we have old data and want to reuse it, load it as 'bind'. Otherwise, get a valid file, read the calibration data from it and save it to the config as well as confirm we have succesfully 'datad'. Then write the data changes to disk. Lastly, update the config with the new file. (We don't write that change to disk because I decided to write all of the file changes at the same time later.)
    if file and myLib.reuse(f"Callibration data used last time was from '{file}'. Would you like to reuse it?"):
        bind = eval(cfg['Data']['cali_bytes'])
    else:
        file = myLib.get_valid_file(Prompt)
        bind = myLib.read_bytes_from_file(file, binl['lower_start'], binl['lower_end'])
        cfg['Data']['cali_bytes'] = str(bytes(bind))
        cfg['Flags']['datad'] = True
        conf.config_file_writer(cfg)
        cfg['Files']['cali_save_file'] = file
    
    # Return the updated config, the binary data, and the bin location. (We need this later and getting it here means if I want to try and make this cursed tool handle card saves onto calibration saves, the reverse of what we're doing, I can give it a similar function and use the card address locations instead.)
    return cfg, bind, binl

def inf(cfg, Prompt):
    # Same as calif, only need the one this time.
    file = cfg['Files']['last_patched_file']

    # Opposite of calif, if we don't have a file or we don't want to reuse it we ask for a new one and add it to the config.
    if not file or not myLib.reuse(f"Save file '{file}' was patched last time. Would you like to reuse it?"):
        file = myLib.get_valid_file(Prompt)
        cfg['Files']['last_patched_file'] = file

    # Now we have our file, grab the contents and return that along with the updated config again.    
    bind = myLib.read_bytes_from_file(file, cfg['Ranges']['input']['start'], cfg['Ranges']['input']['end'])
    return cfg, bind

# Handles the 'out file'. The file we will create with our specific e-Readers calibration data AND the swanky e-Card data from our other save.
def outf(cfg, Prompt):
    #We know this one by now.
    file = cfg['Files']['patched_save_file']

    # If the user has an old file in the config and they want to reuse it then we pass it to get_invalid_file(). If it returns true we just return the original data and config.
    if file is not None and myLib.reuse(f"Patched save was written to '{file}' last time. Would you like to reuse it?"):
        if myLib.get_invalid_file(file):
            return cfg, file
        
    # If the user wants to use a new file we check it with get_invalid_file(). Once we get a result we're happy with, we update the cfg with the new file name.
    file = input(Prompt)
    while not myLib.get_invalid_file(file):
        file = input(Prompt)
    cfg['Files']['patched_save_file'] = file
    # Now we have our file we can just pass the name and the updated cfg back to the main function again.
    return cfg, file