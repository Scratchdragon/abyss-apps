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


def resolve_dep(dependency, version):
    print("Getting alias for dependency '" + dependency + "' of version '" + version + "'")
    file = open(conf + "/pkg-alias.json", "r")
    data = json.loads(file.read())
    alias = ""
    try:
        alias = data[dependency][version]
    except Exception as e:
        print("No apt package found for dependency. Aborting")
        safe_exit(-1)

    print("Found apt package '" + alias + "', installing...")
    ret = os.system("apt install " + alias)
    if ret == 0:
        print(dependency + "installed")
    else:
        print("'apt' returned non-zero exit code '" + str(ret) + "'")
        safe_exit(-1)


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
        "version"] + "' BIN='" + exe + "' bash " + tmp + "/install.sh"
    # Locate install script
    install = ""
    if "*" in data["install"]:
        install = data["install"]["*"]
    elif platform.machine() in data["install"]:
        install = data["install"][platform.machine()]
    else:
        print("No valid install script found for '" + platform.machine() + "'")
        exit(-1)
    # Download install script
    print("Downloading package install script")
    file = open(tmp + "/install.sh", "w")
    file.write(request(repo + truename + "/" + install))
    file.close()
    # Dependencies
    print("Resolving dependencies")
    for pkg in data["dependencies"]:
        resolve_dep(pkg, data["dependencies"][pkg])
    # do the thing
    print("Running install script")
    print("[ " + command + " ]")
    ret = os.system(command)
    os.system("rm " + tmp + "/install.sh > /dev/null")
    if ret == 0:
        print(data["name"] + " installed")
    else:
        print(tmp + "/install.sh returned non-zero exit code '" + str(ret) + "'")
    exit(ret)

else:
    print("Package not found")
