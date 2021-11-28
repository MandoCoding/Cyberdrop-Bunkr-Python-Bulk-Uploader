import linecache
import os
import requests

base_url = "https://cyberdrop.me"

#Read the userdata file
token = linecache.getline('userdata.txt', 1).rstrip()

#If userdata file is empty request user input
if token == "":
    token = input('Enter Token and press enter: ')

#Write data back to userdata file, can't write to specific line so all must be written again
userinp = open("userdata.txt","w+")
userinp.write(token)
userinp.close()

#Confirmation of user info, remove later
print()
print('Token:    ', token)
print()

#Sort the base directory and start a list for upload subfolders (Dirlist)
cwd = os.getcwd()  #gets current directory
upload_dir = cwd + "/Uploads/"
Dirlist = list()

#Create a list of upload subfolders
for root, subdirectories, files in os.walk(upload_dir):
    for subdirectory in subdirectories:
        dir = os.path.join(root, subdirectory)
        Dirlist.append(dir)

#For each subfolder print the directory, album name and files
for i in Dirlist:
    dir = i + '/'
    print("Directory:  ", dir)
    os.chdir(dir) #change current directory to the subfolder to make the following code easier
    album_name = os.path.basename(os.getcwd())
    print("Album Name: ", album_name)
    print()

    #Create Album JSON (whatever that means)
    album_json = '{ "name": "' + album_name + '", "description": "", "public": true, "download": true }';  # copied from Marcus
    print("Creating album: ", album_name)
    albums_url = base_url+"/api/albums"

    #create the album
    albumheaders = {
        'Content-Type': 'application/json',
        'token': f"{token}",
    }
    data = album_json
    r = requests.post(albums_url, headers=albumheaders, data=data)  # creates the album on Cyberdrop
    data = r.json()

    #was it a success?
    success = data['success']
    print('Success?: ', success)
    if success == True:
        album_id = data['id']
        print(album_id)
    elif success == False:
        print("Album already exists")

    #Now we start on the files by creating a list of them
    Filelist = list()
    for root, subdirectories, files in os.walk(dir):
        for file in files:
            Filelist.append(file)

    #the generic api upload url
    upload_file_url = base_url+"/api/upload"

    #give it some headers
    fileheaders = {
        'token': f"{token}",
        'albumid': f"{album_id}",
    }

    #lets do this
    for file in Filelist:
        print("uploading: ", file)
        files = {'files[]': open(file, 'rb')}
        response = requests.post(upload_file_url, headers=fileheaders, files=files)
        data2 = response.json()
        success = data2['success']
        if success == True:
            print(file, "uploaded succesfully")
        elif success == False:
            print(file, "upload failed")