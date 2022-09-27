import requests
import sys
import json
import os


def request(url):
    if url.startswith("file:///"):
        file = open(url[7:len(url)], "r")
        ret = file.read()
        file.close()
        return ret
    else:
        return requests.get(url)


home = os.getenv("SRC") + "/"
args = sys.argv

if len(args) == 1:
    args.append("")

file = open(home + "conf/repo-list.json")
repo_list = json.loads(file.read())
file.close()

for repo_name in repo_list:
    repo = repo_list[repo_name]
    applist = request(repo + "apps.list").split()

    found = []
    for item in applist:
        if args[1].lower() in item.lower():
            found.append(item)
            rawdata = request(repo + item + "/package.json")
            data = json.loads(rawdata)
            print(item + " - " + data["version"])
            print("  " + data["description"] + "\n")
