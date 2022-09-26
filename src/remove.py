import requests
import sys
import os
import json
import platform

home = "/etc/minpin/"
exe = home + "bin"
tmp = home + "tmp"
conf = home + "conf"


def safe_exit(code):
    os.system("rm " + tmp + "/install.sh > /dev/null")
    exit(code)


def request(url):
    if url.startswith("file:///"):
        file = open(url[7:len(url)], "r")
        ret = file.read()
        file.close()
        return ret
    else:
        return requests.get(url)


args = sys.argv

if len(args) == 1:
    print("No package specified")
    exit(0)

repo = "file:///etc/minpin/apps/"

applist = request(repo + "apps.list").split()

truename = ""
for item in applist:
    if item.lower() == args[1].lower():
        truename = item

if truename != "":
    print("Getting package data")
    rawdata = request(repo + truename + "/package.json")
    data = json.loads(rawdata)
    # Constructing command
    command = "name='" + data["name"] + "' version='" + data[
        "version"] + "' BIN='" + exe + "' bash " + tmp + "/remove.sh"
    # Locate install script
    remove = ""
    if "*" in data["remove"]:
        remove = data["remove"]["*"]
    elif platform.machine() in data["remove"]:
        remove = data["remove"][platform.machine()]
    else:
        print("No valid removal script found for '" + platform.machine() + "'")
        exit(-1)
    # Download install script
    print("Downloading package removal script")
    file = open(tmp + "/remove.sh", "w")
    file.write(request(repo + truename + "/" + remove))
    file.close()
    # do the thing
    print("Running removal script")
    print("[ " + command + " ]")
    ret = os.system(command)
    os.system("rm " + tmp + "/remove.sh > /dev/null")
    if ret == 0:
        print(data["name"] + " removed")
    else:
        print(tmp + "/remove.sh non-zero exit code '" + str(ret) + "'")
    exit(ret)

else:
    print("Package not found")
