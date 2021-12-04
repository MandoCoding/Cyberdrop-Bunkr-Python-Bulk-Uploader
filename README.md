# Cyberdrop-Bunkr-Lolisafe-Python-Uploader
Python script to batch upload every subfolder in the uploads directory to cyberdrop or bunkr as configured
Many thanks to Marcus' lolisafe bash script

# Information
Created using Python 3.10

# Random crap, remove later
It works, more than I ever expected. There's still a lot to do:

- Bunkrs chunked uploads break the script - connection reset error :feelsrageman 
- New output txt for every batch upload?
- Error Handling - No folders to upload
- Error Handling - file upload fail, retry?
- Error Handling - file upload duplicate, what does it do?
- Create bat file to install pre-requisites
- Tidy up the prints 
- Tidy up variables
- Improve upload progress to fill bar
- Parallel uploads?
- Create exe
- Allow updates to folders - is this possible via API or will it have to scrape current album contents and upload difference?

# Done
- Check for and create /Uploads/ directory
- Close out line "Uploads complete, press enter etc..."
- Show upload progress - basic version is number of files
- Error Handling (album already exists = album ID fail right now)
- Cyberdrop - Write Uploaded album urls to file for easy posting :EZ:
- bunkr - Write Uploaded album urls to file for easy posting :EZ: - I hate how I've had to do this but it works so far as I can tell

# Installation
1. Download and install Python to Path 
![0001_add_Python_to_Path.png](https://s1.putme.ga/0001_add_Python_to_Path.png)
2. Download the latest release from https://github.com/MandoCoding/Cyberdrop-Bunkr-Lolisafe-Python-Uploader/releases (or just master for now) and extract
3. Paste folders to be uploaded into the uploads folder
4. Run Start.bat to install all the necessary pre-requisites and start the download script
5. Provide your bunkr or cyberdrop tokens when requested. These can be found in your dashboard on the left, click on 'Manage your token'. 
6. The script outputs a timestamped txt file listing the album names and URLs


# Usage
1. Paste folders to be uploaded into the uploads folder
2. Run Uploader.py
