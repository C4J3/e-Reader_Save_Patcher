import json
import myLib
import os

Script_Version = "1.0"
Config_file = (f'{os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]}.json')

# I gave up. Need this everywhere but if I make it global it all breaks. This is the best I could come up with.
def bad():
    from patcher import Script_Version as patcher_ver
    from myLib import Script_Version as myLib_ver
    from files import Script_Version as files_ver
    
    present_scripts = {
        'patcher.py': patcher_ver,
        'myLib.py': myLib_ver,
        'files.py': files_ver,
        'conf.py':  Script_Version
    }
    
    return present_scripts

# If the config exists but is bad we'll ask the user what they want to create a new config. If they don't say yes we terminate the program.
def dud_config(passthrough):
    
    if myLib.reuse("Would you like to create a new config? (THIS WILL DELETE THE CURRENT ONE IF IT IS PRESENT!)") is True:
        return config_maker(passthrough)
    else:
        print("Terminating script.")
        exit()

# Try and make sure we have some kind of valid configuration file. Loads of things to do but it should do enough of them.
def config_init():

    # If there is no config file, make a new one.
    if not os.path.exists(Config_file):
        print("Generating config...")
        return config_maker(bad())

    # If there is a config file, try and load it. If it gives a JSON Decode error, make a new one. If it doesn't give the error AND it has the write script number. Then we can actually use it. Hooray! 
    with open(Config_file, 'r') as cfg:
        try:
            dat = json.load(cfg)
        except json.JSONDecodeError:
            print("Bad config file found.")
            return dud_config(bad())

    script_scripts = dict([('patcher.py', "1.0"), ('myLib.py', "1.0"), ('files.py', "1.0"), ('conf.py', Script_Version)])
    json_scripts = dat['Metadata']
    present_scripts = bad()
    
    # Import each scripts version number. Kind of obvious in hindsight but importing them all at the start breaks things with circular references...
    if script_scripts != present_scripts:
        print(f"conf.py is expecting {script_scripts}. The scripts present are {present_scripts}. Please correct this before proceeding.\nTerminating...")
        exit()

    for script in json_scripts:
        print(f"testing {script} script")
        try:
            if json_scripts[script] != script_scripts[script]:
                print(f"Error. {script} does not match.")
                return dud_config()
        except KeyError:
            print("Invalid or incompatible config JSON. Please correct or remove the config JSON from the current directory.")
            return dud_config
        else:
            print(f"Script {script} verions match. Proceeding...")
        print("All scripts match, proceeding to main program.")    
        return dat

# Make a config following my default config format. Then write it to disk and pass it back to the main program.
def config_maker(default_dict):

    # This is what the json file should look like, formatted and all.
    cfg = {
    'Metadata':

    default_dict,

    'Flags': 
    {
        'initialised':       False,
        'datad':             False,
        'filed':             False,
        'completed':         False
    },
    'Files': 
    {
        'cali_save_file':   None,
        'last_patched_file': None, 
        'patched_save_file': None
    },
    'Ranges': 
    {
        'calibration': 
        {
            'lower_start':   0xD000,
            'lower_end':     0xD05F,
            'upper_start':   0xE000,
            'upper_end':     0xE05F
        },
        'input': 
        {
            'start':         0x0,
            'end':           0x20000
        },
        
    },
    'Data': 
    {
        'cali_bytes':       None
    }
}
    # Give it to the config writer. Then return our shiny new config to use in memory.
    config_file_writer(cfg)
    return cfg

# Literally just write the config to disk.
def config_file_writer(dat):
    with open(Config_file, 'w') as f:
        json.dump(dat, f, indent=3)