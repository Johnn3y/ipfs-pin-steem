import argparse,ipfspinsteem.strings as s
from ipfspinsteem.ipfspinsteem2 import Steem,Parser,IPFS
import ipfshttpclient

parser = argparse.ArgumentParser(description='Extracts IPFS Hashes to Dtube/Dsound, creates an IPFS Object and pins it to an IPFS node.')
parser.add_argument('url', type=str, nargs='+',help='Dtube Video-Url. Example: account/permlink')
parser.add_argument('--api', dest='api', default='/ip4/127.0.0.1/tcp/5001/http',help='IPFS API IP. Default:/ip4/127.0.0.1/tcp/5001/http')
parser.add_argument('--exclude', dest='exclude', nargs='+',help='Exclude something. Example: videohash')
parser.add_argument('--object', dest='object',action='store_true',help='Will wrap all hashes to a single IPFS Object.')
parser.add_argument('--no-pin', dest='nopin',action='store_true',help='Will not pin anything to IPFS')
parser.add_argument('--quiet', dest='quiet',action='store_true',help='Will only print hash(es) and nothing else when successfully finnished.')
args=parser.parse_args()

def main():
	'''
	Connect to IPFS and Steem api.
	'''
	ipfs=IPFS(args.api)
	steem=Steem(steemd_nodes=None)
	'''
	Get user and permlinks from url argument.
	'''
	try:
		parser=Parser()
		info = parser.parseURL(urls=args.url)
	except ValueError:
		print("Invalid URL. Aborted")
		exit(0)
	'''
	Get IPFS hashes from Steem by content(user and permlink)
	'''
	try:
		hashes=steem.getHashesByContentList(info)
	except SyntaxError:
		print("SyntaxError. Probablly unavailable user and/or permlink. Aborted")
		exit(0)
	except KeyboardInterrupt:
		print("Interrupted by user")
	if hashes is None:
		print('No hashes found')
		exit(0)
	'''
	Remove invalid stuff
	'''
	opts={s.donotadd:args.exclude}
	hashes=Steem.removeInvalid(hashes,opts)
	'''
	Link all Hashes to a new IPFS Object or just add Hashes to list without creating object
	'''
	#print(ipfs.parseHash("QmbWPdc526RQxMVijVNQEyvz6s1Mh5hT3r4CZ4xhUh6xZk","QmbWPdc526RQxMVijVNQEyvz6s1Mh5hT3r4CZ4xhUh6xZk"))
	#objopts={s.donotadd:args.exclude}#Object creation options
	liste=[]
	for h in hashes:
		for e in h[s.permlinks]:
			for q in e:
				for p in q[s.links]:
					if args.quiet == False:
						print('extracted',h[s.user],'/',q[s.permlink],'/',p[s.Name],'/',p[s.Hash])
					if args.object == False:
						liste.append(p[s.Hash])
						#ipfs.pin(p[s.Hash])
						#print('pinned',p[s.Hash],'recursively')
	if args.object == True:
		try:
			obj=ipfs.createNewSingleObject(hashes),
		except KeyboardInterrupt:
			print('interrupted by user')
			exit(0)
		#obj=obj[0]
		liste.append(obj[0])
		if args.quiet == False:
			print('created object',obj[0])
	#obj=obj[0]

	#if args.quiet==False:

	'''
	Pin List "liste" to IPFS Node
	'''
	if args.nopin==False:
		try:
			ipfs.pin(liste)
			if args.quiet==False:
				for i in liste:
					print('pinned',i,'recursively')
			else:
				for i in liste:
					print(i)
		except ipfshttpclient.exceptions.DecodingError as e:
			print('pinning failed')
			print(e)
		except KeyboardInterrupt:
			print('Pinning Interrupted by user')
	elif args.object == True:
		if args.quiet== True:
			print(liste[0])
