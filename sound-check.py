from os.path import expanduser
import ConfigParser
import soundcloud

home_dir = expanduser("~")
config_file = home_dir + "/.es-soundcloud/es-soundcloud.ini"

config = ConfigParser.ConfigParser()
config.read(config_file)

client_id = config.get("soundcloud", "client_id")
client_secret = config.get("soundcloud", "client_secret")
sc_host = config.get("soundcloud", "api_host")

client = soundcloud.Client(client_id=client_id, host=sc_host)

# get the first 100 trending tracks
trending = client.get('/explore/Popular+Music', limit=100)

for track in trending.tracks:
    print (track)

print (trending.next_href)

trending = client.get('/explore/Popular+Music', limit=100,
                      linked_partitioning=1)

for track in trending.tracks:
    print (track['title'].encode("utf-8"))

print (trending.next_href)

trending = client.get('https://api-v2.soundcloud.com/explore/Popular+Music?offset=100&tag=out-of-experiment&limit=100',
                      limit=100, linked_partitioning=1)

for track in trending.tracks:
    print (track['title'].encode("utf-8"))

print (trending.next_href)
