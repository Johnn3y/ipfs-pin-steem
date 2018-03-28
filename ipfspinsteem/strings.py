import ast,ipfsapi,json
from steem.steemd import Steemd


Hash='Hash'
Name='Name'

user='user'
permlink='permlink'
#opts
donotadd='donotadd'

video='video'
audio='audio'

pepe='pepe'

#DTube
videohash='videohash'
video240hash='video240hash'
video480hash='video480hash'
video720hash='video720hash'
snaphash='snaphash'
spritehash='spritehash'
subtitleshash='subtitleshash'
subtitles='subtitles'

#DSound
sound='sound'
cover='cover'
peaks='peaks'

stroname='stroname'#Random string

jsonmd='json_metadata'

info='info'
obj='obj'

content='content'
files='files'

links='Links'
permlinks='permlinks'

available=[{stroname:content,obj:[
			{Name:videohash},
			{Name:video480hash},
			{Name:video720hash},
			{Name:video240hash},
			{Name:subtitleshash},
			{Name:subtitles},
			]
			},
			{stroname:info,obj:[
			{Name:snaphash},
			{Name:spritehash}]
			},
			{stroname:files,obj:[
			{Name:sound},
			{Name:cover},
			{Name:peaks}
			]},
			]
