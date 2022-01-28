import json
import requests
from crypto import addLengthPrefix, hashTx, sha512Half

from shamap import shamap
from shamap_node import node_type

URL = 'http://s2.ripple.com:51234'

class ledger:
    def __init__(self, header):
        self.header = header

    def verifyTransactions(self, transactions):
        s = shamap()
        print("COMPUTED HASHES")
        for tx in transactions:
            blob = addLengthPrefix(tx["tx_blob"]) + addLengthPrefix(tx["meta"])
            hash = hashTx(tx["tx_blob"])
            s.insert(hash, blob, node_type.TRANSACTION_METADATA)

        if s.hash() != self.header["transaction_hash"]:
            print(s.hash() + " does not equal tx  hash in ledger header " + self.header["account_hash"])
            raise Exception('mismatched hashes')

    def verifyState(self, state, diff):
        for change in diff:
            if change == "":
                state.erase(change["index"])
            else:
                state.insert(change["index"], change["data"], node_type.ACCOUNT_STATE)

        if state.hash() != self.header["account_hash"]:
            print(state.hash() + " does not equal state hash in ledger header " + self.header["account_hash"])
            raise Exception('mismatched hashes')

def getLedgerDiff(seq):
    params = [{"ledger_index": seq}]
    data = json.dumps({"method": "ledger", "params": params})
    r = requests.post(URL, data=data)
    resp = json.loads(r.text)
    return {}
 

def getLedger(seq):
    params = [{"ledger_index": seq}]
    data = json.dumps({"method": "ledger", "params": params})
    r = requests.post(URL, data=data)
    resp = json.loads(r.text)
    return ledger(resp["result"]["ledger"])

def getTxHashes(seq):
    params = [{"ledger_index": seq, "transactions": True}]
    data = json.dumps({"method": "ledger", "params": params})
    r = requests.post(URL, data=data)
    resp = json.loads(r.text)
    print(resp["result"]["ledger"]["transactions"])
    return resp["result"]["ledger"]["transactions"]


def getLedgerTransactions(seq):
    params = [{"ledger_index": seq, "transactions": True, "binary": True, "expand": True}]
    data = json.dumps({"method": "ledger", "params": params})
    r = requests.post(URL, data=data)
    resp = json.loads(r.text)
    return resp["result"]["ledger"]["transactions"]

def getLedgerState(seq, marker):
    params = [{"ledger_index": seq, "binary": True}]
    if marker != None:
        params[0]["marker"] = marker

    data = json.dumps({"method": "ledger_data", "params": params})
    r = requests.post(URL, data=data)
    resp = json.loads(r.text)
    state = resp["result"]["state"]
    
    newMarker = None
    try:
        newMarker = resp["result"]["marker"]
    except:
        pass

    return [state, newMarker]


def loadInitialLedger(seq):
    [ledger_state, marker] = getLedgerState(seq, None)
    state = ledger_state

    while marker != None:
        print("Marker: " + marker)
        [ledger_state, marker] = getLedgerState(seq, marker)
        state = state + ledger_state
    
    return state


            