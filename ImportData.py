import json

with open('MyData/StreamingHistory1.json', 'r', encoding='utf-8') as f:
    streaming_data = json.load(f)


def convert_time(ms):
    seconds = (ms / 1000) % 60
    seconds = int(seconds)
    minutes = (ms / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (ms / (1000 * 60 * 60)) % 24
    return "%d:%d:%d" % (hours, minutes, seconds)


# This function sorts artists by total listening time (in descending order)
def rank_artist(stream_log):
    artist_dict = {}
    for stream in stream_log:
        if stream['artistName'] not in artist_dict.keys():
            tmp = {stream['artistName']: stream['msPlayed']}
            artist_dict.update(tmp)
        else:
            current_msPlayed = artist_dict.get(stream['artistName'])
            current_msPlayed += stream['msPlayed']
            artist_dict[stream['artistName']] = current_msPlayed
    artist_dict = dict(sorted(artist_dict.items(), key=lambda item: item[1], reverse=True))
    for artists in artist_dict.keys():
        artist_dict[artists] = convert_time(artist_dict.get(artists))
    return artist_dict


print(rank_artist(streaming_data))

#
# def rank_album(stream_log):
#     #
#
# def rank_song(stream_log):
#     #
