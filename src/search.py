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
    args.append("")

repo = "file:///etc/minpin/apps/"

applist = request(repo + "apps.list").split()

found = []
for item in applist:
    if args[1].lower() in item.lower():
        found.append(item)
        rawdata = request(repo + item + "/package.json")
        data = json.loads(rawdata)
        print(item + " - " + data["version"])
        print("  " + data["description"] + "\n")

if len(found) == 0:
    print("No package found")