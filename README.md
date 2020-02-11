## Census: simple GitHub repo & fork parser 

#### [Create your token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
Copy token to `token.txt`, file must be in the same directory with an executable script

IF YOU'LL HAVE ANY ISSUES WITH TRYTING TO LAUNCH IT:

Just copy your token and build it directly into the code:

Delete strings: `25`, `70`, `156`, `199`, `243`
Edit strings: `26`, `71`,`157`, `200`, `244` within the folowing format: 

`headers = {"Authorization": "Token " +  "yourabcdefgh0123token"}`

#### Launch instructions:
* Open cmd/powershell/terminal
* `cd ~/path to script directory`
* `python3 ./census.py`
* Follow further program instructions

* You can type/paste URL of the repo, just try: `https://github.com/kmike/pymorphy2/graphs/contributors`
* You can type/paste URL of the forks, try this for example: `https://github.com/tarantool/tarantool/network/members`
* Input the name of CSV-file, it will appear and save in the program directory

### IMPORTANT NOTE
Sometimes you may recieve an error in fork mode. It happens because current link autoconfig make URL by the following rule: `user/repo`, but some forks may work under the rule: `repo/repo`. So just use manual configure mode for now. It will be fixed soon

You can also manually surf through GitHub API and create your own links accodrind to the following structure: `/repos/:owner/:repo/forks` and `/repos/:owner/:repo/contributors`

This script requiers [Python3](https://www.python.org/), [Requests module](https://2.python-requests.org/en/master/), [tqdm module](https://github.com/tqdm/tqdm)

### If you want to make it easily executable on linux:
Make a new empty `census.py` file in the directory where you want to store it with `touch census.py` command

Add `#!/usr/bin/python3` at the top of the script

Copy all of the code to the new file & save it

Run: `chmod +x census.py` 

Add a Directory with your script to `$PATH:` permanently by running the following in Terminal:`nano ~/.bashrc`

Add in the end of the file `PATH=$PATH:~/YOUR NEW PATH TO SCRIPT`, mark it with `##PATH##` for further needs

Save & exit wtih: `ctrl+O` `ctrl+X`

Run: `source ~/.bashrc`

Confirm changes: `echo $PATH`

You'll see the path to your new directory in the end of the line

Now you can launch it in Terminal from every directory by running: `census.py` 


