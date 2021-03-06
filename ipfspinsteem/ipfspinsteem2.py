import ast,ipfshttpclient,json

try:
	from beem.comment import Comment as C
	from beem.account import Account as A
	from beem.exceptions import ContentDoesNotExistsException
except ImportError:
	try:
		from steem.steemd import Steemd as S	
	except ImportError:	
		pass
import requests
import random
import ipfspinsteem.strings as s

class Parser:
	'''
	Class for Parser
	'''		
	def parseURL(self,urls):
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
			url=url.replace('dlive.io/','')
			url=url.replace('steemit.com/','')
			url=url.replace('busy.org/','')
			url=url.replace('dsound.audio/','')
			url=url.replace('#!/','')
			url=url.replace('v/','')
			url=url.replace('c/','')
			url=url.replace('@','')
			try:
				a,b=url.split('/')
				liste.append({s.user:a,s.permlink:b})
			except ValueError:
				liste.append({s.user:url,s.permlink:None})

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
		try:
			self.steem = S(steemd_nodes)
		except NameError:
			pass
		#self.steem = C()
	
	def getContentJSON(self,account,permlink):#returns list
		liste=[]
		if permlink is None:
			comment =A(account).get_blog()
			for c in comment:
				liste.append({'json_metadata':c.json_metadata,'permlink':c.permlink})
		else:
			try:
				data=self.steem.get_content(account,permlink)
				data=data['json_metadata']
				obj=None
				try:
					obj=ast.literal_eval(data)
				except ValueError:
					obj=json.loads(data)
				liste.append({'json_metadata':obj,'permlink':permlink})

			except (NameError,AttributeError):
				try:
					liste.append({'json_metadata':C(authorperm='@'+account+'/'+permlink).json_metadata,'permlink':permlink})
				except:
					#response=urllib.request.urlopen("https://steemit.com/"+random.choice('abcdef')+"/@"+account+'/'+permlink)
					r=requests.get("https://steemit.com/"+random.choice('abcdef')+"/@"+account+'/'+permlink+'.json')
					data = r.json()
					data=data['post']
					data=data['json_metadata']
					liste.append({'json_metadata':data,'permlink':permlink})
		return liste
				
			
		
	def getHashesByContentList(self,liste):
		'''
		liste=[{'user':'usera','permlink':'sdlfjsdlk'},{'user':'userb','permlink':'asdfgfd'}] See parseURL()
		
		returns [{user:'username1',permlink:'prml1nk','Links':[{Name:snaphash,Hash:Hash1},{Name:videohash,Hash:Hash2},...]},...]
		
		returns None if no hashes were found
		'''


		j={}

		for l in liste:
			#identifier='@'+l[s.user]+'/'+l[s.permlink]
			#vidobj2= C(authorperm=identifier).json_metadata

			vidobj22= self.getContentJSON(l[s.user],l[s.permlink])
			for vidobj2 in vidobj22:
		
				pl=vidobj2[s.permlink]
				vidobj2=vidobj2['json_metadata']
				for jsonmdstr in s.available:	
					retlist=[]
					for lu in s.available[jsonmdstr]:
						for q in lu:
							#vidobj2=self.getContentJSON(l[s.user],l[s.permlink])
							try:
								if(vidobj2[q] is not None):#Implicit for DLive/Steepshot
									if(vidobj2[q][0]=='Q' and vidobj2[q][1]=='m' and len(vidobj2[q])==46):
										zz={}
										zz={s.Name:q,s.Hash:vidobj2[q]}
										retlist.append(zz)
							except KeyError:
								pass
							try:
								vidobj10=vidobj2[q]
								for hu in lu[q]:
									for t in hu:
										vidobj11=vidobj10[t]
										for lili in hu[t]:
											try:
												zz={}
												zz[s.Name]=lili
												zz[s.Hash]=vidobj11[lili]
												if zz[s.Hash] is not None:
													retlist.append(zz)
											except KeyError:
												pass
							except KeyError:
								pass
				
				try:
					j[l[s.user]].append({s.permlink:pl,s.links:retlist})
				except KeyError:
					j[l[s.user]]=[]
					j[l[s.user]].append({s.permlink:pl,s.links:retlist})
		ka=liste
		endl=[]
		for a,b in j.items():
			plist=[]
			for l in ka:
				if a==l[s.user]:
					plist.append(b)
			endl.append({s.user:a,s.permlinks:plist})
		return endl
		
		
	def removeInvalid(liste,opts):
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
	def __init__(self,api2):
		self.api=ipfshttpclient.connect(api2)
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
			res=self.api.object.patch.add_link(res[s.Hash],row[s.Name],row[s.Hash])

		return res[s.Hash]

		
	def pin(self,hashes):
		for h in hashes:
			self.api.pin.add(h)

	def pinList(self,liste):#Pins the list what Steem.getHashesByContentList returns
		for l in liste:
			for e in l[s.permlinks]:
				for p in e[s.links]:
					self.api.pin.add(p[s.Hash])
