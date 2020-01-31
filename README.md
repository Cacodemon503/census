#### [Создать токен](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
Скопировать токен в `token.txt`, файл должен находится в одной директории с исполняемым скриптом

Или скопировать токен в код исполняемого скрипта:

`headers = {"Authorization": "Token " +  "yourabcdefgh0123token"}`

#### Запустить:
* Открыть cmd/powershell/terminal
* `cd ~/Путь до директории с файлом`
* `python3 ./census.py`
* Следовать инструкции скрипта

* Ввести URL интересующего репозитория, например: `https://github.com/kmike/pymorphy2/graphs/contributors`
* Ввести URL интересующего списка форков, например: `https://github.com/tarantool/tarantool/network/members`
* Ввести название CSV-файла, файл будет сохранен в директории с программой

Можно также вводить кастомные ссылки на основе: `/repos/:owner/:repo/forks` и `/repos/:owner/:repo/contributors`

Для работы скрипта нужен [Python3](https://www.python.org/), [модуль Requests](https://2.python-requests.org/en/master/), [модуль tqdm](https://github.com/tqdm/tqdm)

#### If you want to make it easily executable on linux:
Make a new empty `census.py` file in the directory where you want to store it with `touch census.py` command

Add `#!/usr/bin/env python` at the top of the script

Copy all of the code to the new file & save it

Add a Directory with your script to `$PATH:` permanently by running the following in Terminal:`nano ~/.bashrc`

Add in the end of the file `PATH=$PATH:~/"YOUR NEW PATH TO SCRIPT`, mark it with `##PATH##` for further needs

Save & exit wtih: `ctrl+O` `ctrl+X`

Run: `source ~/.bashrc`

Confirm changes: `echo $PATH`

You'll see the path to your new directory in the end of the line

Now you can launch it in Terminal from every directory by running: `census.py` 


