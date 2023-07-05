import glob, os
from tkinter import Tk, filedialog
from datetime import datetime
import sysrsync


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




# Yep, it's the main() function
def main():
    
    startTime   = datetime.now()

    # Let user select both source and destination folders for rsync 
    print ( r'Select Source Folder' )
    sourceFolder        = getFolder()

    print ( r'Select USB Root Folder' )
    destinationFolder   = getFolder()

    validateSource_and_Target(sourceFolder, destinationFolder)

    sysrsync.run(source=f'{sourceFolder}',
                destination=f'{destinationFolder}',
                sync_source_contents=False)


    print ( f'Source Folder is {sourceFolder}' )
    print ( f'Destination Folder is {destinationFolder}' )

    print( f'Complete in {datetime.now() - startTime } seconds' )
    print()
    print('All Done!!')
    print()





# Run main() as the main function
if __name__ == '__main__':
    main()


