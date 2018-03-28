import ast,ipfsapi,json
from steem.steemd import Steemd
import ipfspinsteem.strings as s
import io

#strhash='Hash'

#struser='user'
#strp='permlink'

class Parser:
	'''
	Class for Parser
	'''		
	def parseURL(urls):
		'''
		urls:"[@username/permlink,d.tube/uname2/eiohfs,...]"
		returns [{'user':'usr11','permlink':'fser909e'},...]
		
		'''
		#TODO recognize duplications
		liste=[]
		for url in urls:
			url=url.replace('https://','')
			url=url.replace('http://','')
			url=url.replace('d.tube/','')
			url=url.replace('d.tube/','')
			url=url.replace('dsound.audio/','')
			url=url.replace('#!/','')
			url=url.replace('v/','')
			url=url.replace('@','')
			
			a,b=url.split('/')
			liste.append({s.user:a,s.permlink:b})
		return liste


class Steem:
	'''
	Class for Steem-related stuff
	'''
	def __init__(self,steemd_nodes):
		if steemd_nodes is None:
			steemd_nodes = [
    	"https://api.steemit.com",
	]
		self.steem = Steemd(nodes=steemd_nodes)	
		
	def getHashesByContentList(self,liste):
		'''
		liste=[{'user':'usera','permlink':'sdlfjsdlk'},{'user':'userb','permlink':'asdfgfd'}] See parseURL()
		
		returns [{user:'username1',permlink:'prml1nk','Links':[{Name:snaphash,Hash:Hash1},{Name:videohash,Hash:Hash2},...]},...]
		
		returns None if no hashes were found
		'''

		h=[]
		j={}
		ah=[]
		for l in liste:
			vidobj3= self.steem.get_content(l[s.user],l[s.permlink])
			try:
				vidobj2=vidobj3[s.jsonmd]
			except TypeError:
				vidobj2=vidobj3[s.jsonmd]

			try:
				vidobj2=ast.literal_eval(vidobj2)
			except ValueError:
				vidobj2=json.loads(vidobj2)
			try:#for dsound, dirty solution
				vidobj=vidobj2[s.video]
			except KeyError:
				try:
					vidobj=vidobj2[s.audio]
				except KeyError:
					return None

			retlist=[]
			for e in s.available:
				try:
					nobj=vidobj[e[s.stroname]]
					for a in e[s.obj]:
						zz={}
						zz[s.Name]=a[s.Name]
						zz[s.Hash]=nobj[a[s.Name]]
						if zz[s.Hash] is not None:
							retlist.append(zz)

				except KeyError:
					pass
			h.append({s.user:l[s.user],s.permlink:l[s.permlink],s.links:retlist})
			
			try:
				j[l[s.user]].append({s.permlink:l[s.permlink],s.links:retlist})
			except KeyError:
				j[l[s.user]]=[]
				j[l[s.user]].append({s.permlink:l[s.permlink],s.links:retlist})
		ka=liste
		endl=[]
		for a,b in j.items():
			plist=[]
			for l in ka:
				if a==l[s.user]:
					plist.append(b)
			endl.append({s.user:a,s.permlinks:plist})
		return endl
		
		
	def removeInvalid(liste,opts):#some redundat code
		for users in liste:			
			for permlinks in users[s.permlinks]:
				for element in permlinks:
					for ha in element[s.links]:
						if ha[s.Hash]=='':
							element[s.links].remove(ha)
						elif ha[s.Hash] is None:
							element[s.links].remove(ha)
						if opts[s.donotadd] is not None:
							for t in opts[s.donotadd]:
								try:		
									if ha[s.Name]==t:
										element[s.links].remove(ha)	
								except KeyError:
									pass
								except TypeError:
									pass
					if opts[s.donotadd] is not None:
						for t in opts[s.donotadd]:
							for ha in element[s.links]:
								try:
									if ha[s.Name]==t:
										element[s.links].remove(ha)
								except KeyError:
									pass
								except TypeError:
									pass
					
							
		return liste	
				
class IPFS:
	'''
	Class for IPFS related stuff.
	'''
	def __init__(self,api2,port):
		self.api=ipfsapi.connect(api2,port)
		#self.aipfs=i(api2,port)

	def createNewSingleObject(self,liste):
		'''
		liste: result of getHashesByContentList()
		creates something like this:
		[[user1->[permlink1->[{Name1,Hash1},{Name2,Hash2}],...],...],...]	
		
		
		
		
		INFO recomended to run liste=Steem.removeInvalid(liste,opts=None) before
		'''

		userhashes=[]
		for users in liste:			
			phashes=[]
			for permlinks in users[s.permlinks]:
				for element in permlinks:		
					phashes.append({s.Name:element[s.permlink],s.Hash:self.createNewObject(element[s.links],targethash=None)})
			
			userhashes.append({s.Name:users[s.user],s.Hash:self.createNewObject(phashes,targethash=None)})
		return self.createNewObject(userhashes,targethash=None)

	def createNewObject(self,hashlist,targethash):
		'''
		returns Hash of new IPFS object created with given hashlist:
		
		hashlist=[{Hash:"Qmhash1",Name:"Name1"},{Hash:"Qmhash2",Name:"Name2"}]
		targethash: hash to link to.Default:'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'(unixfs-dir)
		
		'''		
		if targethash is None:
			targethash='QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'#Ugly
		res={s.Hash:targethash}
		for row in hashlist:
			res=self.api.object_patch_add_link(res[s.Hash],row[s.Name],row[s.Hash])

		return res[s.Hash]

		
	def pin(self,hashes):
		for h in hashes:
			self.api.pin_add(h)

	def pinList(self,liste):#Pins the list what Steem.getHashesByContentList returns
		for l in liste:
			for e in l[s.permlinks]:
				for p in e[s.links]:
					self.api.pin_add(p[s.Hash])

