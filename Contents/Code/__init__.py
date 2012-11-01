
VIDEO_PREFIX 	= 	"/video/tv2play"
ART 			= 	"art-default.jpg"
ICON 			= 	"icon-default.png"
NAME 			=	"TV 2 Play"
API_KEY			=	""	# REMEBER TO ADD THE API KEY WHILE TESTING AND ENCRYPTION/DECRYPTION IS NOT IMPLEMENTED
LOGIN_URL		=	"http://ajax.tv2.dk/login/user/login"
API_URL			= 	"http://r7.tv2.dk/api/3/"
API_SECURE_URL	=	"https://r7.tv2.dk/api/3/"
SECRET 			= 	""
def ValidatePrefs():
	if Prefs['usrName'] != "" and Prefs['pwd'] !="":
		pass
	else:
		Log.Debug(Login.message)
def Start():
	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	MediaContainer.art 		= R(ART)
	MediaContainer.title1 	= NAME
	DirectoryObject.thumb 	= R(ICON)
	DirectoryObject.art		= R(ART)
	ObjectContainer.art 	= R(ART)
	VideoClipObject.thumb	= R(ICON)
	VideoClipObject.art		= R(ART)
	InputDirectoryObject.thumb = R(ICON)
	InputDirectoryObject.art = R(ART)
	
def VideoMainMenu():
	dir = ObjectContainer(view_group = "List", title1 = NAME, title2 = 'Video')
  	machineip = HTTP.Request('http://plexapp.com/ip.php')
  	Log.Debug(machineip)
  	dir.add(PrefsObject(title = 'Indstillinger',
						thumb = R(ICON),
						art = R(ART)))
  	
  	### my little test to check auth and classes
  	json = Access()
  	Log.Debug(json.Profile())

	return dir



class Access:
	def __init__(self):
		pass
		
	def Profile(self):
		try:
			self.Login()
			json = JSON.ObjectFromURL(API_SECURE_URL + 
									"access/profile.json", 
									values = {'username':Prefs['usrName'], 
											'password':Prefs['pwd']})
		except:
			Log.Debug(Prefs['usrName'])
			Log.Debug(Prefs['pwd'])
			return None
			
		else:
			return json
	def End(self):
		HTTP.Request(API_KEY + "access/end.json")
	def Login(self):
		HTTP.Request(LOGIN_URL, values = {'username':Prefs['usrName'], 'password':Prefs['pwd']})

class Broadcasts:
	def __init__(self):
		pass
	def Query(self,ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									'broadcasts/ApplicationCode-%s.json' % ApplicationCode)
		except:
			return None
		else:
			return json
	def Get(self,id,ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									'broadcasts/get/%s/id-%s.json' % ("ApplicationCode-%s" % ApplicationCode,id))
		except:
			return None
		else:
			return json

class Categories:
	def __init__(self):
		pass
	def Query(self,order,parent=None,code=None):
		try:
			json = JSON.ObjectFromURL(API_URL + 'categories/order-%s' % order + 
									["" if parent is None else "/parent-%s" % parent] + 
									["" if code is None else "/code-%s" % code] + 
									".json"  )
			
		except:
			return None
		else:
			return json
	def Get(self,id,ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									"get/ApplicationCode-%s/id-%s.json" % (ApplicationCode,id))
		except:
			return None
		else:
			return json
		
class Epg:
	def __init__(self):
		pass
	def Current(self,ApplicationCode=API_KEY, max=None):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									"epg/ApplicationCode-%s" % ApplicationCode+ 
									["" if max is None else "/max-%s" % max] +".json")
		except:
			return None
		else:
			return json
	def Date(self,date,ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									"epg/date/ApplicationCode-%s/date-%s.json" % (ApplicationCode, date))
#			yyyy-mm-dd
		except:
			return None
		else:
			return json

class Events:
	def __init__(self):
		pass
	def Query(self,order,ApplicationCode = API_KEY, page = None, category = None, series = None, date = None):
				try:
					json = JSON.ObjectFromURL(API_URL + 
											"events/ApplicationCode-%s/order-%s" % (ApplicationCode, order) + 
											["" if page is None else "/order-%s" % page] + 
											["" if category is None else "/category-%s" % category]+
											["" if series is None else "/category-%s" % series ]+
											["" if date is None else "/date-%s" % date] + 
											".json")
				except:
					return None
				else:
					return json
	def Get(self, id, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "events/get/ApplicationCode-%s/id-%s.json" % (ApplicationCode, id))
		except:
			return None
		else:
			return json
	def Search(self, search, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL +
									"events/search.json?ApplicationCode=%s&query=%s" % (ApplicationCode, search))
		except:
			return None
		else:
			return json

class Placeholders:
	def __init__(self):
		pass
	def List(self, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "placeholders/ApplicationCode-%s.json" % ApplicationCode )
		except:
			return None
		else:
			return json	
	def Get(self, code, ApplicationCode = API_KEY, with_content = 0, content_limit = 0):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									"placeholders/get/ApplicationCode-%s/code-%s" % (ApplicationCode, code),
									["" if with_content <=0 else "/with_content-1" ],
									["" if content_limit<=0 else "/content_limit-%s" % content_limit ]+
									".json")
		except:
			return None
		else:
			return json
	def Content(self, code, ApplicationCode = API_KEY, limit = 0):
		try:
			json = JSON.ObjectFromURL(API_URL +
									"placeholders/content/ApplicationCode-%s/code-%s" % (ApplicationCode, code)+
									["" if limit <=0 else "/limit-%s" % limit]+
									".json")
		except:
			return None
		else:
			return json

class Play:
	def __init__(self):
		pass
	def Request(self, media_id, media_type, device_uid, ApplicationCode = API_KEY, device_name = None, device_type=None):
		try:
			Access().Login()
			json = JSON.ObjectFromURL(API_SECURE_URL +
									"play/request.json?ApplicationCode=%s&media_type=%s&media_id=%s&device_uid=%s" %(
											ApplicationCode, media_type, media_id, device_uid)+
									["" if device_name is None else "&device_name=%s" % device_name]+
									["" if device_type is None else "&device_type=%s" % device_type],
									values = {'username':Prefs['usrName'], 'password':Prefs['pwd']} )
		except:
			return None
		else:
			return json
		
	def Manifest(self, media_type, media_id, device_uid, ApplicationCode = API_KEY, device_name = None, device_type = None):
		try:
			Access().Login()
			json = JSON.ObjectFromURL(API_SECURE_URL + 
									"play/manifest.json?ApplicationCode=%s&media_type=%s&media_id=%s&device_uid=%s" % (
										ApplicationCode, media_type, media_id, device_uid)+
									["" if device_name is None else "&device_name=%s" % device_name ]+
									["" if device_type is None else "&device_type=" % device_type],
									values = {'username':Prefs['usrName'], 'password':Prefs['pwd']})
		except:
			return None
		else:
			return json
	def Playready(self, handle, media_type, media_id, expire, signature = SECRET):
		try:
			Access().Login()
			json = JSON.ObjectFromURL(API_SECURE_URL + "play/playready.json?handle=%s&media_type=%s&media_id=%s&keyid=%s&expire=%s&signature=%s" %(
															handle, media_type, media_id, expire, Hash.sha1(signature)	),
									values = {'username':Prefs['usrName'], 'password':Prefs['pwd']})
		except:
			return None
		else:
			return json
	def WMS_Protector(self, requestedUri, handle = None, userIp = Network.PublicAddress):
		try:
			json = JSON.ObjectFromURL(API_URL + "play/wmsprotector/?" +
									["" if handle is None else "handle=%s" % handle]+
									"userIp=%s" % userIp+
									"&requestedUrl=%s" % requestedUri)
		except:
			return None
		else:
			return json

class Programs:
	def __init__(self):
		pass
	def Query(self, ApplicationCode = API_KEY, order ='latest', direction= None, page = None, category = None, series = None):
		try:
			json = JSON.ObjectFromURL(API_URL + "/programs/ApplicationCode-%s/order-%s" % (
												ApplicationCode, order)+
									["" if direction is None else "/direction-%s" % direction]+
									["" if page is None else "/page-%s" % page]+
									["" if category is None else "/category-%s" % category]+
									["" if series is None else "/series-%s" % series]+
									".json")
		except:
			return None
		else:
			return json
	def Get(self, id, ApplicationCode = API_URL):
		try:
			json = JSON.ObjectFromURL(API_URL + "programs/get/ApplicationCode-%s/id-%s.json" %(
													ApplicationCode, id))
		except:
			return None
		else:
			return json
	def Search(self, query, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "programs/search.json?ApplicationCode=%s&query=%s" %(
													ApplicationCode, query))
		except:
			return None
		else:
			return json
	def Related(self, id, ApplicationCode = API_KEY):
		try:
			json= JSON.ObjectFromURL(API_URL + "programs/related/ApplicationCode-%s/id-%s.json" %(
												ApplicationCode, id))
		except:
			return None
		else:
			return json
 
class Search:
	def __init__(self):
		pass
	def Query(self, query, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "search/ApplicationCode-%s/query-%s.json" % (
													ApplicationCode, query))
		except:
			return None
		else:
			return json

class Series:
	def __init__(self):
		pass
	def Query(self, order, category = None):
		try:
			json = JSON.ObjectFromURL(API_URL + "series/order-%s" % order+
									["" if category is None else "/category-%s" % category]+
									".json"	)
		except:
			return None
		else:
			return json
	def Get(self,id):
		try:
			json = JSON.ObjectFromUrl(API_URL + "series/get/id-%s.json" % id)
		except:
			return None
		else:
			return json
	def Search(self,query):
		try:
			json = JSON.ObjectFromURL(API_URL + "series/search.json?query=%s" % query)
		except:
			return None
		else:
			return json
class Services:
	def __init__(self):
		pass
	def Settings(self,ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "service/ApplicationCode-%s.json" % ApplicationCode)
		except:
			return None
		else:
			return json
	def Notification(self, ApplicationCode = API_KEY, version = None):
		try:
			json = JSON.ObjectFromURL(API_URL + 
									"service/notification/ApplicationCode-%s"+
									["" if version is None else "/version-%s" % version]+
									".json"
									)
		except:
			return None
		else:
			return json
		
class Share:
	def __init__(self):
		pass
	def Sendmail(self, type, id, to_mail,From, body_hash, keyid, expire = 15, to = None, ApplicationCode = API_KEY):
		try:
			json = JSON.ObjectFromURL(API_URL + "share/mail.json?ApplicationCode=%s&type=%s&id=%s" % (
														ApplicationCode, type, id) +
									["" if to is None else "&to=%s" % to ]+
									"&to_mail=%s&from=%s&body_hash=%s&keyid=%s&expire=%s&signature=%s" %(
															to_mail, From, body_hash, expire, Hash.sha1(SECRET)))
		except:
			return None
		else:
			return json
		