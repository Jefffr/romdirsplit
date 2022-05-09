import sys
import xml.etree.ElementTree as ET
import shutil
import os
import argparse

def main():

    parser = argparse.ArgumentParser(description='''
    This script uses the Mame dat file to determine the system of the rom using the "sourcefile".

    You can copy or move the roms to a destination directory.
    This script also moves directories with the same name as the rom (eg kinst.zip moves kinst.zip and kinst/).
    How to use:

    Find the systems you need to move into the Mame xxx.dat file:
    ex. for NeoGeo => in dat search a neogeo game > sourcefile="neogeo.cpp" use "neogeo"
    some useful systems: neogeo, cps1, cps2, cps3
    ''' + bcolors.WARNING + '''
    use this script at your own risk
    ''' + bcolors.ENDC, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-r", "--roms-folder", help="Location of roms folder. Use '.' for current folder", required=True)
    parser.add_argument("-d", "--dat-file", help="Location of dat file", required=True)
    parser.add_argument("-s", "--systems", nargs='*', help="List of systems to be splitted, splitted by space. ex: -c cps1 neogeo cps2", required=True)
    parser.add_argument("-ext", "--roms-extension", help="File extension of roms. Default = zip", default="zip")
    parser.add_argument("-dest","--destination-folder", help="Destination Folder. If not set, roms are moved into a sub-folder of roms folder.")
    parser.add_argument("-m", "--move", action="store_true", help="Move files instead of copy.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show current action.")


    args = vars(parser.parse_args())
    romsFolder = args['roms_folder']
    fileDat = args['dat_file']
    cores = args['systems']
    fileExtension = args['roms_extension']
    destinationFolder = args['destination_folder'] if args['destination_folder'] != None else romsFolder
    move = args['move']

    global verbose
    verbose = args['verbose']

    if not os.path.exists(romsFolder):
        sys.exit("Roms folder not exist.")
    if not os.path.isfile(fileDat):
        sys.exit("Dat not exist")
    if not os.path.exists(destinationFolder):
        print("The destination directory does not exist. we will create it.")

    print("\n------------------ Selected Options ------------------")
    print("Roms folder: " + bcolors.OKGREEN + romsFolder + bcolors.ENDC)
    print("Destination folder: " + bcolors.OKGREEN + destinationFolder + bcolors.ENDC)
    print("Dat file: " + bcolors.OKGREEN + fileDat + bcolors.ENDC)
    print("Systems to be split: " + bcolors.OKGREEN + str(cores) + bcolors.ENDC)
    print("Roms files extension: " + bcolors.OKGREEN + fileExtension + bcolors.ENDC)
    print("Mode: " + bcolors.OKGREEN + ("Move" if move else "Copy") + bcolors.ENDC)
    print("------------------------------------------------------\n")


    tree = ET.parse(fileDat)
    root = tree.getroot()

    for core in cores :
        unVerbosePrint("")
        unVerbosePrint("Treatment of: " + bcolors.OKGREEN + core + bcolors.ENDC)
        currentSystemNode = root.findall("machine[@sourcefile='" + core + ".cpp']")
        
        destinationSystemPath = destinationFolder + os.sep + core
        currentDestinationSystemPathExist = os.path.exists(destinationSystemPath)

        for child in currentSystemNode:
            colorPoint = bcolors.OKCYAN
            romName = child.attrib['name']
            romFileName =  romName + "." + fileExtension
            romSourcePath = romsFolder + os.sep + romFileName
            romDestinationPath = destinationSystemPath + os.sep + romFileName

            if os.path.exists(romSourcePath):
                if not currentDestinationSystemPathExist and not os.path.exists(destinationSystemPath):
                    verbosePrint("Create destination Folder: " + destinationSystemPath)
                    os.makedirs(destinationSystemPath)
                    currentDestinationSystemPathExist = True

                romSubFolder = romsFolder + os.sep + romName
                if os.path.exists(romDestinationPath):
                    colorPoint = bcolors.FAIL
                    verbosePrint("SKIP > Exist: " + romDestinationPath)
                else:
                    if move:
                        verbosePrint("Moving: " + romFileName + " (" + child.find("description").text + ")")
                        shutil.move(romSourcePath, romDestinationPath)
                        if not romSubFolder.endswith(core) and os.path.exists(romSubFolder): # For folder in relation of rom like CHD
                            verbosePrint("\tMoving: " + romSubFolder + " (sub folder of rom)")
                            shutil.move(romSubFolder, destinationSystemPath + os.sep + romName)
                        colorPoint = bcolors.OKBLUE
                    else:
                        verbosePrint("Copy:\t" + romFileName + " (" + child.find("description").text + ")")
                        shutil.copy(romSourcePath, romDestinationPath)
                        if not romSubFolder.endswith(core) and os.path.exists(romSubFolder): # For folder in relation of rom like CHD
                            verbosePrint("\t" + romSubFolder + " (sub folder of rom)")
                            shutil.copytree(romSubFolder, destinationSystemPath + os.sep + romName)
                        colorPoint = bcolors.OKGREEN
            unVerbosePrint(colorPoint + "." + bcolors.ENDC, True)

def unVerbosePrint(text, sameLine=False):
    if not verbose:
        if sameLine:
            print(text, end="")
        else:
            print(text)
    return

def verbosePrint(text):
    if verbose:
        print(text)
    return

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    main()