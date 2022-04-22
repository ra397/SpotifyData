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


# This function sorts albums in descending order, album 'None' is all the songs not present in the
# libray grouped together. Under the assumption the listening time for songs in that category is low, the data is
# still meaningful.
def rank_album(stream_log, library):
    album_dict = {}  # maps albums to total time played
    song_album = {}  # maps songs to albums
    for song in library:
        song_album.update({song['track']: song['album']})
    for stream in stream_log:
        if song_album.get(stream['trackName']) not in album_dict.keys():
            album_dict.update({song_album.get(stream['trackName']): stream['msPlayed']})
        else:
            current_msPlayed = album_dict.get(song_album.get(stream['trackName']))
            current_msPlayed += stream['msPlayed']
            album_dict[song_album.get(stream['trackName'])] = current_msPlayed
    album_dict = dict(sorted(album_dict.items(), key=lambda item: item[1], reverse=True))
    for album in album_dict.keys():
        album_dict[album] = convert_from_ms(album_dict.get(album))
    return album_dict


# This function sorts artists/tracks by total listening time (in descending order)
def rank_data(stream_log, rank_by, library=None):
    if rank_by != 'artist' and rank_by != 'track' and rank_by != 'album':
        return 'Invalid input'
    if rank_by == 'artist':
        rank_by = 'artistName'
    if rank_by == 'track':
        rank_by = 'trackName'
    if rank_by == 'album':
        return rank_album(stream_log, library)
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


# rank songs not in library
def song_not_in_library(stream_log, library):
    songs_in_library = []
    for song in library:
        songs_in_library.append(song['track'])
    print(songs_in_library)


song_not_in_library(streaming_data, library_data)