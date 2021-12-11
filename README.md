# Cyberdrop-Bunkr-Lolisafe-Python-Uploader
Python script created with Python 3.10 to batch upload every subfolder in the uploads directory to cyberdrop or bunkr as configured and output a txt file with a list of album names and their associated URLs

Many thanks to Marcus' lolisafe bash script

# Installation
1. Download and install Python to Path

![0001_add_Python_to_Path.png](https://s1.putme.ga/0001_add_Python_to_Path.png)

2. Download the latest release from https://github.com/MandoCoding/Cyberdrop-Bunkr-Lolisafe-Python-Uploader/releases and extract
3. Paste folders to be uploaded into the uploads folder
4. Run Start.bat to install all the necessary pre-requisites and start the download script
5. Provide your bunkr or cyberdrop tokens when requested. These can be found in your dashboard on the left, click on 'Manage your token'. 
6. The script outputs a date and time stamped txt file listing the album names and URLs


# Usage
1. Paste folders to be uploaded into the uploads folder
2. Run Uploader.py

# Known Major Issues:
Does not support files larger than 100 MB on bunkr despite bunkrs max file size limit being 5 GB
