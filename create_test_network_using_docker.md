# Start a test network using docker

## Create containers
```
docker run -it --hostname=node1 --name=node1 sawtooth-node:v3 /bin/bash
docker run -it --hostname=node2 --name=node2 sawtooth-node:v3 /bin/bash
docker run -it --hostname=node3 --name=node3 sawtooth-node:v3 /bin/bash
docker run -it --hostname=node4 --name=node4 sawtooth-node:v3 /bin/bash
```

## Generate keys
```
sawtooth keygen node1
sawadm keygen
sawtooth keygen node2
sawadm keygen
sawtooth keygen node3
sawadm keygen
sawtooth keygen node4
sawadm keygen
```

## Generate the genesis block
```
sawset genesis --key $HOME/.sawtooth/keys/node1.priv -o config-genesis.batch
cat /etc/sawtooth/keys/validator.pub
sawset proposal create --key $HOME/.sawtooth/keys/node1.priv -o config-consensus.batch sawtooth.consensus.algorithm.name=pbft sawtooth.consensus.algorithm.version=1.0 sawtooth.consensus.pbft.members='["","","",""]' 
sawadm genesis config-genesis.batch config-consensus.batch
```

## Edit validator.toml
```
nano /etc/sawtooth/validator.toml
```
### node1
```
peers = ["tcp://172.17.0.3:8800", "tcp://172.17.0.4:8800", "tcp://172.17.0.5:8800"]
```
### node2
```
peers = ["tcp://172.17.0.2:8800", "tcp://172.17.0.4:8800", "tcp://172.17.0.5:8800"]
```
### node3
```
peers = ["tcp://172.17.0.2:8800", "tcp://172.17.0.3:8800", "tcp://172.17.0.5:8800"]
```
### node4
```
peers = ["tcp://172.17.0.2:8800", "tcp://172.17.0.3:8800", "tcp://172.17.0.4:8800"]
```

## node1
### enter container
docker exec -it node1 /bin/bash
### validator
```
sawtooth-validator --bind component:tcp://172.17.0.2:4004 --bind network:tcp://172.17.0.2:8800 --bind consensus:tcp://172.17.0.2:5050 --endpoint tcp://172.17.0.2:8800 --peers tcp://172.17.0.3:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
settings-tp -v --connect tcp://172.17.0.2:4004
```
### consensus
```
pbft-engine -vv --connect tcp://172.17.0.2:5050
```
### rest-api
```
sawtooth-rest-api -v --connect tcp://172.17.0.2:4004
```
### abac-tp
```
abac-tp-python -v --connect tcp://172.17.0.2:4004
```
### abac-listener
```
abac-listener tcp://172.17.0.2:4004
```

## node2
### enter container
docker exec -it node2 /bin/bash
### validator
```
sawtooth-validator --bind component:tcp://172.17.0.3:4004 --bind network:tcp://172.17.0.3:8800 --bind consensus:tcp://172.17.0.3:5050 --endpoint tcp://172.17.0.3:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
settings-tp -v --connect tcp://172.17.0.3:4004
```
### consensus
```
pbft-engine -vv --connect tcp://172.17.0.3:5050
```
### rest-api
```
sawtooth-rest-api -v --connect tcp://172.17.0.3:4004
```
### abac-tp
```
abac-tp-python -v --connect tcp://172.17.0.3:4004
```
### abac-listener
```
abac-listener tcp://172.17.0.3:4004
```

## node3
### enter container
docker exec -it node3 /bin/bash
### validator
```
sawtooth-validator --bind component:tcp://172.17.0.4:4004 --bind network:tcp://172.17.0.4:8800 --bind consensus:tcp://172.17.0.4:5050 --endpoint tcp://172.17.0.4:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.5:8800
```
### settings-tp
```
settings-tp -v --connect tcp://172.17.0.4:4004
```
### consensus
```
pbft-engine -vv --connect tcp://172.17.0.4:5050
```
### rest-api
```
sawtooth-rest-api -v --connect tcp://172.17.0.4:4004
```
### abac-tp
```
abac-tp-python -v --connect tcp://172.17.0.4:4004
```
### abac-listener
```
abac-listener tcp://172.17.0.4:4004
```

## node4
### enter container
docker exec -it node4 /bin/bash
### validator
```
sawtooth-validator --bind component:tcp://172.17.0.5:4004 --bind network:tcp://172.17.0.5:8800 --bind consensus:tcp://172.17.0.5:5050 --endpoint tcp://172.17.0.5:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.4:8800
```
### settings-tp
```
settings-tp -v --connect tcp://172.17.0.5:4004
```
### consensus
```
pbft-engine -vv --connect tcp://172.17.0.5:5050
```
### rest-api
```
sawtooth-rest-api -v --connect tcp://172.17.0.5:4004
```
### abac-tp
```
abac-tp-python -v --connect tcp://172.17.0.5:4004
```
### abac-listener
```
abac-listener tcp://172.17.0.5:4004
```

## Add new node
### Create keys
```
sawtooth keygen node*
sawadm keygen
```
### Edit configuration
```
nano /etc/sawtooth/validator.toml
peers = [urls of all other nodes in the network]
```
### Start the node
```
// like other nodes
```
### Turn to the genesis node
```
sawset proposal create --key $HOME/.sawtooth/keys/node1.priv sawtooth.consensus.pbft.members='[previous-list,"new-node-validator-pubkey"]'
```
