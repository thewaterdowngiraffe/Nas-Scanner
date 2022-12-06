
import time
import os
import requests
import os.path
import time
from timeit import default_timer as timer   
import multiprocessing
import time
from driver_functions import *



def dirGet(rootdir,file_count,finished,file_extensions,timeStart,html_file_dir,scanType,output=1):

    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            finished = dirGet(d,file_count,finished,file_extensions,timeStart,html_file_dir,scanType,output)
            finished += files(d,file_extensions,scanType,output)
            
            if output == 1:
                os.system('cls')
                print(loading(finished,file_count,"getting Files\t"),end="\n\t")
            if output >= 2:
                os.system('cls')
                print("current scan directory: {}\nScanning {} files. scan completed on {} files.\nPersentage finished: {}%".format( d, file_count, finished, round((finished/file_count)*100,2)))

            if (finished != 0):
                if output >= 2:
                    print("time remaining {} min".format(  round((((time.perf_counter() - timeStart)*(file_count-finished)/finished))/60 ,2)))
                with open("files\\status.run","w") as status:
                    status.write(str(round(((finished/file_count)*100),2)))
                if scanType == '0':
                    if output >= 2:
                        print("generating the html file")
                    make_HTML(scan_other(output),html_file_dir,output)
                    if output >= 2:
                        print("gen finished")
    return(finished)




def files(rootdir,file_extensions,scanType,output=1):
    if output == 1: 
        print("")
    count = 0 
    dir_count = len(os.listdir(rootdir))
    files_hash = []
    files_hash_dir = []
    files_hash_hash = []
    pool = multiprocessing.Pool()
    if output >= 3:
        print(pool._processes)
    for x in os.listdir(rootdir):
        if output >= 4:
            print(os.path.isdir(rootdir+"\\"+x),end="")
            print("\t"+x)
        if os.path.isdir(rootdir+"\\"+x) == False:
                count+=1
                status = "scantype: "+str(scanType)+"\t"
                if output == 1:
                    print(loading(count,dir_count,status),end="")
                d = open("files\\Files dir.txt", "a")
                h = open("files\\Files hash.txt", "a")
                if scanType == '0':
                    files_hash.append(rootdir+"\\"+x)
                    files_hash_dir.append(rootdir+"\\"+x)
                    if len(files_hash) >= pool._processes or count+1 >= dir_count:
                        files_hash_hash = pool.map(hash_file, files_hash)
                        for o in range(len(files_hash_hash)):
                            if files_hash_hash[0] == "error_":
                                print("error please check log file")
                            else:
                                d.write(files_hash[o]+"\n")
                                h.write(files_hash_hash[o]+"\n")
                        files_hash = []
                        files_hash_dir = []
                        files_hash_hash = []
                if scanType == '1':
                    filehash = hash_file(rootdir+"\\"+x)
                    d.write(rootdir+"\\"+x+"\n")
                    h.write(filehash+"\n")
                    if output >= 3:
                        print("\t\t"+filehash)
                if scanType == '2':
                    d.write(rootdir+"\\"+x+"\n")
                    h.write(x+"\n")
                    if output >= 3:
                        print("\t\t"+x)
                d.close
                h.close


    return(count)


#   dirgetfiles and filesextentions functions have 2 functions
#   first function is obtain total count of files for scanning
#   second is determin the file types that follow the file 
#   extiontion format that i am enforcing, the file types
#   must be "human format" meaning the file extention can not 
#   contain either underscores nor blank spaces. file format 
#   must be .type 


def dirGetfiles(rootdir,file_extensions,file_count,output=1): 
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            file_count = dirGetfiles(d,file_extensions,file_count,output)
            file_extensions, file_count = filesextentions(d,file_extensions,file_count,output)
    return(file_count) #walks through dir
def filesextentions(rootdir,file_extensions,file_count,output=1): 
    if output >= 2:
        print(file_count)
    for x in os.listdir(rootdir):
        if os.path.isdir(x) == False:
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




def scan_other(output=1): # this is what makes the dupes.csv file, the html file requires this
    if output >= 2:
        print("scanning for duplicates")
    f = open("files\\dupes.csv", "w")
    f.close
    d = open("files\\Files dir.txt", "r")
    h = open("files\\Files hash.txt", "r")
    Lines = h.readlines()
    Lines_dir = d.readlines()
    flaged = 0
    dupe = 0
    for x in range(len(Lines)):
        if output >= 1:
            print(loading(x+1,len(Lines),"Dupe-Scan:\t"),end = "")
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
    f = open("files\\dupes.csv", "a")
    f.write("\n")
    f.close
    h.close
    d.close
    if output >= 2:
        print("scan finished")
    if output >= 3:
        print(flaged)
        print(dupe)

    return(flaged)# this is what makes the dupes.csv file, the html file requires this




def Run(rootdir,html_file_dir,scanType,output=1): # full hash 
    file_prep()
    file_extensions = []
    file_count = 0
    file_count = dirGetfiles(rootdir,file_extensions,file_count,output)
    if output >= 4:
        print(file_extensions)
    if output >= 2:
        print(file_count)
    dirGet(rootdir,file_count,0,file_extensions,time.perf_counter(),html_file_dir,scanType,output)
    make_HTML(scan_other(output),html_file_dir,output)
    return(file_count)
     # this is what makes the dupes.csv file, the html file requires this




def make_HTML(num,html_file_dir,output=1): # make html pages from csv content 
    html_file_dir = html_file_dir +"\\"
    status = open("files\\status.run","r")
    csv_file = open("files\\dupes.csv", "r")
    Lines = status.readlines() #reads the CSV file
    csv = csv_file.readlines()
    dir_cap = 35
    pagenum = 0 #current page
    divs = 0
    filename =html_file_dir + "page{}.html".format(pagenum+1)
    html = open(filename, "w+")
    html_writer_top(html,pagenum,(num//dir_cap)+1,num,Lines[0])
    ##scans through CSV file looking for a new line, when finding a new line a div will be created and all images in that section will be placed in that div.
    e = 0
    runs = 0
    for imgs in csv:
        runs+=1
        if output >= 4:
            print(e,end = "\t")
            print(divs,end = "\t")
            print(imgs)
        if imgs == "\n":
            if divs == dir_cap:
                divs= 1
                html_writer_bottom(html)
                pagenum+=1
                filename =html_file_dir + "page{}.html".format(pagenum+1)
                html = open(filename, "w+")
                html_writer_top(html,pagenum,(num//dir_cap)+1,num,Lines[0])
                if output >= 2:
                    print("generating html page{}".format(pagenum+1))
                html_writer_div(html,divs)
            else:
                divs+=1
                e+=1
                if runs != len(csv):
                    html_writer_div(html,divs)
                else:
                    html_writer_bottom(html)
        else:
            html.write(html_writer_img(imgs[:len(imgs)-2]))
    return #this is the html file(s) generator



def download_updates(files,output=1): #using list provided download the file and name it/place  in correct directory
    if output >= 2:
        print("starting update\ndownloading {} files".format(len(files)))
    count = 0
    for file_download in files:
        if not "conf" in file_download[2]:
            print(file_download[2])
            if output >= 3:
                print(file_download[2])
            count +=1
            if output >= 2:
                print("files downloaded {}/{}".format(count,len(files)))
            if output == 1:
                print(loading(count,len(files),"downloading"),end = "")
            if not file_download[1] == '':
                MYDIR = (file_download[1])
                CHECK_FOLDER = os.path.isdir(MYDIR)
                if not CHECK_FOLDER:
                    os.makedirs(MYDIR)
            r = requests.get(file_download[0], allow_redirects=True)    
            open(file_download[2], 'wb').write(r.content)
        elif os.path.isfile(file_download[2]) == False:
            if output >= 3:
                print(file_download[2])
            count +=1
            if output >= 2:
                print("files downloaded {}/{}".format(count,len(files)))
            if output == 1:
                print(loading(count,len(files),"downloading"),end = "")
            if not file_download[1] == '':
                MYDIR = (file_download[1])
                CHECK_FOLDER = os.path.isdir(MYDIR)
                if not CHECK_FOLDER:
                    os.makedirs(MYDIR)
            r = requests.get(file_download[0], allow_redirects=True)    
            open(file_download[2], 'wb').write(r.content)
        else:
            if output >= 2:
                print("skipping {}".format(file_download[2]))
            count +=1
            if output >= 2:
                print("files downloaded {}/{}".format(count,len(files)))
            if output == 1:
                print(loading(count,len(files),"downloading"),end = "")
    if output >= 1:
        print("\n\tupdate finished")






        

if __name__ == '__main__':

    # The program will exit if there are only daemonic threads left.

    ## things to add
    # light weight scan looks for duplicate names -
    # mid looks at metadata
    # heavy looks at hash 
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
    # andrew wants movie codec shit keep good one? more questions must be asked to answer that
    # make C/c++ program to do the hashing and logging

    #error handeling for non english file names will thow errors need fix


    #   file STATS amount of each file type (catagory)
    #   file counts
    #   folder counts

    #   things done:
    #       added light scan
    #       reduced ram usage when looking at html site
    #       config changes
    #       download updates/changes#

    #   file metadata will be a pain in the side 


    try:
        rootdir, html_file_dir, scanType, update, output = read_config()
    except :
        files_too_download = [['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/config.conf','files','files\\config.conf'],]
        download_updates(files_too_download)

        osCommandString = "notepad.exe files\\config.conf"  #open file that was just downloaded and present to user
        os.system("files\\config.conf")

        updates = 1







    ## update/download update function 
    # dir to make must not be left blank please leave it as '' if there is no directory to make
    # [link, dir to make, filename/location]

    if update == '1':
    
        files_too_download = [
            ['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/dupes.css',html_file_dir,html_file_dir + '\\dupes.css'],             
            ['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/config.conf','files','files\\config.conf'],
            ['https://github.com/thewaterdowngiraffe/Nas-Scanner/raw/master/required/backup.png',html_file_dir + "\\images",html_file_dir + "\\images" + '\\backup.png'],
            ['https://raw.githubusercontent.com/thewaterdowngiraffe/Nas-Scanner/master/required/HTML.conf','files',"files\\HTML.conf"]
            ]

        download_updates(files_too_download)
    




    #   scan type is a number that will represent the type of scan
    #   0 is full scan multithreaded hashing
    #   1 is full scan single threaded hashing
    #   2 is light (looks at file names nothing else)
    #   #
    

    file_count = Run(rootdir,html_file_dir,scanType,output) #  uncomment to run 

    start = timer()
    

    run_logs(start, file_count,scanType,output,rootdir,html_file_dir,scan_other(0))



   






    #  uncomment to run 
    #clean_up() ## removes bulky and unreadable files


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




















    '''
    # taken from https://realpython.com/pysimplegui-python/
    '''
