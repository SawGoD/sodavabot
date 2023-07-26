import requests


def get_changes():
    url = f"https://api.github.com/repos/SawGoD/sodavabot/commits"
    response = requests.get(url)
    output = ""
    if response.status_code == 200:
        commits = response.json()
        commits = commits[:5]

        for commit in commits:
            commit_message = commit['commit']['message']
            commit_date = commit['commit']['author']['date'][:10]
            commit_author = commit['author']['login']
            commit_url = commit['html_url']

            output += f'''
*Обновление* - {commit_date} от [{commit_author}](https://github.com/{commit_author}):
    *Изменения:* [{commit_message}]({commit_url})
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'''
    return output
