# Cyberdrop-Bunkr-Lolisafe-Python-Uploader

It works, more than I ever expected. There's still a lot to do:

- Bunkrs chunked uploads break the script - connection reset error :feelsrageman 
- New output txt for every batch upload?
- Error Handling - No folders to upload
- Error Handling - file upload fail, retry?
- Error Handling - file upload duplicate, what does it do?
- batch file to install pre-requisites
- Tidy up the prints 
- Tidy up variables
- Improve upload progress to fill bar
- Parallel uploads?
- Create exe
- Allow updates to folders - is this possible via API or will it have to scrape current album contents and upload difference?



Many thanks to Marcus' lolisafe bash script



Done:
- Check for and create /Uploads/ directory
- Close out line "Uploads complete, press enter etc..."
- Show upload progress - basic version is number of files
- Error Handling (album already exists = album ID fail right now)
- Cyberdrop - Write Uploaded album urls to file for easy posting :EZ:
- bunkr - Write Uploaded album urls to file for easy posting :EZ: - I hate how I've had to do this but it works so far as I can tell
