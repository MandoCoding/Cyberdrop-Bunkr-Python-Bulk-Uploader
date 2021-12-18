import linecache
import os
import math
import requests
import datetime
import time
from colorama import init
from colorama import Fore, Back, Style

init()

base_url = None

#Start some lists
Dirlist = list()
Albumfaillist = list()
Albumalreadyuplist = list()
Albumsuccesslist = list()
Albumurllist = list()
Albumsuccesscount = 0

#Check for and create the upload directory
root = os.path.dirname(__file__)
upload_dir = root + "/Uploads/"
isExist = os.path.exists(upload_dir)
if not isExist:
    os.makedirs(upload_dir)
    input(Fore.GREEN +'The uploads folder has been created. Copy in the folders you want to upload and then press enter to continue')

#Read the userdata file
site = linecache.getline('userdata.txt', 1).rstrip()
token = linecache.getline('userdata.txt', 2).rstrip()


#If userdata file is empty request user input
if site == "":
    site = input(Fore.GREEN +'Enter site (i.e. cyberdrop or bunkr) and press enter: ')
if token == "":
    token = input(Fore.GREEN +'Enter Token and press enter: ')

#Write data back to userdata file, can't write to specific line so all must be written again
userinp = open("userdata.txt","w+")
userinp.write(site)
userinp.write("\n")
userinp.write(token)
userinp.close()

if site == "cyberdrop":
    base_url = str("https://cyberdrop.me")
if site == "bunkr":
    base_url = str("https://bunkr.is")

#Sort the base directory
cwd = os.getcwd()  #gets current directory
base_dir = cwd
upload_dir = cwd + "/Uploads/"

#Create a list of folders to be uploaded
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
    albums_url = base_url+ "/api/albums"

    #create the album
    albumheaders = {'Content-Type': 'application/json', 'token': f"{token}",}
    data = album_json
    r = requests.post(albums_url, headers=albumheaders, data=data)  # creates the album on cyberdrop/bunkr etc.
    data = r.json()

    #was it a success?
    success = data['success']
    if success == False:
        print(Fore.RED + 'Album \'',album_name,'\' already exists')
        Albumalreadyuplist.append(album_name)
        #Need to work out how to skip to next item
    elif success == True:
        album_id = data['id']
        print(Fore.GREEN + 'Album \'',album_name,'\' created successfully with ID:', album_id)
        print()

        #Now we start on the files by creating a list of them
        Filelist = list()
        for root, subdirectories, files in os.walk(dir):
            for file in files:
                Filelist.append(file)
        album_file_number = len(Filelist)
        print(Fore.YELLOW + 'Uploading ', album_file_number, ' files')

        #the generic api upload url
        upload_file_url = base_url+"/api/upload"

        #give it some headers
        fileheaders = {'token': f"{token}", 'albumid': f"{album_id}"}

        #lets do this - uploading files
        file_number = 1
        Faillist = list()
        for file in Filelist:
            print()
            print(Fore.YELLOW + "uploading file",file_number, 'of', album_file_number,':', file, 'to:', album_name)
            file_number = file_number + 1
            success_count = 0
            response = requests.Session()

            attempts = 0
            while attempts <10:
                try:
                    files = {'files[]': open(file, 'rb')}
                    response = requests.post(upload_file_url, headers=fileheaders, files=files)
                    attempts = 11
                except:
                    attempts += 1
                    print("upload failed, trying again in 3 seconds")
                    time.sleep(3)
            data2 = response.json()
            success = data2['success']
            if success == True:
                print(Fore.GREEN + file, "uploaded succesfully")
                success_count = success_count + 1
            elif success == False:
                print(Fore.RED + file, "upload failed")
                Faillist.append(file)
        print()


        #Get the album url and add to list
        albumurlheaders = {'token': f"{token}", }
        albumr = requests.get(albums_url, headers=albumurlheaders)  # gets list of albums
        albumdata = albumr.json()

        #shitty bunkr album URL fix by calculating page of uploads list the album is on, I hate this
        if base_url == "https://bunkr.is":
            pagecount = str(math.floor(albumdata['count'] / 25))
            albums_url = "https://bunkr.is/api/albums/" + pagecount
            albumurlheaders = {'token': f"{token}", }
            r = requests.get(albums_url, headers=albumurlheaders)  # gets list of albums
            albumdata = r.json()
            for attrs in albumdata['albums']:
                if attrs['id'] == album_id:
                    albumurl = base_url + '/a/' + attrs['identifier']
                    break
            else:
                print(Fore.RED + 'Nothing found!')
                albumurl = ""
            Albumurllist.append(albumurl)

        #The normal cyberdrop approach (much better)
        else:
            for attrs in albumdata['albums']:
                if attrs['id'] == album_id:
                    albumurl = base_url + '/a/' + attrs['identifier']
                    break
            else:
                print(Fore.RED + 'Nothing found!')
                albumurl = ""
            Albumurllist.append(albumurl)

        #Did album upload every file successfully or not?
        if (file_number - 1) == album_file_number:
            print(Fore.GREEN + 'Album \'',album_name,'\' uploaded successfully:', albumurl)
            Albumsuccesslist.append(album_name) #remove later or change to success list
            Albumsuccesscount = Albumsuccesscount + 1
        else:
            print(Fore.YELLOW + 'Album not fully uploaded.', success_count, 'files uploaded successfully. The following files failed to upload:', Faillist)
            Albumfaillist.append(album_name)
        print()
        print()

#Success/Fail Stats
if Albumsuccesscount == album_count:
    print(Fore.GREEN + 'All albums uploaded successfully: ', Fore.CYAN, Albumsuccesslist)
    print(Fore.CYAN, Albumurllist)
elif Albumsuccesscount == 0:
    print()
    print(Fore.RED + 'No albums uploaded, they already existed')
else:
    print(Fore.GREEN + 'The following albums uploaded successfully:', Albumsuccesslist)
    print(Fore.CYAN, Albumurllist)
    print(Fore.YELLOW + 'The following albums already existed:', Albumalreadyuplist)
    print(Fore.RED + 'The following albums failed to upload successfully:', Albumfaillist)


#write uploaded album urls to a txt file
os.chdir(base_dir) #Move back to base directory
filename = datetime.datetime.now()
output = open(filename.strftime("%Y-%m-%d_%H-%M")+"_uploaded_album_urls.txt", "w") #Open file, creates if doesn't already exist

#write a combined list of album names and URLs
output.write('Combined album name + URL list:' + '\n')
for i in range(len(Albumurllist)):
    output.write(Albumsuccesslist[i] + '\n' + Albumurllist[i] +'\n')
output.write('\n')

#write a list of just URLs
output.write('Bare URL list:' + '\n')
for url in Albumurllist:
    output.write(url + '\n')
output.close()

exitText = input("\nPress enter to quit.")