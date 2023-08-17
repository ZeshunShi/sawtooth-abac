# Start a test network using docker
## node1
### validator
sawtooth-validator --bind component:tcp://172.17.0.2:4004 --bind network:tcp://172.17.0.2:8800 --bind consensus:tcp://172.17.0.2:5050 --endpoint tcp://172.17.0.2:8800 --peers tcp://172.17.0.3:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
### settings-tp
settings-tp -v --connect tcp://172.17.0.2:4004
### consensus-engine
pbft-engine -vv --connect tcp://172.17.0.2:5050
### rest-api
sawtooth-rest-api -v --connect tcp://172.17.0.2:4004
### abac-tp
abac-tp-python -v --connect tcp://172.17.0.2:4004
## node2
### validator
sawtooth-validator --bind component:tcp://172.17.0.3:4004 --bind network:tcp://172.17.0.3:8800 --bind consensus:tcp://172.17.0.3:5050 --endpoint tcp://172.17.0.3:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.4:8800,tcp://172.17.0.5:8800
### settings-tp
settings-tp -v --connect tcp://172.17.0.3:4004
### consensus-engine
pbft-engine -vv --connect tcp://172.17.0.3:5050
### rest-api
sawtooth-rest-api -v --connect tcp://172.17.0.3:4004
### abac-tp
abac-tp-python -v --connect tcp://172.17.0.3:4004
## node3
### validator
sawtooth-validator --bind component:tcp://172.17.0.4:4004 --bind network:tcp://172.17.0.4:8800 --bind consensus:tcp://172.17.0.4:5050 --endpoint tcp://172.17.0.4:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.5:8800
### settings-tp
settings-tp -v --connect tcp://172.17.0.4:4004
### consensus-engine
pbft-engine -vv --connect tcp://172.17.0.4:5050
### rest-api
sawtooth-rest-api -v --connect tcp://172.17.0.4:4004
### abac-tp
abac-tp-python -v --connect tcp://172.17.0.4:4004
## node4
### validator
sawtooth-validator --bind component:tcp://172.17.0.5:4004 --bind network:tcp://172.17.0.5:8800 --bind consensus:tcp://172.17.0.5:5050 --endpoint tcp://172.17.0.5:8800 --peers tcp://172.17.0.2:8800,tcp://172.17.0.3:8800,tcp://172.17.0.4:8800
### settings-tp
settings-tp -v --connect tcp://172.17.0.5:4004
### consensus-engine
pbft-engine -vv --connect tcp://172.17.0.5:5050
### rest-api
sawtooth-rest-api -v --connect tcp://172.17.0.5:4004
### abac-tp
abac-tp-python -v --connect tcp://172.17.0.5:4004

