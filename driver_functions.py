from datetime import datetime
import platform
import hashlib
import requests
import sys
import os
from timeit import default_timer as timer 

def run_logs(start=0, file_count="unknown",scantype="unknown",output_lvl="unknown",target="Unknown",html_target="Unknown",dupes=0,Livepage=0):
    finish = timer()
    time =  finish - start
    if os.path.isfile("scan_logs.csv")== False:
        with open("scan_logs.csv", "a+") as log_file:
            log_file.write("Start_time,Finish_time,Run_time,File_count,Scan_type,Output_lvl,Live_Page,Scan_dir,Number_of_dupes,HTML_page_location,OS,OS_Version\n")
    with open("scan_logs.csv", "a+") as log_file:
        log_file.write(str(start)+","+str(finish)+","+str(time)+","+str(file_count)+","+str(scantype)+","+str(output_lvl)+","+str(Livepage)+","+str(target)+","+str(dupes)+","+str(html_target)+","+str(platform.system())+","+str(platform.release())+"\n")


def error_log(error):
    with open("Error.log.csv", "a+") as log_file:
        time = datetime.utcnow()
        log_file.write(str(error) + ","+ str(time)+","+str(platform.system())+","+str(platform.release())+","+str(platform.version())+","+str(platform.processor())+"\n")
    return()

def hash_file(filename):
    try:
        h = hashlib.sha1()
        with open(filename,'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)
        return h.hexdigest()
    except:
        error_log(sys.exc_info()[0])
        return("error_")

def read_config(): # reads the config file and returns setting and directorys to be used
    scan_dir =""
    html_file_dir = ""
    with open("files\\config.conf","r+") as conf:
        settings = conf.readlines()
        for line in settings:
            if not "#" in line:
                if "scan=" in line:
                    scan_dir = line[len("scan="):len(line)-1]              
                if "site=" in line:
                    html_file_dir = line[len("site="):len(line)-1]               
                if "scantype=" in line:
                    scantype = line[len("scantype="):len(line)-1]
                if "update=" in line:
                    update = line[len("update="):len(line)-1]

                if "outputlevel=" in line:
                    try:
                        outputlevel = int(line[len("outputlevel="):len(line)-1])
                    except :
                        outputlevel = 1
                if "Livepage=" in line:
                    try:
                        Livepage = int(line[len("Livepage="):len(line)-1])
                    except :
                        Livepage = 0



    return(scan_dir,html_file_dir,scantype,update,outputlevel,Livepage)

def file_prep():
    d = open("files\\Files dir.txt", "w+")
    h = open("files\\Files hash.txt", "w+")
    f = open("files\\dupes.csv", "w+")
    # wipes files and resets
    f.close()
    d.close()
    h.close()
    return # wipes files that are hard coded

def loading(current,max_val,status):
    fin_bar = ""
    fin = int(round(current/max_val*100,0))
    for x in range(fin):
        fin_bar += "\u25A0"
    for x in range(100 - fin):
        fin_bar +="*"
    retunr_str = "\r{}[{}]: {}%".format(status, fin_bar,fin) 
    return(retunr_str)

def html_conf_scan(): # reads the config file and returns setting and directorys to be used
    with open("files\\HTML.conf","r+") as conf:
        settings = conf.readlines()
        for line in settings:
            if not "#" in line:
                if "StartTag=" in line:
                    StartTag = line[len("StartTag="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "EndTag=" in line:
                    EndTag = line[len("EndTag="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "nav0=" in line:
                    nav0 = line[len("nav0="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "nav1=" in line:
                    nav1 = line[len("nav1="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "nav2=" in line:
                    nav2 = line[len("nav2="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "navclose=" in line:
                    navclose = line[len("navclose="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "IMG_open=" in line:
                    IMG_open = line[len("IMG_open="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "IMG_close=" in line:
                    IMG_close = line[len("IMG_close="):len(line)-1].replace("\\n","\n").replace("\\t","\t")
                if "div=" in line:
                    div = line[len("div="):len(line)-1].replace("\\n","\n").replace("\\t","\t")

    return(StartTag,EndTag,nav0,nav1,nav2,navclose,IMG_open,IMG_close,div)

def html_writer_top(file_html,pagenum,pages,num,Line):
    StartTag,EndTag,nav0,nav1,nav2,navclose,IMG_open,IMG_close,div = html_conf_scan()
    file_html.write(StartTag)
    if pagenum == 0:
        file_html.write(nav0.replace("{}",str(pagenum+2)))
    elif pagenum+1 == pages:
        file_html.write(nav1.replace("{}",str(pagenum)))
    else:
        file_html.write(nav2.replace("{1}",str(pagenum)).replace("{2}",str(pagenum+2)))
    file_html.write(navclose.replace("{1}",str(num)).replace("{2}",str(Line)))
    return

def html_writer_img(content):
    StartTag,EndTag,nav0,nav1,nav2,navclose,IMG_open,IMG_close,div = html_conf_scan()
    string = IMG_open.replace("{}",content) +content+IMG_close
    return(string)

def html_writer_div(file_html,content):
    StartTag,EndTag,nav0,nav1,nav2,navclose,IMG_open,IMG_close,div = html_conf_scan()
    file_html.write(div.replace("{}",str(content)))
    return()

def html_writer_bottom(file_html):
        StartTag,EndTag,nav0,nav1,nav2,navclose,IMG_open,IMG_close,div = html_conf_scan()
        file_html.write(EndTag)

def clean_up():
    os.remove("files\\Files dir.txt")
    os.remove("files\\Files hash.txt")
    os.remove("files\\status.run")



def download_updates(files,output=1): #using list provided download the file and name it/place  in correct directory
    if output >= 2:
        print("starting update\ndownloading {} files".format(len(files)))
    count = 0
    for file_download in files:
        if not "conf" in file_download[2]:
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
