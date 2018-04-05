[![Build Status](https://travis-ci.org/Johnn3y/ipfs-pin-steem.svg?branch=master)](https://travis-ci.org/Johnn3y/ipfs-pin-steem)


# ipfs-pin-steem - A tool for pinning Dtube/Dsound content to your IPFS node


## Dependencies
ipfsapi
steem

## Installation
Install with pip
```
pip install ipfs-pin-steem
```

or build from source
```
git clone https://github.com/Johnn3y/ipfs-pin-steem
cd ipfs-pin-steem
python setup.py install
```

## Usage
cli-Knowledge required. Run "ipfs-pin-steem --help" for more details. To simply pin a post run:

```
ipfs-pin-steem d.tube/v/user/permlink
```

to wrap all hashes to a single ipfs object, run:

```
ipfs-pin-steem d.tube/v/user/permlink --object
```
If you don't want to pin e.g snaphash and spritehash, simply run:

```
ipfs-pin-steem d.tube/v/user/permlink --exclude snaphash spritehash
```

If you don't want to pin anything and just create the object, run:

```
ipfs-pin-steem d.tube/v/user/permlink --object --no-pin
```


If your IPFS Node is not on your local Machine or you changed the port, you can simply run:

```
ipfs-pin-steem d.tube/v/user/permlink --api 127.0.0.1 --port 5001
```
Run "ipfs-pin-steem --help" for more details.  s. 
