from crypto import addLengthPrefix
from download_ledger import getLedger, getLedgerDiff, getLedgerState, getLedgerTransactions, getTxHashes, loadInitialLedger
from leaf_node import leaf_node
from shamap import shamap
from shamap_node import node_type

s = shamap()
seq = 3253223
state = loadInitialLedger(seq)
initialLedger = getLedger(seq)
initialLedger.verifyTransactions(getLedgerTransactions(seq))
initialLedger.verifyState(s, state)
print("VALID")
# while True:
#     seq = seq + 1
#     print("getting ledger")
#     ledger = getLedger(seq)
#     print("verifying txs")
#     txs = getLedgerTransactions(seq)
#     print(len(txs))
#     ledger.verifyTransactions(txs)
#     print("verifying state")
#     diff = getLedgerDiff(seq)
#     print(diff)
#     ledger.verifyState(state, diff)
#     print("verified state")
