import json
from os import path

Script_Version = "1.0"
Config_file = (f'{path.splitext(path.basename(path.abspath(__file__)))[0]}.json')

# Try and make sure there is something resembling a valid config file available. If so load it into memory. If not, run config_maker.
def config_init():

    # If there is no config file, make a new one.
    if not path.exists(Config_file):
        return config_maker()
    
    # If there is a config file, try and load it. If it gives a JSON Decode error, make a new one. If it doesn't give the error AND it has the write version number. Then we can actually use it. Hooray!
    with open(Config_file, 'r') as cfg:
        try:
            dat = json.load(cfg)
        except json.JSONDecodeError:
            return config_maker()
        
        json_versions = dat['Metadata']
        from patcher import Script_Version as patcher_ver
        from myLib import Script_Version as myLib_ver
        from files import Script_Version as files_ver

        script_versions = dict([('patcher.py_version', patcher_ver), ('myLib.py_version', myLib_ver), ('files.py_version', files_ver), ('conf.py_version', Script_Version)])
        if json_versions != script_versions:
            print("Error. Script version mismatch.")
            return config_maker
        else:
            return dat
        '''if dat['Metadata']['conf.py_version'] == Script_Version and dat['Flags']['initialised']:
            return dat'''
    
    # If all else fails, just make a new one.
    return config_maker()

# Make a config following my default config format. Then write it to disk and pass it back to the main program.
def config_maker():

    # Import each scripts version number. Kind of obvious in hindsight but importing them all at the start breaks things with circular references...
    from patcher import Script_Version as patcher_ver
    from myLib import Script_Version as myLib_ver
    from files import Script_Version as files_ver

    # This is what the json file should look like, formatted and all.
    cfg = {
    'Metadata':
    {
        'patcher.py_version': patcher_ver,
        'myLib.py_version': myLib_ver,
        'files.py_version': files_ver,
        'conf.py_version':  Script_Version
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