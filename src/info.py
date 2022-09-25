import requests
import sys
import json

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

repo = "file:///etc/abyss-apps/apps/"

applist = request(repo+"apps.list").split()

truename = ""
for item in applist:
    if item.lower() == args[1].lower():
        truename = item

if truename != "":
    rawdata = request(repo+truename+"/package.json")
    data = json.loads(rawdata)
    print("Package " + data["name"])
    print("-"*len("Package " + data["name"]))
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