import os
from tkinter import Tk, filedialog
from datetime import datetime
import sysrsync
import subprocess
import screen


# Get a list of non-hidden files in the root folder and all sub-folders
def getFileList(sourceFolder):
    subFolders = next(os.walk(sourceFolder))[1]
    subFolders = [os.path.join(sourceFolder, f, '') for f in subFolders if not f.startswith('.')]
    subFolders.insert(0,sourceFolder)

    # Get all the non-hidden files in the root and all the sub-folders
    allFiles = list()

    for folder in subFolders:
        print(f'{screen.colour.BLUE}Processing Folder: {folder} {screen.colour.END}')

        # Get all the files in the folder (no super easy way to do a complex filter here so do it step-by-step
        files = next(os.walk(folder))[2]
        # Extract just the .mov and .avi files
        files = [f for f in files if not f.lower().startswith('.')]
        # Append the full path to the filename
        files = [os.path.join(folder, f) for f in files]

        allFiles = allFiles + files

    return allFiles



#Let user select a folder and return a clean path to that folder
def getFolder():

    # Default to the users home folder
    default_folder = '.'

    #Open a Dialogue Box to select a folder
    window = Tk()
    window.withdraw()  # Hide the tk window
    folder = filedialog.askdirectory(initialdir=default_folder)
    window.destroy()

    # Check we got something
    if not folder:
        print('User Cancelled !')
        exit()

    # Make folder a full path
    folder = os.path.join(folder, '')

    # Should not be able to select anything other than a folder, but check and quit if a non-folder is selected
    if not os.path.isdir(folder):
        print ('Selected Item is NOT a folder')
        exit()

    return folder



# Stop some obviously stupid things - this is by no means comprehensive
def validateSource_and_Target(sourceFolder, destinationFolder):

    if sourceFolder == destinationFolder:
        print ( f'Source and Destination cannot be the same')
        exit()

    # Note: this only works on MacOS 
    if not destinationFolder.startswith('/Volumes/'):
        print (f'Destination folder is not a removable drive')
        exit()

    if '/Volumes/Time Machine' in destinationFolder:
        print (f'Destination folder is a Time Machine volume - you probably dont want to do this')
        exit()


# Copy the files using rsync
# Just catch any error and exit
# -a = archive (copy everything incl sub-folders)
# -v = verbose
# -I = Ignore time stamps and verify/copy everything
# --exclusions .* = Do not copy hidden files or folders
#  
def copyFolder(sourceFolder, destinationFolder):

    try:
        print()
        sysrsync.run(source=f'{sourceFolder}',
                    destination=f'{destinationFolder}',
                    sync_source_contents=False, 
                    options=['-avIP'],
                    exclusions=['.*'] )

    except:
        print (f'{screen.colour.RED}Something went wrong - files did NOT copy !!{screen.colour.END}')
        exit()




def checkSumFiles(sourceFiles, sourceFolder, destFolder):
    # Extract the name of the folder to be copied - this has to be added to the destination folder to get the full destination file path 
    # e.g '/Users/jamdoran/Documents/Git/mp4copy/' will deliver mp4copy
    # Then os.path.join to add the trailing /
    folder = sourceFolder.split('/')[-2] + '/'

    print ()
    print ()
    print (f'{screen.colour.UNDERLINE}Comparing copied files with shasum based checksum {screen.colour.END}')
    print ()

    for file in sourceFiles:
        destFile = file.replace(sourceFolder, destFolder+folder)

        result = subprocess.run(['shasum', f'{file}'], stdout=subprocess.PIPE)
        sourceSHA = result.stdout.decode('utf-8').split(" ",1)[0]

        result = subprocess.run(['shasum', f'{destFile}'], stdout=subprocess.PIPE)
        destSHA = result.stdout.decode('utf-8').split(" ",1)[0]

        print ()
        print (f'Source File: {file}  (sha = {sourceSHA})')
        print (f'Dest File  : {destFile}  (sha = {destSHA})')
        if sourceSHA == destSHA:
            print (f'{screen.colour.BLUE}Files Match{screen.colour.END}')
        else:
            print (f'{screen.colour.RED}Files DO NOT Match{screen.colour.END}')


def clearScreen():
    os.system('clear')




# Yep, it's the main() function
def main():
    
    startTime   = datetime.now()

    # Let user select both source and destination folders for rsync 
    sourceFolder        = getFolder()
    destinationFolder   = getFolder()

    # Do some basic checks on the source and dest folders 
    validateSource_and_Target(sourceFolder, destinationFolder)

    clearScreen()
    print (screen.logo)
    print ()
    print ()
    print ( f'Source Folder : {sourceFolder}' )
    print ( f'Dest Folder   : {destinationFolder}' )
    print ()

    #Get a list of all the files in the sourceFolder and sub-folders with full path 
    sourceFiles = getFileList(sourceFolder)

    # print()
    # for f in sourceFiles:
    #     print (f)

    # Copy the files with rsync - exit() on any failure
    copyFolder(sourceFolder, destinationFolder)

    # Checksum all the files 
    checkSumFiles(sourceFiles, sourceFolder, destinationFolder)

    print()
    print( f'{screen.colour.BLUE}Complete in {datetime.now() - startTime } seconds !{screen.colour.END}' )
    print()



# Run main() as the main function
if __name__ == '__main__':
    main()


