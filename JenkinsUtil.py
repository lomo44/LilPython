# Utility Functions regarding Jenkins
import re
import subprocess


JENKINS_CLI_CALLER = 'java -jar jenkins-cli.jar'
JENKINS_OPTION_SERVER_URL = '-s'
JENKINS_CLI_FUNCTION_SETBUILD_DISPLAY_NAME = "set-build-display-name"

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