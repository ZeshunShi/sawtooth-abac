# Start a test network using docker

## Generate keys
```
$ sawtooth keygen node1
$ sawadm keygen
$ sawtooth keygen node2
$ sawadm keygen
$ sawtooth keygen node3
$ sawadm keygen
$ sawtooth keygen node4
$ sawadm keygen
```

## Generate the genesis block
```
$ sawset genesis --key $HOME/.sawtooth/keys/node1.priv -o config-genesis.batch
$ cat /etc/sawtooth/keys/validator.pub
$ sawset proposal create --key $HOME/.sawtooth/keys/node1.priv -o config-consensus.batch sawtooth.consensus.algorithm.name=pbft sawtooth.consensus.algorithm.version=1.0 sawtooth.consensus.pbft.members='["","","",""]' 
$ sawadm genesis config-genesis.batch config-consensus.batch
```

## Edit validator.toml
```
nano /etc/sawtooth/validator.toml
```
### node1
```
peers = ["tcp://172.17.0.3", "tcp://172.17.0.4", "tcp://172.17.0.5"]
```
### node2
```
peers = ["tcp://172.17.0.2", "tcp://172.17.0.4", "tcp://172.17.0.5"]
```
### node3
```
peers = ["tcp://172.17.0.2", "tcp://172.17.0.3", "tcp://172.17.0.5"]
```
### node4
```
peers = ["tcp://172.17.0.2", "tcp://172.17.0.3", "tcp://172.17.0.4"]
```

## node1
### validator
```
$ sawtooth-validator --bind component:tcp://172.17.0.2:4004 --bind network:tcp://172.17.0.2:8800 --bind consensus:tcp://172.17.0.2:5050 --endpoint tcp://172.17.0.2:8800 --peers tcp://172.17.0.3:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
$ settings-tp -v --connect tcp://172.17.0.2:4004
```
### consensus
```
$ pbft-engine -vv --connect tcp://172.17.0.2:5050
```
### rest-api
```
$ sawtooth-rest-api -v --connect tcp://172.17.0.2:4004
```
### abac-tp
```
$ abac-tp-python -v --connect tcp://172.17.0.2:4004
```
### abac-listener
```
$ abac-listener tcp://172.17.0.2:4004
```

## node2
### validator
```
$ sawtooth-validator --bind component:tcp://172.17.0.3:4004 --bind network:tcp://172.17.0.3:8800 --bind consensus:tcp://172.17.0.3:5050 --endpoint tcp://172.17.0.3:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
$ settings-tp -v --connect tcp://172.17.0.3:4004
```
### consensus
```
$ pbft-engine -vv --connect tcp://172.17.0.3:5050
```
### rest-api
```
$ sawtooth-rest-api -v --connect tcp://172.17.0.3:4004
```
### abac-tp
```
$ abac-tp-python -v --connect tcp://172.17.0.3:4004
```
### abac-listener
```
$ abac-listener tcp://172.17.0.3:4004
```

## node3
### validator
```
$ sawtooth-validator --bind component:tcp://172.17.0.4:4004 --bind network:tcp://172.17.0.4:8800 --bind consensus:tcp://172.17.0.4:5050 --endpoint tcp://172.17.0.4:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
$ settings-tp -v --connect tcp://172.17.0.4:4004
```
### consensus
```
$ pbft-engine -vv --connect tcp://172.17.0.4:5050
```
### rest-api
```
$ sawtooth-rest-api -v --connect tcp://172.17.0.4:4004
```
### abac-tp
```
$ abac-tp-python -v --connect tcp://172.17.0.4:4004
```
### abac-listener
```
$ abac-listener tcp://172.17.0.4:4004
```

## node4
### validator
```
$ sawtooth-validator --bind component:tcp://172.17.0.5:4004 --bind network:tcp://172.17.0.5:8800 --bind consensus:tcp://172.17.0.5:5050 --endpoint tcp://172.17.0.5:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.4:8800
```
### settings-tp
```
$ settings-tp -v --connect tcp://172.17.0.5:4004
```
### consensus
```
$ pbft-engine -vv --connect tcp://172.17.0.5:5050
```
### rest-api
```
$ sawtooth-rest-api -v --connect tcp://172.17.0.5:4004
```
### abac-tp
```
$ abac-tp-python -v --connect tcp://172.17.0.5:4004
```
### abac-listener
```
$ abac-listener tcp://172.17.0.5:4004
```
