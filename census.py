import sys
import time
import urllib.parse
import requests
from tqdm import tqdm
import csv

#-----------------------------START MENU-----------------------------#

print("""
─▄▄▀▀█▀▀▄▄
▐▄▌─▀─▀─▐▄▌
──█─▄▄▄─█──▄▄  CENSUS: Github repo & fork parser {v.1.0}
──▄█▄▄▄█▄─▐──▌ by Babun: github.com/cacodemon503
▄█▀█████▐▌─▀─▐
▀─▄██▀██▀█▀▄▄▀ Don't forget to create token: help.github.com
							""")
choice = str(input("""Please choose [r] for repo & [f] for fork or [mf/mr] for manual setup
                      or [anon] to get anonymous repo contributors: """))

#-----------------------------REPO PARSER-----------------------------#

if choice == str("r"):
    start = time.monotonic()
    token = open("token.txt" , "r").read()
    headers = {"Authorization": "token " + token}

    user_input = urllib.parse.urlsplit(str(input("Paste URL: "))).path
    fragment = user_input.split("/")

    URL = "https://api.github.com/repos/" + str(fragment[1]) + "/" + str(fragment[2]) + "/contributors" # ?per_page=100&page=1&anon=1
    r = requests.get(url = URL, headers = headers)
    collaborators = r.json()
#     print(URL)

    while "next" in r.links.keys():
        r = requests.get(r.links["next"]["url"], headers = headers)
        collaborators.extend(r.json())

    names = [i["login"] for i in collaborators]

    with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
        print("File will be saved in the program directory ... ")
        writer = None
        for i in tqdm(names):
            URL = "https://api.github.com/users/" + i
            r = requests.get(url = URL, headers = headers)
            data = r.json()
            URL = "https://api.github.com/users/" + i + "/repos"
            r = requests.get(url = URL, headers = headers)
            user_repos = r.json()
            languages = [i["language"] for i in user_repos if i["language"] != None if i["language"] != "Makefile"]   # searching languages
            langs_counted = {i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)} # counting % languages
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                        'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                        'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter=';', fieldnames=readout.keys())
            writer.writerow(readout)

    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

#-----------------------------FORK PARSER-----------------------------#

elif choice == str("f"):
    start = time.monotonic()
    token = open("token.txt" , "r").read()
    headers = {"Authorization": "token " + token}

    user_input = urllib.parse.urlsplit(str(input("Paste URL: "))).path
    fragment = user_input.split("/")
#-----------------------------LINK CHECKER-----------------------------#
    URL = "https://api.github.com/repos/" + str(fragment[1]) + "/" + str(fragment[2]) + "/forks" # ?per_page=100&page=1
    r = requests.get(url = URL, headers = headers)
    forkers = r.json()

    if not forkers:
#---------------------------LINK RECONFIGURE---------------------------#
        print("Wow, this link seems not right. I'll try to reconfigure it for you ...")

        URL = "https://api.github.com/repos/" + str(fragment[2]) + "/" + str(fragment[2]) + "/forks" # ?per_page=100&page=1
        r = requests.get(url = URL, headers = headers)
        forkers = r.json()
#------------------------------NEW TRY---------------------------------#
        while "next" in r.links.keys():
            r = requests.get(r.links["next"]["url"], headers = headers)
            forkers.extend(r.json())

        owners = [i["owner"] for i in forkers]
        names = [i["login"] for i in owners]

        with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
            print("File will be saved in the program directory ... ")
            writer = None
            for i in tqdm(names):
                URL = "https://api.github.com/users/" + i
                r = requests.get(url = URL, headers = headers)
                data = r.json()
                URL = "https://api.github.com/users/" + i + "/repos"
                r = requests.get(url = URL, headers = headers)
                user_repos = r.json()
                languages = [i["language"] for i in user_repos if i["language"] != None if i["language"] != "Makefile"]   # searching languages
                langs_counted = {i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)}
                readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                            'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                                'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
                if not writer:
                    writer = csv.DictWriter(filename, delimiter = ";", fieldnames = readout.keys())
                writer.writerow(readout)

        print(str("Users parsed: ") + str(len(names)))
        print ("Writing completed")
        result = time.monotonic() - start
        print("Program time: " + str(result) + " seconds.")

        # sys.exit()
#---------------------------------NORMAL TRY-----------------------------#
    while "next" in r.links.keys():
        r = requests.get(r.links["next"]["url"], headers = headers)
        forkers.extend(r.json())

    owners = [i["owner"] for i in forkers]
    names = [i["login"] for i in owners]

    with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
        print("File will be saved in the program directory ... ")
        writer = None
        for i in tqdm(names):
            URL = "https://api.github.com/users/" + i
            r = requests.get(url = URL, headers = headers)
            data = r.json()
            URL = "https://api.github.com/users/" + i + "/repos"
            r = requests.get(url = URL, headers = headers)
            user_repos = r.json()
            languages = [i["language"] for i in user_repos if i["language"] != None if i["language"] != "Makefile"]   # searching languages
            langs_counted = {i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)}
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                        'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                            'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter = ";", fieldnames = readout.keys())
            writer.writerow(readout)

    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

#-----------------------------MANUAL REPO PARSER-----------------------------#

elif choice == str("mr"):
    start = time.monotonic()
    token = open("token.txt" , "r").read()
    headers = {"Authorization": "token " + token}

    custom_url = str(input("""[repo]: custom URL
                              [https://api.github.com/repos/:owner/:repo/collaborators]
                              Insert here: """))
    r = requests.get(url = custom_url, headers = headers)
    collaborators = r.json()

    while "next" in r.links.keys():
        r = requests.get(r.links["next"]["url"], headers = headers)
        collaborators.extend(r.json())

    names = [i["login"] for i in collaborators]

    with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
        print("File will be saved in the program directory ... ")
        writer = None
        for i in tqdm(names):
            URL = "https://api.github.com/users/" + i
            r = requests.get(url = URL, headers = headers)
            data = r.json()
            URL = "https://api.github.com/users/" + i + "/repos"
            r = requests.get(url = URL, headers = headers)
            user_repos = r.json()
            languages = [i["language"] for i in user_repos if i["language"] != None if i["language"] != "Makefile"]   # searching languages
            langs_counted = {i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)}
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                        'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                        'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter=';', fieldnames=readout.keys())
            writer.writerow(readout)

    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

#-----------------------------MANUAL FORK PARSER-----------------------------#

elif choice == str("mf"):
    start = time.monotonic()
    token = open("token.txt" , "r").read()
    headers = {"Authorization": "token " + token}

    custom_url = str(input("""[fork]: custom URL
                              [https://api.github.com/repos/:owner/:repo/forks]
                              Insert here: """))
    r = requests.get(url = custom_url, headers = headers)
    forkers = r.json()

    while "next" in r.links.keys():
        r = requests.get(r.links["next"]["url"],headers = headers)
        forkers.extend(r.json())

    owners = [i["owner"] for i in forkers]
    names = [i["login"] for i in owners]

    with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
        print("File will be saved in the program directory ... ")
        writer = None
        for i in tqdm(names):
            URL = "https://api.github.com/users/" + i
            r = requests.get(url = URL, headers = headers)
            data = r.json()
            URL = "https://api.github.com/users/" + i + "/repos"
            r = requests.get(url = URL, headers = headers)
            user_repos = r.json()
            languages = [i["language"] for i in user_repos if i["language"] != None if i["language"] != "Makefile"]   # searching languages
            langs_counted = {i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)}
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                        'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                        'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter = ";", fieldnames = readout.keys())
            writer.writerow(readout)

    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

#-----------------------------ANON REPO PARSER-----------------------------#

elif choice == str("anon"):
    start = time.monotonic()
    token = open("token.txt" , "r").read()
    headers = {"Authorization": "token " + token}

    print("""This is a tracker of anonymous contributors, please note that
             the final data will be different from the regular output""")
    user_input = urllib.parse.urlsplit(str(input("Paste URL: "))).path
    fragment = user_input.split("/")

    URL = "https://api.github.com/repos/" + str(fragment[1]) + "/" + str(fragment[2]) + "/contributors?anon=1" # ?per_page=100&page=1&anon=1
    r = requests.get(url = URL, headers = headers)
    collaborators = r.json()

    while "next" in r.links.keys():
        r = requests.get(r.links["next"]["url"], headers = headers)
        collaborators.extend(r.json())

    anons = [i for i in collaborators if i["type"] == "Anonymous"]
    keys = anons[0].keys()

    with open("{}.txt".format(str(input("Enter file name: "))), "w", encoding = "utf-8") as filename:
        writer = csv.DictWriter(filename, delimiter=";", fieldnames=keys)
        writer.writeheader()
        writer.writerows(tqdm(anons))

    print(str("Users parsed: ") + str(len(anons)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

#-----------------------------END-----------------------------#

else:
    print("Please restart")
