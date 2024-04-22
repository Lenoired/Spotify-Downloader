# Spotify downloader
# Uses spotifydown.com API
from requests import Session
from threading import Thread
from sys import argv
if len(argv)<2 or argv[1].find('/track/')<=0 and argv[1].find('/playlist/')<=0:
  exit(f"Usage: python {argv[0]} <spotify song link>")


# Download concurrent
# 2 = 2 songs downloading at the same time
max_ths = 2

# Download location, must end in "/"
location = "./"

# Colors
green = "\u001b[32;1m"
red = "\u001b[31;1m"
reset = "\u001b[0m"


def sanitize(title):
  return [title := title.replace(char, "") for char in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']][-1]


def download(id):
  r = handler.get(f"https://api.spotifydown.com/download/{id}", headers={"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36", "Origin": "https://spotifydown.com", "Referer": "https://spotifydown.com/"})
  title = sanitize(r.json()['metadata']['title'])
  artists = r.json()['metadata']['artists']
  url = r.json()['link']
  print(f"Downloading {green}{title}{reset} by {green}{artists}{reset}")
  with handler.get(url, stream=True) as r:
    with open(f"{location}{title}.mp3","wb") as f:
      for chunk in r.iter_content(chunk_size=14000):
        f.write(chunk)

  print(f"Downloaded {green}{title}{reset}")


handler = Session()
id = argv[1].split('fy.com/')[1].split('/')[1].split('?si')[0]
if argv[1].find('/track/')>0:
  download(id)
elif argv[1].find('/playlist/')>0:
  r = handler.get(f"https://api.spotifydown.com/trackList/playlist/{id}", headers={"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36", "Origin": "https://spotifydown.com", "Referer": "https://spotifydown.com/"})
  if '"success":false' in r.text: exit(red + r.json()['message'] + reset)
  ths = []
  for idx in r.json()['trackList']:
    th = Thread(target=download, args=(idx['id'],))
    th.start()
    ths.append(th)
    if len(ths)>=max_ths:
      for worker in ths: worker.join()
      ths = []



