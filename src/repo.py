import requests
import sys
import os
import json
import platform


def request(url):
    if url.startswith("file:///"):
        file = open(url[7:len(url)], "r")
        ret = file.read()
        file.close()
        return ret
    else:
        return requests.get(url)


def check_repo(url):
    status = True
    try:
        status = len(request(url + "apps.list")) > 0
    except Exception as e:
        status = False
    return status


if os.getenv("SRC") is None:
    print("$SRC is not defined, cannot locate minpin config")
    exit(-1)

home = os.getenv("SRC") + "/"
args = sys.argv

if len(args) <= 1:
    print("Insufficient arguments for operation 'repo'")
    exit(-1)

file = open(home + "conf/repo-list.json")
repo_list = json.loads(file.read())
file.close()

if args[1] == "list":
    for repo in repo_list:
        print(repo + ":")
        state = "Up"
        if not check_repo(repo_list[repo]):
            state = "Down"
        print("  " + repo_list[repo] + " [" + state + "]\n")
elif args[1] == "state":
    if len(args) == 2:
        for repo in repo_list:
            state = "Up"
            if not check_repo(repo_list[repo]):
                state = "Down"
            print(repo + " = " + state)
    else:
        repo = ""
        try:
            repo = args[2]
            state = "Up"
            if not check_repo(repo_list[repo]):
                state = "Down"
            print(state)
        except Exception as e:
            print("Not found in repo-list")
            exit(-1)
else:
    print("Unknown operation '" + args[1] + "'")
    exit(-1)
