import sys
import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient
import tokens
from

reload(sys)
sys.setdefaultencoding('utf-8')

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
else:
    print "Can't get token for", username

print "Found {} tracks for user '{}' on Spotify".format(len(tracks), username)

if tracks:
    gmusic = Mobileclient()
    logged_in = gmusic.login(tokens.GMUSIC_USER, tokens.GMUSIC_PWD, Mobileclient.FROM_MAC_ADDRESS, 'en_US')
    if (logged_in):
        for track in tracks:
            track = track['track']
            name = track['name']
            album = track['album']['name']
            artist = track['album']['artists'][0]['name']
            print " in: {} - {} - {}".format(name, artist, album)
            searchterms = [
                name + ' ' + artist + ' ' + album,
                name + ' ' + artist,
                name + ' ' + album
            ]
            results = gmusic.search(name + ' ' + artist + ' ' + album)
            result = results['song_hits'][0]['track']
            print "out: {} - {} - {}".format(result['title'], result['artist'], result['album'])
    else:
        print("Could not log in to '{}'".format(tokens.GMUSIC_USER))
else:
    print('no tracks to transfer')