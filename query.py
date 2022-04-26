import json
import itertools

with open('MyData/StreamingHistory0.json', 'r', encoding='utf-8') as f:
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
    if days != 0:
        return '{}:{}:{}:{}'.format(days, hours, minutes, seconds)
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
    if rank_by != 'artistName' and rank_by != 'trackName' and rank_by != 'albumName':
        return 'Invalid input'
    if rank_by == 'albumName':
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


# ranks your favorite songs that are not currently in your library
def song_not_in_library(stream_log, library):
    song_dict = {}
    songs_in_library = []
    for song in library:
        songs_in_library.append(song['track'])
    for stream in stream_log:
        if stream['trackName'] not in songs_in_library and stream['trackName'] not in song_dict.keys():
            song_dict[stream['trackName']] = stream['msPlayed']
        elif stream['trackName'] not in songs_in_library:
            current_msPlayed = song_dict.get(stream['trackName'])
            current_msPlayed += stream['msPlayed']
            song_dict[stream['trackName']] = current_msPlayed
    song_dict = dict(sorted(song_dict.items(), key=lambda item: item[1], reverse=True))
    for song in song_dict.keys():
        song_dict[song] = convert_from_ms(song_dict.get(song))
    return song_dict


# most song listened to on repeat list
def on_repeat(stream_log, rank_by, library=None):
    repeat = {}
    for i in range(len(stream_log)):
        if stream_log[i]['msPlayed'] >= 30000 and i < len(stream_log) - 2:
            count = 1
            while stream_log[i][rank_by] == stream_log[i + 1][rank_by] \
                    and stream_log[i]['msPlayed'] >= 30000 and stream_log[i + 1]['msPlayed'] >= 30000:
                count += 1
                i += 1
            if stream_log[i][rank_by] not in repeat.keys():
                repeat[stream_log[i][rank_by]] = 1
            else:
                currentMax = repeat.get(stream_log[i][rank_by])
                if count > currentMax:
                    repeat.update({stream_log[i][rank_by]: count})
    repeat = dict(sorted(repeat.items(), key=lambda item: item[1], reverse=True))
    return repeat


def total_listening_time(stream_log):
    msPlayed = 0
    for stream in stream_log:
        msPlayed += stream['msPlayed']
    return convert_from_ms(msPlayed)


# Write json file that summarizes query data
user_data = {'Favorite Songs': dict(itertools.islice(rank_data(streaming_data, 'trackName').items(), 15)),
             'Favorite Albums': dict(
                 itertools.islice(rank_data(streaming_data, 'albumName', library_data).items(), 15)),
             'Favorite Artist': dict(itertools.islice(rank_data(streaming_data, 'artistName').items(), 15)),
             'Favorite Songs not in Library': dict(
                 itertools.islice(song_not_in_library(streaming_data, library_data).items(), 15)),
             'Favorite Artists played repeatedly': dict(
                 itertools.islice(on_repeat(streaming_data, 'artistName').items(), 15)),
             'Favorite Songs played repeatedly': dict(
                 itertools.islice(on_repeat(streaming_data, 'trackName').items(), 15))}

with open('Summary.json', 'w') as f:
    json.dump(user_data, f, indent=4)
