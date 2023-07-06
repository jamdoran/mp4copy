import os
from tkinter import Tk, filedialog
from datetime import datetime
import sysrsync


class colour:
	RED = '\033[91m'
	END = '\033[0m'


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
def copyFiles(sourceFolder, destinationFolder):
    try:
        sysrsync.run(source=f'{sourceFolder}',
                    destination=f'{destinationFolder}',
                    sync_source_contents=False, 
                    options=['-avIP'],
                    exclusions=['.*'] )

    except:
        print (f'{colour.RED}Something went wrong - files did NOT copy !!{colour.END}')
        exit()



# Run a second copy to verify the files were copied correctly - use checksum only, no dates
#  
def copyVerifyFiles(sourceFolder, destinationFolder):
    try:
        sysrsync.run(source=f'{sourceFolder}',
                    destination=f'{destinationFolder}',
                    sync_source_contents=False, 
                    options=['-avhcP'],
                    exclusions=['.*'] )

    except:
        print (f'{colour.RED}Something went wrong - files did NOT copy !!{colour.END}')
        exit()


# Yep, it's the main() function
def main():
    
    startTime   = datetime.now()

    # Let user select both source and destination folders for rsync 
    print ( r'Select Source Folder' )
    sourceFolder        = getFolder()

    print ( r'Select USB Root Folder' )
    destinationFolder   = getFolder()

    validateSource_and_Target(sourceFolder, destinationFolder)

    print ()
    print ( f'Source Folder : {sourceFolder}' )
    print ( f'Dest Folder   : {destinationFolder}' )
    print ()
    print ()

    # Copy the files - exit() on failure
    copyFiles(sourceFolder, destinationFolder)
    print()
    print()
    print( f'Copy Complete in {datetime.now() - startTime } seconds' )
    print()
    print()
    print()

    # Copy the files twice again for verification, use checksum only to compare files - exit() on failure
    print(f'Starting second copy for checksum verification')
    print()
    print()
    copyVerifyFiles(sourceFolder, destinationFolder)
    print()
    print(f'Starting third copy for checksum verification')
    print()
    print()
    copyVerifyFiles(sourceFolder, destinationFolder)
    print()
    print()

    print('All Done!!')
    print()



# Run main() as the main function
if __name__ == '__main__':
    main()


