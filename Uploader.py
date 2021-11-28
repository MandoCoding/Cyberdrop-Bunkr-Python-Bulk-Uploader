import linecache
import os
import requests

base_url = "https://cyberdrop.me" #This can be set to https://bunkr.is or any other lolisafe instance. Remember to update the userdata file with the appropriate token

#Start some lists
Dirlist = list()
Albumfaillist = list()
Albumsuccesslist = list()
Albumurllist = list()
Albumsuccesscount = 0

#Check for and create the upload directory
root = os.path.dirname(__file__)
upload_dir = root + "/Uploads/"
isExist = os.path.exists(upload_dir)
if isExist:
    print("Folder already exists")
if not isExist:
    os.makedirs(upload_dir)
    input('The uploads folder has been created. Copy in the folders you want to upload and then press enter to continue')

#Read the userdata file
token = linecache.getline('userdata.txt', 1).rstrip()

#If userdata file is empty request user input
if token == "":
    token = input('Enter Token and press enter: ')

#Write data back to userdata file, can't write to specific line so all must be written again
userinp = open("userdata.txt","w+")
userinp.write(token)
userinp.close()

#Sort the base directory
cwd = os.getcwd()  #gets current directory
upload_dir = cwd + "/Uploads/"


#Create a list of upload subfolders
for root, subdirectories, files in os.walk(upload_dir):
    for subdirectory in subdirectories:
        dir = os.path.join(root, subdirectory)
        Dirlist.append(dir)
        album_count = len(Dirlist)

#For each subfolder print the directory, album name and files
for i in Dirlist:
    dir = i + '/'
    os.chdir(dir) #change current directory to the subfolder to make the following code easier
    album_name = os.path.basename(os.getcwd())

    #Create Album JSON (whatever that means)
    album_json = '{ "name": "' + album_name + '", "description": "", "public": true, "download": true }';  # copied from Marcus
    print()
    print("Creating album: ", album_name)
    albums_url = base_url+"/api/albums"

    #create the album
    albumheaders = {'Content-Type': 'application/json', 'token': f"{token}",}
    data = album_json
    r = requests.post(albums_url, headers=albumheaders, data=data)  # creates the album on cyberdrop/bunkr etc.
    data = r.json()

    #was it a success?
    success = data['success']
    if success == True:
        album_id = data['id']
        print('Album', album_name, 'created successfully with ID:', album_id)
        print()
    elif success == False:
        print("Album already exists")
        #Need to work out how to skip to next item

    #Now we start on the files by creating a list of them
    Filelist = list()
    for root, subdirectories, files in os.walk(dir):
        for file in files:
            Filelist.append(file)
    album_file_number = len(Filelist)
    print('Uploading ', album_file_number, ' files')

    #the generic api upload url
    upload_file_url = base_url+"/api/upload"

    #give it some headers
    fileheaders = {'token': f"{token}", 'albumid': f"{album_id}",}

    #lets do this
    file_number = 1
    Faillist = list()
    for file in Filelist:
        print()
        print("uploading file",file_number, 'of', album_file_number,':', file)
        file_number = file_number + 1
        success_count = 0
        files = {'files[]': open(file, 'rb')}
        response = requests.post(upload_file_url, headers=fileheaders, files=files)
        data2 = response.json()
        success = data2['success']
        if success == True:
            print(file, "uploaded succesfully")
            success_count = success_count + 1
        elif success == False:
            print(file, "upload failed")
            Faillist.append(file)
    print()

    #Get the album url and add to list
    albumurlheaders = {'token': f"{token}", }
    albumr = requests.get(albums_url, headers=albumurlheaders)  # gets list of albums
    albumdata = albumr.json()
    for attrs in albumdata['albums']:
        if attrs['id'] == album_id:
            albumurl = base_url + '/a/' + attrs['identifier']
            break
    else:
        print('Nothing found!')
        albumurl = ""
    Albumurllist.append(albumurl)

    #Did album upload every file successfully or not?
    if (file_number - 1) == album_file_number:
        print('Album \'',album_name,'\' uploaded successfully:', albumurl)
        Albumsuccesslist.append(album_name) #remove later or change to success list
        Albumsuccesscount = Albumsuccesscount + 1
    else:
        print('Album not fully uploaded.', success_count, 'files uploaded successfully. The following files failed to upload:', Faillist)
        Albumfaillist.append(album_name)
    print()
    print()

#Success/Fail Stats
if Albumsuccesscount == album_count:
    print('All albums uploaded successfully: ', Albumsuccesslist)
    print(Albumurllist)
else:
    print('The following albums uploaded successfully:', Albumsuccesslist)
    print('The following albums failed to upload successfully:', Albumfaillist)

exitText = input("\nPress enter to quit.") #Need to rework this based on earlier