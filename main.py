import sys
import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient
import tokens

reload(sys)
sys.setdefaultencoding('utf-8')

scope = 'user-library-read'

username = tokens.SP_USER

token = util.prompt_for_user_token(username, scope, tokens.SP_CLIENT_ID, tokens.SP_CLIENT_SECRET, tokens.SP_REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)
    sp_results = sp.current_user_saved_tracks(limit=50)
    sp_tracks = sp_results['items']
    while sp_results['next']:
        sp_results = sp.next(sp_results)
        sp_tracks.extend(sp_results['items'])
else:
    print "Can't get token for", username

print "Found {} tracks for user '{}' on Spotify".format(len(sp_tracks), username)

if sp_tracks:
    gmusic = Mobileclient()
    logged_in = gmusic.login(tokens.GMUSIC_USER, tokens.GMUSIC_PWD, Mobileclient.FROM_MAC_ADDRESS, 'en_US')
    if (logged_in):
        missing_tracks = []
        for sp_track in sp_tracks:
            sp_track = sp_track['track']
            name = sp_track['name']
            album = sp_track['album']['name']
            artist = sp_track['album']['artists'][0]['name']
            print " in: {} - {} - {}".format(name, artist, album)
            search_terms = [
                name + ' ' + artist + ' ' + album,
                name + ' ' + artist,
                name + ' ' + album,
                name
            ]
            gm_track = None
            for search_term in search_terms:
                gm_search = gmusic.search(name + ' ' + artist + ' ' + album, max_results = 100)
                gm_results = gm_search['song_hits']
                if (len(gm_results) > 0):
                    gm_track = gm_results[0]['track']
                    break
                else:
                    print "    No results for '{}'".format(search_term)
                    
            if gm_track:
                print "out: {} - {} - {}".format(gm_track['title'], gm_track['artist'], gm_track['album'])
                gmusic.add_store_track(gm_track['storeId'])
            else:
                print "out: No results found"
                missing_tracks.append(search_terms[0])

        print "Unable to add {} tracks.".format(len(missing_tracks))
        for track_info in missing_tracks:
            print track_info
    else:
        print("Could not log in to '{}'".format(tokens.GMUSIC_USER))
else:
    print('no tracks to transfer')