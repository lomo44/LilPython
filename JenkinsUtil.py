# Utility Functions regarding Jenkins
import re
import subprocess
from FileUtility import *

JENKINS_CLI_CALLER = 'java -jar jenkins-cli.jar'
JENKINS_OPTION_SERVER_URL = '-s'
JENKINS_CLI_FUNCTION_SETBUILD_DISPLAY_NAME = "set-build-display-name"

def get_jenkins_server_url(server_name):
    return 'http://' + server_name + "/"
def combine_build_parameters(_list):
    final = ''
    for item in _list:
        final += item + ' '
    return final[0:len(final)-1]

def fetch_artifact_from_jenkins_to_directory(Servername, Jobname, des, includelist):
    print("Getting Build Artifacts From Jenkins...")
    includelistcpy = includelist.copy()
    jenkinsurl = "http://"+Servername + "/job/" + Jobname + "/lastSuccessfulBuild/artifact/*zip*/archive.zip"
    zipfilename = 'archive.zip'
    zipfilepath = os.path.join(des,zipfilename)
    archivepath = os.path.join(des,'archive')
    if check_file_exist_in_directory(zipfilename, des):
        removefile(zipfilepath)
    if check_dir_exist_in_directory("archive", des):
        delete_directory_and_content(archivepath)
    for dir in includelistcpy:
        if check_dir_exist_in_directory(dir, des):
            delete_directory_and_content(os.path.join(des,dir))
    zipfilename = download_file(jenkinsurl,des)
    zipfilepath = os.path.join(des,zipfilename)
    unzipfile(zipfilepath,des)
    for root, dirs, file in os.walk(archivepath):
        for dir in dirs:
            if dir in includelistcpy:
                currentfullpath = os.path.join(root,dir)
                shutil.move(currentfullpath,des)
                includelistcpy.remove(dir)
            if len(includelistcpy) == 0:
                break
        if len(includelistcpy) == 0:
            break

    delete_directory_and_content(archivepath)
    removefile(zipfilepath)

def fetch_buildlog_from_jenkins_to_directory(Servername, Jobname, des):
    print("Getting Build Information From Jenkins...")
    jenkinsurl = "http://" + Servername + "/job/" + Jobname + "/lastSuccessfulBuild/consoleText"
    logfilename = download_file(jenkinsurl,des)
    return logfilename

def parse_buildlog_from_jenkins(Logfile):
    syncingID = 0;
    syncingIDre = re.compile("P4 Task: syncing files at change: ([0-9]*)")
    detailsyncinginfoRE = re.compile("Change ([0-9]*?) on (.*?) by (.*?)@(?:.*?) '(.*)")
    with open(Logfile, "r") as file:
        filetext = file.read()
        info = syncingIDre.search(filetext)
        if info:
            syncingID = info.group(1)
        else:
            return (-1, -1, -1, -1)
    with open(Logfile) as file:
        for line in file:
            resultinfo = detailsyncinginfoRE.search(line)
            if resultinfo and resultinfo.group(1) == syncingID:
                return (resultinfo.group(1), resultinfo.group(2), resultinfo.group(3), resultinfo.group(4))
        return (syncingID, "Unknown", "Unknown", "Unknown")

def parse_log_for_p4_sync_info(Logfile):
    syncingID = 0;
    syncingIDre = re.compile("P4 Task: syncing files at change: ([0-9]*)")
    detailsyncinginfoRE = re.compile("Change ([0-9]*?) on (.*?) by (.*?)@(?:.*?) '(.*)")
    with open(Logfile,"r") as file:
        filetext = file.read()
        info = syncingIDre.search(filetext)
        if info:
            syncingID = info.group(1)
        else:
            return (-1,-1,-1,-1)
    with open(Logfile) as file:
        for line in file:
            resultinfo = detailsyncinginfoRE.search(line)
            if resultinfo and resultinfo.group(1) == syncingID:
                return (resultinfo.group(1),resultinfo.group(2),resultinfo.group(3),resultinfo.group(4))
        return (syncingID, "Unknown", "Unknown", "Unknown")

def change_build_display_name(server_name, job_name, build_num, display_name):
    serverurl = 'http://' + server_name + "/"
    subprocess.call([JENKINS_CLI_CALLER,
                     JENKINS_OPTION_SERVER_URL,
                     serverurl,
                     JENKINS_CLI_FUNCTION_SETBUILD_DISPLAY_NAME,
                     job_name,
                     build_num,
                     display_name])

def change_build_discribtion(server_name, job_name, build_num, discribtion):
    serverurl = 'http://' + server_name + "/"
    subprocess.call([JENKINS_CLI_CALLER,
                     JENKINS_OPTION_SERVER_URL,
                     serverurl,
                     JENKINS_CLI_FUNCTION_SETBUILD_DISPLAY_NAME,
                     job_name,
                     build_num,
                     discribtion])

