import os

#It do the thing
def prog():

    #Range of callibration data in stock eReader cart save file:
    callirange = [0xD000, 0xD04F, 0xE000, 0xE04F]

    #idk, I'm too lazy. The work_dir one is because I broke it once and got scared...
    inpp = "Please enter the file name: "
    work_dir = os.getcwd()+'\\'
    
    
    #Ask for names of different files. Requires full file names but not file paths. Automatically uses the working directory of the script as file path.

    #The save file with calliration data we want to use.
    print("Program will take the callibration data from this save file.")
    callifile = work_dir+input(inpp)

    #The save file we want to patch the callibration data onto.
    print("Program will patch callibration data onto this save file.")
    infile = work_dir+input(inpp)

    #The name of the file we want to write the 'patched' save data to.
    print("Program will write the patched save to this save file.")
    outfile = work_dir+input(inpp)

    #Creates some variable of a type don't know what is that has the callibration data from the appropriate save file. 
    calli = (byter(callirange, callifile))

    #Open the file we want to patch the callibration data onto and read all the data (it's 128kb so should be safe in any modern amount of ram) then store it in memory.
    with open(infile, 'rb') as f:
        inbin = bytearray(f.read())

    #Write the callibration data to the save in memory.
    outbin = bytew(callirange, calli, inbin)

    #Write the patched save data to a new file on disk.
    with open(outfile, 'wb') as prod:
        prod.write(outbin)

#My byte reader function. Give it a range of addresses to look up and a file to look them up in.
def byter(range, book):

    #Open the file in read-only mode, look for the first address and read from their to last address provided. Returning the result.
    with open(book, 'rb') as calli:
        calli.seek(range[0])
        return calli.read(range[1] - range[0])
    
#My byte writer function. Give it a a range, some binary data and some more binary data and it'll write the first set of data onto the the second at the adress given.
def bytew(range, calli, bin):

    #Replace the data in addresses given to the other data's values. Then return the new data.
    bin[range[0]:range[1]] = calli
    bin[range[2]:range[3]] = calli
    return bin

#Actually does something!
prog()