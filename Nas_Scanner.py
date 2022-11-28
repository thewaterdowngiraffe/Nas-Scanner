import hashlib
import time
import os
import requests

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest() #hashfile, just works


def dirGet(rootdir,file_count,finished,file_extensions,timeStart,html_file_dir,scanType):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            finished = dirGet(d,file_count,finished,file_extensions,timeStart,html_file_dir,scanType)
            finished += files(d,file_extensions,scanType)
            os.system('cls')
            print("current scan directory: {}\nScanning {} files. scan completed on {} files.\nPersentage finished: {}%".format( d, file_count, finished, round((finished/file_count)*100,2)))
            if (finished != 0):
                print("time remaining {} min".format(  round((((time.perf_counter() - timeStart)*(file_count-finished)/finished))/60 ,2)     ))
                with open("files\\status.run","w") as status:
                    status.write(str(round(((finished/file_count)*100),2)))
                if scanType == 0:
                    print("generating the html file")
                    make_HTML(scan_other(),html_file_dir)
                    print("gen finished")
    return(finished)



def files(rootdir,file_extensions,scanType):
    count = 0 
    for x in os.listdir(rootdir):
        for i in file_extensions:
            if x.endswith(i):
                count+=1
                d = open("files\\Files dir.txt", "a")
                h = open("files\\Files hash.txt", "a")
                if scanType == 0:
                    filehash = hash_file(rootdir+"\\"+x)
                    d.write(rootdir+"\\"+x+"\n")
                    h.write(filehash+"\n")
                    print("\t\t"+filehash)
                if scanType == 1:
                    d.write(rootdir+"\\"+x+"\n")
                    h.write(x+"\n")
                    print("\t\t"+x)

    return(count)


#   dirgetfiles and filesextentions functions have 2 functions
#   first function is obtain total count of files for scanning
#   second is determin the file types that follow the file 
#   extiontion format that i am enforcing, the file types
#   must be "human format" meaning the file extention can not 
#   contain either underscores nor blank spaces. file format 
#   must be .type 


def dirGetfiles(rootdir,file_extensions,file_count): 
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            file_count = dirGetfiles(d,file_extensions,file_count)
            file_extensions, file_count = filesextentions(d,file_extensions,file_count)
    return(file_count) #walks through dir
def filesextentions(rootdir,file_extensions,file_count):  
    print(file_count)
    for x in os.listdir(rootdir):
        o = 0
        count = 0
        k = 0
        for i in x: # gets the number of periods in a extension
            if i == ".": 
                count += 1  
        for i in x: 
            if i == "." :
                k+=1
            if i == "." and k == count and x[o+1] != "_" and not " " in x[o:] and ".DS_Store" not in x:
                ext = x[o:]
                file_count+=1
                skip = 0
                for y in file_extensions:
                    if y == ext:
                        skip = 1
                if skip ==0:
                    #print(file_extensions)
                    file_extensions.append(ext)
            o+=1
    return(file_extensions,file_count) ##locates and returns all file extentions within a rule set and total files



def file_prep():
    d = open("files\\Files dir.txt", "w+")
    h = open("files\\Files hash.txt", "w+")
    f = open("files\\dupes.csv", "w+")
    # wipes files and resets
    f.close()
    d.close()
    h.close()
    return # wipes files that are hard coded

def Run(rootdir,html_file_dir,scanType): # full hash 
    file_prep()
    file_extensions = []
    file_count = 0
    file_count = dirGetfiles(rootdir,file_extensions,file_count)
    print(file_extensions)
    print(file_count)
    dirGet(rootdir,file_count,0,file_extensions,time.perf_counter(),html_file_dir,scanType)
    make_HTML(scan_other(),html_file_dir)
    return # this is what makes the dupes.csv file, the html file requires this



def scan_other(): # this is what makes the dupes.csv file, the html file requires this
    f = open("files\\dupes.csv", "w")
    f.close
    d = open("files\\Files dir.txt", "r")
    h = open("files\\Files hash.txt", "r")
    Lines = h.readlines()
    Lines_dir = d.readlines()
    flaged = 0
    dupe = 0
    for x in range(len(Lines)):
        skip = 0
        for y in range(x):
            if Lines[x] == Lines[y]:
                skip +=1
                #print(str(x) + "\t"+ str(y))
        if skip == 0:
            count = 0
            for y in range(len(Lines)):
                if y >x:
                    if Lines[x] == Lines[y]:
                        count+=1

                        f = open("files\\dupes.csv", "a")

                        if count == 1:
                            flaged+=1
                            f.write("\n"+Lines_dir[x][:len(Lines_dir[x])-1] + ",\n")
                        f.write(Lines_dir[y][:len(Lines_dir[y])-1]+",\n")
                        if count != 1:
                            dupe+=1
                        f.close
    h.close
    d.close
    print(flaged)
    print(dupe)
    return(flaged)# this is what makes the dupes.csv file, the html file requires this



def make_HTML(num,html_file_dir): # make html pages from csv content 
    html_file_dir = html_file_dir +"\\"
    status = open("files\\status.run","r")
    csv = open("files\\dupes.csv", "r")
    Lines = status.readlines() #reads the CSV file
    
    dir_cap = 35
    pages = (num//dir_cap) +1 # max numebr of pages
    pagenum = 0 #current page

    ##html stuff, need to clean up this section 
    string = '"  onerror=' +"'this.src = " +'"./images/backup.png"' + "' loading='lazy' alt = 'image can not be displayed' >"
    img_tag = ['<img src="',string  ]
    body_tag_start = '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta charset="UTF-8">\n\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n\t\t<!--  Author: Keegan Andrus https://github.com/thewaterdowngiraffe/Nas-Scanner -->\n\t\t<title>Duplicated images</title>\n\t\t<link rel="stylesheet" href="dupes.css">\n\t\t<style type="text/css">\n\t\t\t* {\n\t\t\t\tmargin: 0;\n\t\t\t\tpadding: 0;\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n'
    body_tag_end = '\n\t\t</div>\n\t</body>\n</html>'

    count = 0
    divs = 0
    html = open(html_file_dir + "page0.html", "w+")

    write_string = ""

    ##scans through CSV file looking for a new line, when finding a new line a div will be created and all images in that section will be placed in that div.
    for imgs in csv:


        if divs%dir_cap == 0: #make new file
            filename =html_file_dir + "page{}.html".format(pagenum+1)
            html = open(filename, "w+")
            html.write(body_tag_start) 
        

            ### makes nav bar
            if pagenum == 0:
                html.write('\t<div id="navsection">\n\t\t<header>\n\t\t\t<nav>\n\t\t\t\t<ul>\n\t\t\t\t\t<li><a href="./page{}.html">next</a></li>\n\t\t\t\t</ul>\n\t\t\t</nav>\n\t\t</header>\n\t</div>\n'.format(pagenum+2))
            elif pagenum+1 == pages:
                html.write('\t<div id="navsection">\n\t\t<header>\n\t\t\t<nav>\n\t\t\t\t<ul>\n\t\t\t\t\t<li><a href="./page{}.html">back</a></li>\n\t\t\t\t\t<li><a href="./page0.html">back to start</a></li>\n\t\t\t\t</ul>\n\t\t\t</nav>\n\t\t</header>\n\t</div>\n'.format(pagenum))
            else:
                html.write('\t<div id="navsection">\n\t\t<header>\n\t\t\t<nav>\n\t\t\t\t<ul>\n\t\t\t\t\t<li><a href="./page{}.html">back</a></li>\n\t\t\t\t\t<li><a href="./page{}.html">next</a></li>\n\t\t\t\t</ul>\n\t\t\t</nav>\n\t\t</header>\n\t</div>\n'.format(pagenum,pagenum+2))
            ### start of page
            html.write('\t\t<div class = "title">\n\t\t\t<h1>{} duplicates flagged for viewing</h1>\n\t\t\t<p>scan is at {}%</p>\n\n\t\t</div>\n'.format(num,Lines[0]))



        if imgs == "\n" or divs%35 == 0:
            if divs == 0:
                print("generating html page{}".format(pagenum+1))
            else:
                if divs <= dir_cap:
                    html.write('\n\t\t</div>\n\n\t\t<div class="group">\n\t\t\t<h2>group contains {} duplicates</h2>\n'.format(count))
                if divs == dir_cap+1:
                    html.write('\n\t\t</div>\n\n\t\t<div class="group">\n\t\t\t<h2> to many Duplicates, to prevent website crashes, no further images will be loaded.<br> to load more images please resolve images located above<br>maximum of {} can be displayed at a time</h2>\n'.format(dir_cap))
            html.write(write_string) 
            write_string = ""
            #write and reset the html string that goes to the file
            divs+=1
            count = 0

        if not imgs == "\n":
            count+=1
            if divs <= dir_cap:
                write_string += '\n\t\t\t<a href="{}"  target="_blank" >{}{}{}</a>'.format(imgs[:len(imgs)-2],img_tag[0],imgs[:len(imgs)-2],img_tag[1])
    
        if divs%35 == 0 and imgs == "\n": #finish file ready for next one
            pagenum +=1
            divs =0
            html.write(write_string)
            html.write(body_tag_end)
    return #this is the html file(s) generator










def read_config(): # reads the config file and returns setting and directorys to be used
    scan_dir =""
    html_file_dir = ""
    with open("files\\config.conf","r+") as conf:
        settings = conf.readlines()
        for line in settings:
            if not "#" in line:
                if "scan=" in line:
                    #print(line[5:len(line)-1])
                    scan_dir = line[len("scan="):len(line)-1]
                if "site=" in line:
                    #print(line[5:len(line)-1])
                    html_file_dir = line[len("site="):len(line)-1]
                if "scantype=" in line:
                    scantype = line[len("scantype="):len(line)-1]
                if "update=" in line:
                    update = line[len("update="):len(line)-1]




    return(scan_dir,html_file_dir,scantype,update)









def download_updates(files): #using list provided download the file and name it/place  in correct directory
    print("starting update")
    print (len(files))
    for file_download in files:
        if not file_download[1] == '':
            MYDIR = (file_download[1])
            CHECK_FOLDER = os.path.isdir(MYDIR)
            if not CHECK_FOLDER:
                os.makedirs(MYDIR)
        r = requests.get(file_download[0], allow_redirects=True)
        open(file_download[2], 'wb').write(r.content)
    print("update finished")



## things to add
# light weight scan looks for duplicate names
# mid looks at metadata
# heavy looks at hash 
# display time to finish
# open file for viewing at start of run 
# reduce ram used when loading page
# display file type bellow image
# display directory 
# scan spesific file type
# directory scanning (directory tree)
# check for matching folder content (all files match in directory)
# read speed
# logging file for data 
# minimize button
# site filter for files and others
# delete files from web (make a file that will contain all files to be deleted, move those files to a dir where after 30 days they can be removed)
# file size
#andre wants movie codec shit keep good one? more questions must be asked to answer that



#   things done:
#       added light scan
#       reduced ram usage when looking at html site
#       config changes
#       download updates/changes#







rootdir, html_file_dir, scanType, update = read_config()
print(update)



## update/download update function 
# dir to make must not be left blank please leave it as '' if there is no directory to make
# [link, dir to make, filename/location]

if update == '1':
    
    files_too_download = [
        ['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/dupes.css','',html_file_dir + '\\dupes.css'],             
        ['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/config.conf','files','files\\config.conf'],
        ['https://github.com/thewaterdowngiraffe/Nas-Scanner/raw/master/required/backup.png',html_file_dir + "\\images",html_file_dir + "\\images" + '\\backup.png']
             ]

    download_updates(files_too_download)
    


#   scan type is a number that will represent the type of scan
#   0 is full has
#   1 is light (looks at file names nothing else)
#   #


#Run(rootdir,html_file_dir,scanType) #  uncomment to run 

# --light hash--
# get directory of all files  -- log to file dir.txt
# scan list of files and extract names -- store file names in the hash file
# look for exact matches  scan_other() function will work 
# send list of matches to CSV
# make html  

#   --function list--
#   make_HTML(scan_other(),html_file_dir)
#   rootdir,html_file_dir = read_config()
#   Run(rootdir,html_file_dir,scanType) #hard hash
#   



#make_HTML(scan_other(),html_file_dir) # uncomment to make html site no scan

# changes made to the master files located in the required folder are synced accross all versions when they run 

