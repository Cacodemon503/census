import time
import urllib.parse
import requests
from tqdm import tqdm
import csv

print("""
─▄▄▀▀█▀▀▄▄
▐▄▌─▀─▀─▐▄▌
──█─▄▄▄─█──▄▄  CENSUS: Github repo & fork parser {v.1.0}
──▄█▄▄▄█▄─▐──▌ by Babun: github.com/cacodemon503 
▄█▀█████▐▌─▀─▐
▀─▄██▀██▀█▀▄▄▀ Don't forget to create token: help.github.com
							""")

choice = str(input("Please choose [r] for repo & [f] for fork or [mf/mr] for manual setup: "))

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
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                   'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                   'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter=';', fieldnames=readout.keys())
            writer.writerow(readout)
                
    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")

elif choice == str("f"):
    start = time.monotonic()
    token = open("token.txt" , "r").read() 
    headers = {"Authorization": "token " + token}
    
    user_input = urllib.parse.urlsplit(str(input("Paste URL: "))).path
    fragment = user_input.split("/")
    
    URL = "https://api.github.com/repos/" + str(fragment[2]) + "/" + str(fragment[2]) + "/forks" # ?per_page=100&page=1
    r = requests.get(url = URL, headers=headers)
    forkers = r.json()
#     print(URL)

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
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                   'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                   'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter = ";", fieldnames = readout.keys())
            writer.writerow(readout)
                
    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")
    
elif choice == str("mr"):
    start = time.monotonic()
    token = open("token.txt" , "r").read() 
    headers = {"Authorization": "token " + token}
    
    custom_url = str(input("""[repo]: custom URL 
                              [https://api.github.com/repos/:owner/:repo/collaborators]
                              Insert here: """))
    r = requests.get(url = custom_url, headers=headers)
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
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                   'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                   'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter=';', fieldnames=readout.keys())
            writer.writerow(readout)
                
    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")
    
elif choice == str("mf"):
    start = time.monotonic()
    token = open("token.txt" , "r").read() 
    headers = {"Authorization": "token " + token}
    
    custom_url = str(input("""[fork]: custom URL 
                              [https://api.github.com/repos/:owner/:repo/forks]
                              Insert here: """))
    r = requests.get(url = custom_url, headers=headers)
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
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                   'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                   'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter = ";", fieldnames = readout.keys())
            writer.writerow(readout)
                
    print(str("Users parsed: ") + str(len(names)))
    print ("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")
    
else:
    print("Please restart")