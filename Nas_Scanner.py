# Python program to find the SHA-1 message digest of a file

# importing the hashlib module
from ctypes import Array
import numpy as np
import hashlib
import glob
import time
from operator import countOf
import os
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
   return h.hexdigest()


def dirGet(rootdir,file_count,finished,file_extensions,timeStart):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            #print(d)

            finished = dirGet(d,file_count,finished,file_extensions,timeStart)

            finished += files(d,file_extensions)
            os.system('cls')
            #print("current directory: "+d)
            print("current scan directory: {}\nScanning {} files. scan completed on {} files.\nPersentage finished: {}%".format( d, file_count, finished, round((finished/file_count)*100,2)))
            if (finished != 0):
                print("time remaining {} min".format(  round((((time.perf_counter() - timeStart)*(file_count-finished)/finished))/60 ,2)     ))

                with open("status.run","w") as status:
                    status.write(str(round(((finished/file_count)*100),2)))

                make_HTML(scan_other())


            #print(finished)
            #print(str(round((finished/file_count)*100,2)) +"%")
    return(finished)
           
def files(rootdir,file_extensions):
    #print(rootdir)
    count = 0 
    for x in os.listdir(rootdir):
        #print(x)
        for i in file_extensions:
            if x.endswith(i):
                count+=1
                d = open("Files dir.txt", "a")
                h = open("Files hash.txt", "a")
                filehash = hash_file(rootdir+"\\"+x)
                d.write(rootdir+"\\"+x+"\n")
                h.write(filehash+"\n")
                #print(i)
                #print("\t\t"+filehash)
    return(count)

def dirGetfiles(rootdir,file_extensions,file_count):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            #print(d)
            file_count = dirGetfiles(d,file_extensions,file_count)
            file_extensions, file_count = filesextentions(d,file_extensions,file_count)
    return(file_count)


def filesextentions(rootdir,file_extensions,file_count):
    print(file_count)
    for x in os.listdir(rootdir):
        o = 0
        count = 0
        k = 0
        for i in x:
            if i == ".":
                count += 1
        for i in x:
            if i == "." :
                k+=1
            if i == "." and k == count and x[o+1] != "_" and not " " in x[o:]:
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

    return(file_extensions,file_count)

def file_prep():
    d = open("Files dir.txt", "w+")
    h = open("Files hash.txt", "w+")
    f = open("dupes.csv", "w+")
    f.close()
    d.close()
    h.close()

def Run():
    file_prep()
    file_extensions = []
    file_count = 0
    file_count = dirGetfiles(rootdir,file_extensions,file_count)
    print(file_extensions)
    print(file_count)
    dirGet(rootdir,file_count,0,file_extensions,time.perf_counter())




def scan_other():
    f = open("dupes.csv", "w")
    f.close
    d = open("Files dir.txt", "r")
    h = open("Files hash.txt", "r")
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
                        f = open("dupes.csv", "a")
                        if count == 1:
                            flaged+=1
                            f.write("\n"+Lines_dir[x][:len(Lines_dir[x])-1] + ",\n")
                        f.write(Lines_dir[y][:len(Lines_dir[y])-1]+",\n")
                        if count != 1:
                            dupe+=1
                        



                        print(Lines[x])
                        print(Lines[y])
                        print("\n")
    print(flaged)
    print(dupe)
    return(flaged)





def make_HTML(num):
    status = open("status.run","r")
    html = open("dupes.html", "w+")
    csv = open("dupes.csv", "r")

  
    Lines = status.readlines()

    string = '"  onerror=' +"'this.src = " +'"./images/backup.png"' + "'>"
    print(string)
    img_tag = ['\n\t\t\t<img src="',string  ]
    body_tag_start = '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta charset="UTF-8">\n\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n\t\t<!--  Author: Keegan Andrus,000880159 -->\n\t\t<title>Duplicated images</title>\n\t\t<link rel="stylesheet" href="dupes.css">\n\t\t<style type="text/css">\n\t\t\t* {\n\t\t\t\tmargin: 0;\n\t\t\t\tpadding: 0;\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n'
    body_tag_end = '\n\t\t</div>\n\t</body>\n</html>'


    html.write(body_tag_start)

    divs = 0
    html.write('\t\t<div class = "title">\n\t\t\t<h1>{} duplicates flagged for viewing</h1>\n\t\t\t<p>scan is at {}%</p>\n'.format(num,Lines[0]))
    write_string = ""
    count = 0

    for imgs in csv:
        if imgs == "\n":
            if divs == 0:
                print("generating html page")
            else:

                html.write('\n\t\t</div>\n\n\t\t<div class="group">\n\t\t\t<h2>group contains {} duplicates</h2>'.format(count))


            html.write(write_string)
            write_string = ""
            divs+=1
            count = 0
        else:
            count+=1
            write_string += '<a href="{}"  target="_blank" >{}{}{}</a>'.format(imgs[:len(imgs)-2],img_tag[0],imgs[:len(imgs)-2],img_tag[1])

    html.write(write_string)


    html.write(body_tag_end)


    





rootdir = '//192.168.2.194/nasdrive/parents'
rootdir = '\\\\192.168.2.194\\nasdrive'
rootdir = '\\\\192.168.2.194\\nasdrive\\parents\\images\\all pictures\\sean\\2020'

rootdir = '\\\\192.168.2.194\\nasdrive\\tmp'


#
#exit()

t =  time.perf_counter()
Run()
print(time.perf_counter() - t)
#
#scan()
make_HTML(scan_other())
## GET ALL file types 

