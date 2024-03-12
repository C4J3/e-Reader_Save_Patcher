import conf

class Savbin:
     def __init__(self, size, fileName, stored, saveFunc):
          
          self.size = 0x20000 #cfg->ranges->input->end
          self.fileName = #function to get a file name?
          self.stored = #Check if it came from an old .json config or not. Not sure if I will need this.
          self.saveFunc = #Get from function calling this I think. Is this the calibration save, the 'to be patched' save or the 'patched' save to be written to disk.
          