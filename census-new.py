import sys
import os
import time
import urllib.parse
import requests
from tqdm import tqdm
import csv
import threading
import colorama
colorama.init()

# ---------------------------- START MENU ---------------------------- #


def start_menu():
    purple = '\033[105m'
    red = '\u001B[31m'
    green = '\033[32m'
    yellow = '\033[93m'
    endbgr = '\033[49m'
    endfgr = '\033[39m'

    os.system('cls')
    print(f'{purple} CENSUS: GitHub contributors & fork lists parser {endbgr}')
    print(f"""
    {green} ▄▄▀▀█▀▀▄▄{endfgr}           #-----{yellow}MENU{endfgr}-----#
    {green}▐▄▌─▀─▀─▐▄▌{endfgr}               [{yellow}repo{endfgr}]
    {green}  █─▄▄▄─█  ▄▄{endfgr}             [{yellow}fork{endfgr}]
    {green}  ▄█▄▄▄█▄ ▐  ▌{endfgr}            [{yellow}anon{endfgr}]
    {green}▄█▀█████▐▌ ▀ ▐{endfgr}            [{green}auth{endfgr}]
    {green}▀ ▄██▀██▀█▀▄▄▀{endfgr}            [{green}help{endfgr}]
                              [{red}quit{endfgr}]\n""")
    choice = str(input(f'{yellow}>>>{endfgr} ')).lower().strip(' ')
    return choice


def executor(choice):
    if choice == 'repo':
        repo_parser()
    elif choice == 'fork':
        fork_parser()
    elif choice == 'auth':
        auth()
    elif choice in {'help', 'h', '-h', '--help'}:
        help_info()
    elif choice in {'quit', 'q', ':q', '--quit', 'exit', 'exit()'}:
        quit()
    elif choice in {'anon', 'a', 'anonymous'}:
        anonymous_writer()
    else:
        main()

# ---------------------------- LIMITS & AUTH ---------------------------- #


def rate_limit():
    try:
        os.system('cls')
        URL = f'https://api.github.com/rate_limit'
        f = open(resource_path('token.txt'), "r")
        token = f.read()
        headers = {'Authorization': 'token ' + str(token)}
        r = requests.get(url=URL, headers=headers)
        r_limit = r.json()
        x_limit = r_limit['rate']
        limit = x_limit['limit']
        remaining = x_limit['remaining']
        green = '\033[32m'
        endcolor = '\033[0m'
        print(
            f'TOKEN CHECK: {green}VALID{endcolor}\nRequests limit: {limit}\nRequests remains: {remaining}')
        time.sleep(0.5)
        main()
    except (KeyError, ValueError):
        try:
            os.system('cls')
            red = '\033[91m'
            yellow = '\033[93m'
            endcolor = '\033[0m'
            print(f'{red}INVALID TOKEN:{endcolor} {yellow}Your token is not valid{endcolor}')
            time.sleep(1)
            question = input(
                f'\nDo you still want to continue with an {red}invalid token{endcolor} ? [y/n/show token]: ').lower().strip(' ')
            if question == 'y':
                main()
            elif question == 'n':
                os.system('cls')
                auth()
            elif question == 'show token':
                print(token)
                time.sleep(5)
                rate_limit()
            else:
                rate_limit()
        except KeyboardInterrupt:
            quit()

    except FileNotFoundError:
        try:
            os.system('cls')
            red = '\033[91m'
            yellow = '\033[93m'
            endcolor = '\033[0m'
            print(f'{red}AUTHENTICATION REQUIRED:{endcolor} {yellow}Please, tell me who you are{endcolor}')
            time.sleep(3)
            auth()
        except KeyboardInterrupt:
            quit()
    except(requests.exceptions.ConnectionError):
        try:
            red = '\033[91m'
            endcolor = '\033[0m'
            print(f'{red}NO INTERNET CONNECTION{endcolor}')
            time.sleep(2)
            os.system('cls')
            main()
        except KeyboardInterrupt:
            quit()
    except KeyboardInterrupt:
        quit()


def auth():
    purple = '\033[105m'
    endbgr = '\033[49m'
    os.system('cls')
    print(f'{purple} Setting up token {endbgr}')
    print('\n{[../] to main menu, [help] for help,' '[:q] for exit}\n')
    token = input('Enter your GitHub token: ').lower().replace(' ', '')
    if token == 'quit':
        os.system('cls')
        sys.exit()
    elif token == '../':
        rate_limit()
    elif token == 'help':
        os.system('cls')
        print('#--HELP--#\n')
        print('IF YOU DONT KNOW WHAT TOKEN IS:\n')
        print('1. Sign in or sign up on GitHub.com \n')
        print('2. Follow this link:\n')
        print('https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token \n')
        print('3. Copy your token and paste it here\n')
        print('#--returning in 10 sec--#')
        time.sleep(10)
        auth()
    else:
        os.system('cls')
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        print('Current program directory is:', base_path)
        path_choice = input(
            '\nShould I generate path myself or you will insert it manualy ? [man/auto]: ')
        if path_choice == 'man':
            try:
                os.system('cls')
                file_path = input('Insert the correct path to the program directory: ').strip(' ')
                f = open(f'{file_path}/token.txt', 'w')
                f.write(token)
                f.close()
                rate_limit()
            except FileNotFoundError:
                print('\nERROR: I see no such directory')
                time.sleep(2)
                os.system('cls')
                auth()
            except PermissionError:
                print(
                    '\nERROR: Due to OS settings, I have no permisson to write the file in the following directory')
                time.sleep(4)
                os.system('cls')
                auth()
        elif path_choice == 'auto':
            os.system('cls')
            f = open(resource_path('token.txt'), "w")
            f.write(token)
            f.close()
            print('File saved at', os.path.realpath(f.name))
            print('\nNew authentication try in 2 sec ')
            time.sleep(2)
            rate_limit()
        else:
            auth()

# ---------------------------- HELPER FUNCS ---------------------------- #
# ABSOLUTE PATH TO RESOURCE FOR PYINSTALLER


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# ANIMATION


def animation(stop):
    red = '\033[91m'
    yellow = '\033[93m'
    endcolor = '\033[0m'
    while True:
        os.system('cls')
        print(f'{red}RAM: {yellow}collecting users{endcolor} {red}|{endcolor}')
        time.sleep(0.1)
        os.system('cls')
        print(f'{red}RAM: {yellow}collecting users{endcolor} {red}/{endcolor}')
        time.sleep(0.1)
        os.system('cls')
        print(f'{red}RAM: {yellow}collecting users{endcolor} {red}—{endcolor} ')
        time.sleep(0.1)
        os.system('cls')
        print(f'{red}RAM: {yellow}collecting users{endcolor} {red}\\{endcolor}')
        time.sleep(0.1)
        os.system('cls')
        if stop():
            break

# STAGE


def stage():
    red = '\033[91m'
    yellow = '\033[93m'
    endcolor = '\033[0m'
    print(f'{red}RAM: {yellow}collecting users{endcolor}')

# LINE FLUSH


def line_flusher():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

# USER HELP


def help_info():
    line_flusher()
    print('TEST')
    print('press [Enter] to escape')
    esc = input('')
    if esc is None:
        main()
    else:
        main()

# QUIT APP


def quit():
    os.system('cls')
    sys.exit()


# ---------------------------- REPO PARSER --------------------------- #
def repo_parser():
    yellow = '\033[93m'
    endfgr = '\033[39m'
    start = time.monotonic()
    f = open(resource_path('token.txt'), "r")
    token = f.read()
    headers = {'Authorization': 'token ' + str(token)}
    line_flusher()
    print('[repo]: url type: auto/custom\n')
    link_type = input(f'{yellow}>>>{endfgr} ')
    if link_type in {'auto', 'a', 'aut'}:
        line_flusher()
        line_flusher()
        line_flusher()
        print('[repo]: url type: auto')

        user_input = urllib.parse.urlsplit(str(input(f"\n{yellow}>>>{endfgr} "))).path
        if user_input == '../':
            line_flusher()
            line_flusher()
            repo_parser()
        else:
            try:
                stage()
                fragment = user_input.split("/")

                URL = "https://api.github.com/repos/" + \
                    str(fragment[1]) + "/" + str(fragment[2]) + "/contributors"
                r = requests.get(url=URL, headers=headers)
                collaborators = r.json()

                while "next" in r.links.keys():
                    r = requests.get(r.links["next"]["url"], headers=headers)
                    collaborators.extend(r.json())

                names = [i["login"] for i in collaborators]
                csv_writer(names, start)
            except (KeyError, ValueError, IndexError, TypeError):
                # stop_threads = True
                # t1.join()
                print('Exception: something bad just occured: broken url')
                time.sleep(1)
                line_flusher()
                line_flusher()
                line_flusher()
                line_flusher()
                repo_parser()
            except(requests.exceptions.ConnectionError):
                red = '\033[91m'
                endcolor = '\033[0m'
                print(f'{red}NO INTERNET CONNECTION{endcolor}')
                time.sleep(2)
                line_flusher()
                line_flusher()
                line_flusher()
                line_flusher()
                repo_parser()

    elif link_type in {'manual', 'man', 'm', 'c', 'cus', 'custom'}:
        line_flusher()
        line_flusher()
        line_flusher()
        line_flusher()
        custom_url = str(input(f"""
[repo]: url type: custom
[example]: https://api.github.com/repos/:owner/:repo/collaborators
{yellow}>>>{endfgr} """))
        if custom_url != '../':
            try:
                r = requests.get(url=custom_url, headers=headers)
                forkers = r.json()
                while "next" in r.links.keys():
                    r = requests.get(r.links["next"]["url"], headers=headers)
                    forkers.extend(r.json())
                owners = [i["owner"] for i in forkers]
                names = [i["login"] for i in owners]
                csv_writer(names, start)
            except (KeyError, ValueError):
                print('Exception: something bad just occured: broken url')
                time.sleep(0.5)
                line_flusher()
                line_flusher()
                line_flusher()
                repo_parser()
            except(requests.exceptions.ConnectionError):
                red = '\033[91m'
                endcolor = '\033[0m'
                print(f'{red}NO INTERNET CONNECTION{endcolor}')
                time.sleep(2)
                line_flusher()
                line_flusher()
                line_flusher()
                repo_parser()
        else:
            line_flusher()
            line_flusher()
            repo_parser()

    elif link_type == '../':
        main()

    else:
        line_flusher()
        line_flusher()
        repo_parser()


# --------------------------- FORK PARSER --------------------------- #

def fork_parser():
    yellow = '\033[93m'
    endfgr = '\033[39m'
    start = time.monotonic()
    f = open(resource_path('token.txt'), "r")
    token = f.read()
    headers = {'Authorization': 'token ' + str(token)}
    line_flusher()
    print('[fork]: url type: auto/custom\n')
    link_type = input(f'{yellow}>>>{endfgr} ')
    if link_type in {'auto', 'a', 'aut'}:
        line_flusher()
        line_flusher()
        line_flusher()
        print('[fork]: url type: auto')
        user_input = urllib.parse.urlsplit(str(input(f'\n{yellow}>>>{endfgr} '))).path
        fragment = user_input.split("/")

        if user_input == '../':
            line_flusher()
            line_flusher()
            fork_parser()
        else:
            try:
                stage()
                # stop_threads = False
                # t1 = threading.Thread(target=animation, args=(lambda: stop_threads, ))
                # t1.start()
                URL = "https://api.github.com/repos/" + \
                    str(fragment[1]) + "/" + str(fragment[2]) + "/forks"
                r = requests.get(url=URL, headers=headers)
                forkers = r.json()

                if not forkers:
                    # stop_threads = True
                    # t1.join()
                    print("Invalid link. Trying to reconfigure it ...")

                    URL = "https://api.github.com/repos/" + \
                        str(fragment[2]) + "/" + str(fragment[2]) + "/forks"
                    r = requests.get(url=URL, headers=headers)
                    forkers = r.json()

                    while "next" in r.links.keys():
                        r = requests.get(r.links["next"]["url"], headers=headers)
                        forkers.extend(r.json())

                    owners = [i["owner"] for i in forkers]
                    names = [i["login"] for i in owners]
                    print('Successfully done')
                    csv_writer(names, start)

                while "next" in r.links.keys():
                    r = requests.get(r.links["next"]["url"], headers=headers)
                    forkers.extend(r.json())

                owners = [i["owner"] for i in forkers]
                names = [i["login"] for i in owners]
                print('Successfully done')
                # stop_threads = True
                # t1.join()
                csv_writer(names, start)
            except (KeyError, ValueError, IndexError, TypeError):
                # stop_threads = True
                # t1.join()
                print('Exception: something bad just occured: broken url')
                time.sleep(1)
                line_flusher()
                line_flusher()
                line_flusher()
                line_flusher()
                fork_parser()
            except(requests.exceptions.ConnectionError):
                red = '\033[91m'
                endcolor = '\033[0m'
                print(f'{red}NO INTERNET CONNECTION{endcolor}')
                time.sleep(2)
                line_flusher()
                line_flusher()
                line_flusher()
                line_flusher()
                fork_parser()

    elif link_type in {'manual', 'man', 'm', 'c', 'cus', 'custom'}:
        line_flusher()
        line_flusher()
        line_flusher()
        line_flusher()
        custom_url = str(input(f"""
[fork]: url type: custom
[example]: https://api.github.com/repos/:owner/:repo/forks
{yellow}>>>{endfgr} """))
        if custom_url != '../':
            try:
                r = requests.get(url=custom_url, headers=headers)
                forkers = r.json()
                while "next" in r.links.keys():
                    r = requests.get(r.links["next"]["url"], headers=headers)
                    forkers.extend(r.json())
                owners = [i["owner"] for i in forkers]
                names = [i["login"] for i in owners]
                csv_writer(names, start)
            except (KeyError, ValueError, IndexError, TypeError):
                print('Exception: something bad just occured: broken url')
                time.sleep(1)
                line_flusher()
                line_flusher()
                line_flusher()
                fork_parser()
            except(requests.exceptions.ConnectionError):
                red = '\033[91m'
                endcolor = '\033[0m'
                print(f'{red}NO INTERNET CONNECTION{endcolor}')
                time.sleep(2)
                line_flusher()
                line_flusher()
                line_flusher()
                fork_parser()
        else:
            line_flusher()
            line_flusher()
            fork_parser()

    elif link_type == '../':
        main()

    else:
        line_flusher()
        line_flusher()
        fork_parser()

# ---------------------------- ANONYMOUS WRITER --------------------------- #


def anonymous_writer():
    line_flusher()
    red = '\033[91m'
    yellow = '\033[93m'
    endcolor = '\033[0m'
    start = time.monotonic()
    f = open(resource_path('token.txt'), "r")
    token = f.read()
    headers = {'Authorization': 'token ' + str(token)}

    print("This is a tracker of anonymous contributors")
    print("Please note that the final data will be different from the regular output")
    user_input = urllib.parse.urlsplit(str(input(f"\n{yellow}>>>{endcolor} "))).path
    if user_input != '../':
        try:
            stage()
            fragment = user_input.split("/")
            URL = "https://api.github.com/repos/" + \
                str(fragment[1]) + "/" + str(fragment[2]) + \
                "/contributors?anon=1"
            r = requests.get(url=URL, headers=headers)
            collaborators = r.json()

            while "next" in r.links.keys():
                r = requests.get(r.links["next"]["url"], headers=headers)
                collaborators.extend(r.json())

            anons = [i for i in collaborators if i["type"] == "Anonymous"]
            keys = anons[0].keys()
            print('Successfully done')
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            print(f'{red}CSV:{endcolor} {yellow}file path{endcolor}')
            print('File will be saved at:', base_path)
            p_choice = input('Set the path manualy? [y/n]: ').lower().strip(' ')
            if p_choice in {'y', 'yes'}:
                file_path = input(f'Set the path: ').strip(' ')
            elif p_choice in {'n', 'no'}:
                file_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            else:
                line_flusher()
                line_flusher()
                line_flusher()
                anonymous_writer()

            file_name = input(f'Enter file name: ')
            print('Successfully done')
            print(f'{red}CSV:{endcolor} {yellow}saving users{endcolor}')
            with open(f'{file_path}/{file_name}.txt', 'w', encoding='utf-8') as filename:
                writer = csv.DictWriter(filename, delimiter=";", fieldnames=keys)
                writer.writeheader()
                writer.writerows(tqdm(anons))

            print(str("Users parsed: ") + str(len(anons)))
            print("Writing completed")
            result = time.monotonic() - start
            print("Program time: " + str(result) + " seconds.")
            print(f'\n{red}press [Enter] to escape{endcolor}')
            esc = input('')
            if esc is None:
                main()
            else:
                main()
        except (KeyError, ValueError, IndexError, TypeError):
            print('Exception: something bad just occured: broken url')
            time.sleep(1)
            line_flusher()
            line_flusher()
            line_flusher()
            line_flusher()
            line_flusher()
            anonymous_writer()
        except(requests.exceptions.ConnectionError):
            red = '\033[91m'
            endcolor = '\033[0m'
            print(f'{red}NO INTERNET CONNECTION{endcolor}')
            time.sleep(2)
            line_flusher()
            line_flusher()
            line_flusher()
            fork_parser()

    else:
        main()


# ---------------------------- CSV WRITER --------------------------- #


def csv_writer(names, start):
    red = '\033[91m'
    yellow = '\033[93m'
    endcolor = '\033[0m'
    f = open(resource_path('token.txt'), "r")
    token = f.read()
    headers = {'Authorization': 'token ' + str(token)}
    # os.system('cls')
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(f'{red}CSV:{endcolor} {yellow}file path{endcolor}')
    print('File will be saved at:', base_path)
    p_choice = input('Set the path manualy? [y/n]: ').lower().strip(' ')
    if p_choice in {'y', 'yes'}:
        file_path = input(f'Set the path: ').strip(' ')
    elif p_choice in {'n', 'no'}:
        file_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    else:
        line_flusher()
        line_flusher()
        line_flusher()
        csv_writer(names, start)

    file_name = input(f'Enter file name: ')
    print('Successfully done')
    with open(f'{file_path}/{file_name}.txt', 'w', encoding='utf-8') as filename:
        # os.system('cls')
        print(f'{red}CSV:{endcolor} {yellow}saving users{endcolor}')
        writer = None
        for i in tqdm(names):
            URL = "https://api.github.com/users/" + i
            r = requests.get(url=URL, headers=headers)
            data = r.json()
            URL = "https://api.github.com/users/" + i + "/repos"
            r = requests.get(url=URL, headers=headers)
            user_repos = r.json()
            languages = [i["language"] for i in user_repos if i["language"] !=
                         None if i["language"] != "Makefile"]   # searching languages
            # counting % languages
            langs_counted = {
                i: f"{round(languages.count(i)/len(languages)*100, 2)}%" for i in set(languages)}
            readout = {'Username': data['login'], 'Full Name': data['name'], 'Email': data['email'],
                       'Location': data['location'], 'Company': data['company'], 'Hireable Status': data['hireable'],
                       'Languages': langs_counted, 'Profile Summary': 'https://profile-summary-for-github.com/user/' + data['login']}
            if not writer:
                writer = csv.DictWriter(filename, delimiter=';', fieldnames=readout.keys())
            writer.writerow(readout)

    print(str("Users parsed: ") + str(len(names)))
    print("Writing completed")
    result = time.monotonic() - start
    print("Program time: " + str(result) + " seconds.")
    print(f'\n{red}press [Enter] to escape{endcolor}')
    esc = input('')
    if esc is None:
        main()
    else:
        main()

# ---------------------------- MAIN LOGIC ---------------------------- #


def main():
    choice = start_menu()
    executor(choice)


if __name__ == "__main__":
    rate_limit()
