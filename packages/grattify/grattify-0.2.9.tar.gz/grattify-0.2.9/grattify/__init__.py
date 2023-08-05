from __future__ import unicode_literals
from bs4 import BeautifulSoup
import sys, requests, youtube_dl, os, traceback, spotipy, urllib,pprint,re
import spotipy.util as util
from mutagen.easyid3 import EasyID3


SPOTIPY_CLIENT_ID = "6ddf2f4253a847c5bac62b17cd735e66"
SPOTIPY_CLIENT_SECRET = "5b54de875ad349f3bb1bbecd5832f276"
SPOTIPY_REDIRECT_URI = "http://tabatest://callback"

def downloadSong(title,artist,attempt,saveDir,ytlink=None,trackNum=""):
	savePath = makeSavepath(title,artist,saveDir)
	print artist,"---",title
	options = {
		'format':'bestaudio/best',
		'extractaudio':True,
		'audioformat':'mp3',
		'outtmpl':'%(id)s.%(ext)s',		#name the file the ID of the video
		'noplaylist':True,
		'nocheckcertificate':True,
		'proxy':"",
		'addmetadata':True,
		'postprocessors': [{
        	'key': 'FFmpegExtractAudio',
        	'preferredcodec': 'mp3',
        	'preferredquality': '192',
    	}]
	}
	ydl = youtube_dl.YoutubeDL(options)
	#reformat
	if (ytlink is None):
		songURL = findNthBestLink(attempt,artist.lower(),title.lower())['link']
		if not songURL:
			return False
	else:
		songURL = ytlink

	try: #video already being downloaded
		os.stat(savePath)
		print "%s already downloaded, continuing..." % savePath
	except OSError: #download video
		try:
			result = ydl.extract_info(songURL, download=True)
			print savePath
			os.rename(result['id'] +'.mp3', savePath)
			metatag = EasyID3(savePath)
			metatag['title'] = title
			metatag['artist'] = artist
			metatag.RegisterTextKey("track", "TRCK")
			metatag['track'] = trackNum
			metatag.save()
			print "Downloaded and converted %s successfully!" % savePath
		except Exception as e:
			print "Can't download audio! %s\n" % traceback.format_exc()
			return False
	return True

def makeSavepath(title,artist,saveDir):
	title = title.replace('/',' ')
	artist = artist.replace('/',' ')
	return os.path.join(saveDir,"%s - %s.mp3" % (artist, title))

def getYoutubeSearchResults(query):
	results= []
	try:
		r = requests.post("https://www.youtube.com/results?search_query="+query)
		print "https://www.youtube.com/results?search_query="+query
	except Exception as e:
		print "Can't download audio! %s -- %s\n" % (artist,title)
		return False
	soup = BeautifulSoup(r.content,'html.parser')
	for div in soup.findAll("div"):
		if 'class' in div.attrs and "yt-lockup-content" in div['class']:
			for a in div.findAll('a'):
				if "watch" in a['href']:
					try:
						link = a['href']
						title = a['title']
						duration  = a.parent.find('span').text.split(' ')[-1][:-1]
						for li in div:
							if "views" in li.text:
								viewCount = li.text.split(' ')[-2][3:]
								results.append({"viewCount":int(viewCount.replace(',','')),
												"link":"https://www.youtube.com"+link,
												"title":title.lower(),
												"duration":duration})
					except:
						continue
	return results

def findNthBestLink(n,artist,title):
	searchString = artist + ' ' + title
	searchString = re.sub('[^0-9a-zA-Z ]+', '', searchString.lower()).replace(' ','+')
	results = getYoutubeSearchResults(searchString)
	if results == False or len(results) == 0:
		#try again with unformatted input
		results = getYoutubeSearchResults(artist+'+'+title)
		if results == False or len(results) == 0:
			return False

	badKeywords = ["video","album","live","cover","remix","instrumental","acoustic","karaoke"]
	goodKeywords = ["audio","lyric"]
	
	badKeywords = filter(lambda bk: searchString.find(bk) < 0,badKeywords)

	scoreIndex = []
	for i,ytR in enumerate(results):
		matchScore = i
		for bk in badKeywords:
			if ytR['title'].find(bk) != -1:
				matchScore += 1.1
		for gk in goodKeywords:
			if ytR['title'].find(gk) != -1:
				matchScore -= 1.1
		if ytR['title'].find("".join(artist.split("the "))) != -1:
			matchScore -= 5
		if ytR['title'].find(title) != -1:
			matchScore -= 3
		scoreIndex.append((i,matchScore))
	bestToWorst = sorted(scoreIndex,key=lambda score: score[1])
	nthBest = bestToWorst[n-1][0]
	#printResults(ytResults,bestToWorst)
	return results[nthBest]
 		
def printResults(ytResults,bestToWorst):
	print "UNSORTED::"
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(ytResults[:7])
	print "\n\n\n"
	print "BY ALGORITHM::"
	smartList = map(lambda score: (ytResults[score[0]],score[1]),bestToWorst)
	pp.pprint(smartList[:7])

def parsePandoraLikes(pandoraLikesPage):
	pFile = urllib.urlopen(pandoraLikesPage).read()
	soup = BeautifulSoup(pFile,'html.parser')
	songs = []
	for div in soup.findAll('div',id=lambda x: x and x.startswith('tracklike')):
		info = div.findAll('a')
		songs.append((info[0].text,info[1].text))
	return songs

def getTopN(artist,n):
	try:
		r = requests.get("http://www.last.fm/music/"+artist.replace(' ','+')+"/+tracks")
		soup = BeautifulSoup(r.content,'html.parser')
		tds = soup.findAll("td",{"class":"chartlist-name"})
		songs = []
		for i in range(n):
			song = tds[i].find("a").text
			songs.append(song)
		return songs
	except Exception as e:
		print "SEARCH ERROR: Couldnt find top "+str(n)+" songs by "+artist+". Check that the artist is spelled correctly."
		return False

def getAlbum(artist,album):
	try:
		r = requests.get("http://www.last.fm/music/"+artist.replace(' ','+')+"/"+album.replace(' ','+'))
		soup = BeautifulSoup(r.content,'html.parser')
		tds = soup.findAll("td",{"class":"chartlist-name"})
		return map((lambda td: td.find("a").text),tds)
	except Exception as e:
		print "SEARCH ERROR: Couldnt find album "+album+" by "+artist+". Check that the album name is spelled correctly."
		return False

def getSpotifyPlaylists(username,reqPlaylists):
	scope = "playlist-read-private user-library-read"
	token = spotipy.util.prompt_for_user_token(username, scope,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI)
	playlists = []
	if token:
	    sp = spotipy.Spotify(auth=token)
	    user = sp.current_user()['id']
	    spPlaylists = sp.user_playlists(user)
	    for playlist in spPlaylists['items']:
	    	if (len(reqPlaylists) == 0 or playlist['name'].lower() in [pl.lower() for pl in reqPlaylists]):
				results = sp.user_playlist(user, playlist['id'],
				    fields="tracks,next")
				songs = map((lambda item:item['track']['name']),results['tracks']['items'])
				artists = map((lambda item:item['track']['artists'][0]['name']),results['tracks']['items'])
				tracks = zip(artists,songs)
				
				playlists.append({'name':playlist['name'],'tracks':tracks})
	else:
	    print "Can't get token for", username
	return playlists

def compare(file1,file2):
	lines1 = file(file1).readlines()
	lines2 = file(file2).readlines()
	c1 = []
	for i,l in enumerate(lines1):
		if l[:4]=="1st:":
			c1.append(lines1[i+1] + ":::" + l[4:])
	c2 = []
	for i,l in enumerate(lines2):
		if l[:4]=="1st:":
			c2.append(lines2[i+1] + ":::" + l[4:])

	misMatches = filter((lambda (l1,l2): l1 != l2),zip(c1,c2))
	changeLog = file("changeLog.txt","w+")
	for mPair in misMatches:
		m = mPair[0]
		artist = m[m.find("---")+4:m.find("\n:::")]
		song = m[:m.find("---")]
		changeLog.write(artist + "," + song + m + '\n')
	return misMatches


