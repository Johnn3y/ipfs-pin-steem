[![Build Status](https://travis-ci.org/Johnn3y/ipfs-pin-steem.svg?branch=steem)](https://travis-ci.org/Johnn3y/ipfs-pin-steem)


# ipfs-pin-steem

> A tool for pinning Steem content from Dtube,Dlive,Dsound,Steepshot to your IPFS node.


## Requirements
* python3.6
* ipfsapi
* steem

## Installation
Install with pip
```
pip install https://github.com/Johnn3y/ipfs-pin-steem/archive/steem.zip
```

or build from source
```
git clone https://github.com/Johnn3y/ipfs-pin-steem
cd ipfs-pin-steem
git checkout steem
python setup.py install
```

## Usage
cli-Knowledge required. Run `ipfs-pin-steem --help` for more details. 

`url` can look e.g. like `https://d.tube/v/user/permlink` or just `user/permlink`.


To simply pin a post run:

```
ipfs-pin-steem url
```
To pin multiple posts:

```
ipfs-pin-steem url1 url2 url3
```

To wrap all hashes to a single ipfs object, run:

```
ipfs-pin-steem url --object
```

If you don't want to pin e.g. snaphash and spritehash, simply run:

```
ipfs-pin-steem url --exclude snaphash spritehash
```

If you don't want to pin anything and just create the object, run:

```
ipfs-pin-steem url --object --no-pin
```


If your IPFS Node is not on your local machine or you changed the port, you can simply run:

```
ipfs-pin-steem url --api 127.0.0.1 --port 5001
```
