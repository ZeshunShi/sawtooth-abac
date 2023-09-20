# sawtooth-abac
## Install
```
$ python3 setup.py install
```
## Usage
### 1. Start the processor
```
$ abac-tp-python -v --connect "the component bind string"
```
### 2. Start the listener
```
$ abac-listener "the component bind string"
```
### 3. Use functions provided by the client
#### Add a policy
```
$ abac add "policy filename" --user "username"
```
#### Delete a policy
```
$ abac delete "policy filename" --user "username"
```
#### Check a inquiry
```
$ abac check "inquiry filename" --user "username"
```
## Notice
### 1. You may meet error like: SyntaxError: future feature annotations is not defined.
Try to do the following two steps:
```
$ pip3 install marshmallow-annotations
$ pip3 install marshmallow~=3.2
```
