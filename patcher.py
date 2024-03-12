import bins
import conf

Script_Version = "0.3"

# My very own "Hello World!".
print(f"eReader Save Patcher V{Script_Version}.")

# Get the configuration data into memory.
cfg = conf.config_init()

# If the config is new, confirm succesful initation of script and completion of config file.
if not cfg['Flags']['initialised']:
    cfg['Flags']['initialised'] = True
    conf.config_file_writer(cfg)

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
conf.config_file_writer(cfg)

# Overwrite the new save with the callibration data in memory.
in_bin[cal_loc['lower_start']:cal_loc['lower_end']] = cal_bin
in_bin[cal_loc['upper_start']:cal_loc['upper_end']] = cal_bin

# Write the patched save data to disk.
bins.write_bytes(in_bin, out_file)

# Update our completed flag and write out the config one last time.
cfg['Flags']['completed'] = True
conf.config_file_writer(cfg)

# Window dressing so the user knows we didn't just terminate randomly.
print(f"Success! Your patched save file is called: {out_file}")