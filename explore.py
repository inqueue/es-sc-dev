from config import Config
import soundcloud
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import itertools

def dowhile(predicate):
    iter = itertools.repeat(None, 5)
    for _ in iter:
        yield
        if not predicate(): break

def buildBulkRequest(type, index, tracks):
    esactions = []
    track_count = 0

    for track in tracks:
        esactions.append({
            '_op_type':  type,
            '_index': index,
            '_type': 'trending',
            '_source': json.dumps(track)
        })
        track_count += 1

    return esactions

config = Config()
conf = config.load_config()
client_id = conf['soundcloud']['client_id']
schost = conf['soundcloud']['api_host']
eshost = conf['elasticsearch']['host']
esport = conf['elasticsearch']['port']

client = soundcloud.Client(client_id=client_id, host=schost)

# get the first 200 trending tracks
trending = client.get('/explore/Popular+Music', limit=200)

esactions = []
track_count = 0
esactions = buildBulkRequest('index', 'soundcloud-tracks-test4', trending.tracks)

# get more tracks, the iterator will repeat 3 times or until next_href is unset.
for _ in dowhile(lambda: has_more == True):
    trending = client.get(trending.next_href)
    actions = buildBulkRequest('index', 'soundcloud-tracks-test4', trending.tracks)
    esactions = esactions + actions
    has_more = True if 'next_href' in trending.keys() else False

es = Elasticsearch([{ 'host': eshost, 'port': esport }])
response = helpers.bulk(es, esactions, chunk_size=1000, stats_only=True)

print "%s tracks requested." % track_count
print "Elasticsearch response: %s documents indexed, %s errors." % (response[0], response[1])