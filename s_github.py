import os
import requests
from s_handle_db import write_db_cell, read_db_cell
from dotenv import load_dotenv

load_dotenv()


def get_changes(c_from=0, c_to=5):
    url = f"https://api.github.com/repos/SawGoD/sodavabot/commits"
    response = requests.get(url, headers={"Authorization": f"token {os.getenv('API_TOKEN_GIT')}"})
    output = ""
    if response.status_code == 200:
        commits = response.json()
        c_max = int(len(commits))
        write_db_cell("menu_range", c_max, "last")
        c_min = c_max-5
        if c_to >= c_max:
            commits = commits[c_min:c_max]
        else:
            commits = commits[c_from:c_to]
        i = read_db_cell('menu_range', 'last') - read_db_cell('menu_range', 'min') + 1
        for commit in commits:
            i -= 1
            commit_message = commit['commit']['message']
            commit_date = commit['commit']['author']['date'][:10]
            if commit['author'] is None:
                commit_author = commit['commit']['author']['name']
            else:
                commit_author = commit['author']['login']
                # commit_author = "2121"
            commit_url = commit['html_url']

            output += f'''
{i}) *Обновление* - {commit_date} от [{commit_author}](https://github.com/{commit_author}):
*Изменения:* [{commit_message}]({commit_url})
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'''
        output += f"\nСтраница {read_db_cell('menu_range', 'page')} из {int(c_max / 5)}"
    return output
