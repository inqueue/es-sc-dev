from config import Config
import soundcloud

sc_config = Config()
config = sc_config.load_config()
client_id = config['soundcloud']['client_id']
host = config['soundcloud']['api_host']
client = soundcloud.Client(client_id=client_id, host=host)

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

config = Config()
print config.load_config()
