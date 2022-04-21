import json

with open('MyData/StreamingHistory1.json', 'r', encoding='utf-8') as f:
    streaming_data = json.load(f)
with open('MyData/YourLibrary.json', 'r', encoding='utf-8') as f:
    library_data = json.load(f)['tracks']


def convert_from_ms(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = seconds + milliseconds / 1000
    seconds = round(seconds)
    hours += (days * 24)
    return '{}:{}:{}'.format(hours, minutes, seconds)


# This function sorts artists by total listening time (in descending order)
def rank_data(stream_log, rank_by):
    if rank_by != 'artist' and rank_by != 'track':
        return 'Invalid input'
    if rank_by == 'artist':
        rank_by = 'artistName'
    if rank_by == 'track':
        rank_by = 'trackName'
    artist_dict = {}
    for stream in stream_log:
        if stream[rank_by] not in artist_dict.keys():
            artist_dict.update({stream[rank_by]: stream['msPlayed']})
        else:
            current_msPlayed = artist_dict.get(stream[rank_by])
            current_msPlayed += stream['msPlayed']
            artist_dict[stream[rank_by]] = current_msPlayed
    artist_dict = dict(sorted(artist_dict.items(), key=lambda item: item[1], reverse=True))
    for artists in artist_dict.keys():
        artist_dict[artists] = convert_from_ms(artist_dict.get(artists))
    return artist_dict


def rank_album(stream_log, library):
    album_dict = {}  # maps albums to total time played
    album_song = {}  # maps songs to albums
    for song in library:
        album_song.update({song['track']: song['album']})
    print(len(album_song))


rank_album(streaming_data, library_data)
# def rank_song(stream_log):
#     #
