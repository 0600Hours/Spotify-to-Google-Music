import sys
import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient
import tokens

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
        
    else:
        print("Could not log in to '{}'".format(tokens.GMUSIC_USER))
else:
    print('no tracks to transfer')