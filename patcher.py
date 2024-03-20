# Formerly main(). This actually patches the save.

Script_Version = "1.0"
Prompt = "Please enter the name of the file you want to use: "
# Import all the other scripts. Shouldn't need any other libraries for functionality.
import myLib
import conf
import files

# My very own "Hello World!".
print(f"eReader Save Patcher V{Script_Version}.")

# Get the configuration data into memory.
cfg = conf.config_init()

# If the config is new, confirm succesful initation of script and completion of config file.
if not cfg['Flags']['initialised']:
    cfg['Flags']['initialised'] = True
    conf.config_file_writer(cfg)

# Get the calibration data from a save file.
print("Program will take the calibration data from this save file.")
cfg, cal_bin, cal_loc = files.calif(cfg, Prompt)

# Get the rest of the data from another save file.
print("Program will patch calibration data onto this save file.")
cfg, in_bin = files.inf(cfg, Prompt)

# Find out what we want to call the patched save file.
print("Program will write the patched save to this save file.")
cfg, out_file = files.outf(cfg, Prompt)

# Update our configs to remember that we have files available. Should probably use this in the actual code somewhere... huh...
cfg['Flags']['filed'] = True
conf.config_file_writer(cfg)

# Overwrite the new save with the calibration data in memory.
in_bin[cal_loc['lower_start']:cal_loc['lower_end']], in_bin[cal_loc['upper_start']:cal_loc['upper_end']] = cal_bin, cal_bin

# Write the patched save data to disk.
myLib.write_bytes_to_file(in_bin, out_file)

# Update our completed flag and write out the config one last time.
cfg['Flags']['completed'] = True
conf.config_file_writer(cfg)

# Window dressing so the user knows we didn't just terminate randomly.
print(f"Success! Your patched save file is called: {out_file}")

exit()