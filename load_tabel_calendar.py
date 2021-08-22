import requests

#target_url = "https://raw.githubusercontent.com/CyberFox404/tabel_calendar/main/main.py"
target_url = "https://raw.githubusercontent.com/CyberFox404/tabel/main/main.py"
r = requests.get(target_url, allow_redirects=True)

#open('tabel_calendar_2021_load.py', 'wb').write(r.content)
open('tabel_calendar_2021_load.py', 'w').write(r.content)

with open("tabel_calendar_2021_load.py") as f:
    content = f.read()

exec(content)