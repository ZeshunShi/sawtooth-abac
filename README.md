# sawtooth-abac

## Install
python3 setup.py install

## Usage
### 1. Start the processor
abac-tp-python -v --connect "the component bind string"
### 2. Start the listener
abac-listener "the component bind string"
### 3. Use functions provided by the client
#### Add a policy
abac add "policy filename" --user "username"
#### Delete a policy
abac delete "policy filename" --user "username"
#### Check a inquiry
abac check "inquiry filename" --user "username"
