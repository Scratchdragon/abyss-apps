import requests
import sys
import json
import os

if os.getenv("SRC") is None:
    print("$SRC is not defined, cannot locate minpin config")
    exit(-1)

home = os.getenv("SRC") + "/"


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

repo = ""
truename = ""

file = open(home + "conf/repo-list.json")
repo_list = json.loads(file.read())
file.close()

for repo_name in repo_list:
    trepo = repo_list[repo_name]
    applist = request(trepo + "apps.list").split()

    found = []
    for item in applist:
        if args[1].lower() == item.lower():
            truename = item
            repo = trepo

if truename != "":
    rawdata = request(repo + truename + "/package.json")
    data = json.loads(rawdata)
    print("Package " + data["name"])
    print("-" * len("Package " + data["name"]))
    print("  Author:")
    print("    " + data["author"])
    print("  Version:")
    print("    " + data["version"])
    print("  Description:")
    print("    " + data["description"])
    print("  Depends on:")
    dependencies = data["dependencies"]
    for key in dependencies.keys():
        print("    " + key + " " + dependencies[key])
else:
    print("Package not found")
