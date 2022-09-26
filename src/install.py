import requests
import sys
import json

home = "/home/declan/Projects/abyss-apps/"
exe = home + "bin"
tmp = home + "tmp"
conf = home + "conf"


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
    try:
        alias = data[dependency][version]
        print("Found apt package '" + alias + "'")
    except Exception as e:
        print("No apt package found for dependency. Aborting")
        exit(0)


args = sys.argv

if len(args) == 1:
    print("No package specified")
    exit(0)

repo = "file:///home/declan/Projects/abyss-apps/apps/"

applist = request(repo + "apps.list").split()

truename = ""
for item in applist:
    if item.lower() == args[1].lower():
        truename = item

if truename != "":
    rawdata = request(repo + truename + "/package.json")
    data = json.loads(rawdata)
    # Constructing command
    command = "name='" + data["name"] + "' version='" + data["version"] + "' BIN=" + exe + "' bash " + tmp + "/install.sh"
    # Download install script
    file = open(tmp + "/install.sh", "w")
    file.write(request(repo + truename + "/install.sh"))
    file.close()
    # Dependencies
    for pkg in data["dependencies"]:
        resolve_dep(pkg, data["dependencies"][pkg])
else:
    print("Package not found")
