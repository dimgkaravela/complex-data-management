#DIMITRA CHRISTINA GKARAVELA AM:5051
import sys
import time
from typing import List, Set, Dict


def read_transactions(file_path: str) -> List[Set[int]]:
    transactions: List[Set[int]] = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                transactions.append(set())
                continue
            # remove [ ]
            content = line[1:-1]
            items = [int(x) for x in content.split(',') if x.strip()]
            transactions.append(set(items))
    return transactions

def read_queries(file_path: str) -> List[Set[int]]:
    queries: List[Set[int]] = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                   queries.append(set())
                   continue
            # remove [ ]
            content = line[1:-1]
            items = [int(x) for x in content.split(',') if x.strip()]
            queries.append(set(items))
    return queries



def naive_containment_query(query: Set[int], transactions: List[Set[int]]) -> List[int]:
    result = []
    for tid, items in enumerate(transactions):
        if query.issubset(items):
            result.append(tid)
    return result


def build_signature_file(transactions: List[Set[int]]) -> List[int]:
    sigfile = []
    for items in transactions:
        sig = 0
        for item in items:
            if item < 0:
                raise ValueError(f"Invalid item id: {item}")
            sig |= (1 << item)
        sigfile.append(sig)
    with open('sigfile.txt', 'w') as fout:
        for sig in sigfile:
            fout.write(str(sig) + '\n')
    return sigfile


def signature_containment_query(query: Set[int], sigfile: List[int]) -> List[int]:
    qsig = 0
    for item in query:
        qsig |= (1 << item)
    result = []
    for tid, sig in enumerate(sigfile):
        if (sig & qsig) == qsig:
            result.append(tid)
    return result


def build_bitslice_file(transactions: List[Set[int]]) -> Dict[int, int]:
    bitslice: Dict[int, int] = {}
    for tid, items in enumerate(transactions):
        for item in items:
            if item < 0:
                raise ValueError(f"Invalid item id: {item}")
            bitslice.setdefault(item, 0)
            bitslice[item] |= (1 << tid)
    with open('bitslice.txt', 'w') as fout:
        for item in sorted(bitslice.keys()):
            fout.write(f"{item}: {bitslice[item]}\n")
    return bitslice


def bitslice_containment_query(query: Set[int], bitslice: Dict[int, int]) -> List[int]:
    it = iter(query)
    try:
        first = next(it)
    except StopIteration:
        return []
    if first not in bitslice:
        return []
    acc = bitslice[first]
    for item in it:
        if item not in bitslice:
            return []
        acc &= bitslice[item]
    result = []
    while acc:
        lsb = (acc & -acc)
        tid = lsb.bit_length() - 1
        result.append(tid)
        acc &= acc - 1
    result.sort()
    return result


def build_inverted_file(transactions: List[Set[int]]) -> Dict[int, List[int]]:
    inv: Dict[int, List[int]] = {}
    for tid, items in enumerate(transactions):
        for item in items:
            inv.setdefault(item, []).append(tid)
    for lst in inv.values():
        lst.sort()
    with open('invfile.txt', 'w') as fout:
        for item in sorted(inv.keys()):
            fout.write(f"{item}: {inv[item]}\n")
    return inv


def intersect_sorted(a: List[int], b: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return result


def inverted_containment_query(query: Set[int], inv: Dict[int, List[int]]) -> List[int]:
    items = list(query)
    if not items:
        return []
    if items[0] not in inv:
        return []
    res = inv[items[0]]
    for item in items[1:]:
        if item not in inv:
            return []
        res = intersect_sorted(res, inv[item])
        if not res:
            break
    return res


def main():
    if len(sys.argv) != 5:
        print("Usage: python program.py <transactions file> <queries file> <qnum> <method>")
        sys.exit(1)
    tfile, qfile, qnum_str, method_str = sys.argv[1:]
    qnum = int(qnum_str)
    method = int(method_str)

    transactions = read_transactions(tfile)
    queries = read_queries(qfile)

    sigfile = build_signature_file(transactions)
    bitslice = build_bitslice_file(transactions)
    invfile = build_inverted_file(transactions)

    names = {0: 'Naive Method', 1: 'Signature File', 2: 'Bitsliced Signature File', 3: 'Inverted File'}
    funcs = {
        0: lambda q: naive_containment_query(q, transactions),
        1: lambda q: signature_containment_query(q, sigfile),
        2: lambda q: bitslice_containment_query(q, bitslice),
        3: lambda q: inverted_containment_query(q, invfile),
    }

    methods = [method] if method != -1 else [0,1,2,3]

    for m in methods:
        name = names[m]
        func = funcs[m]
        if qnum == -1:
            start = time.time()
            for q in queries:
                _ = func(q)
            elapsed = time.time() - start
            print(f"{name} Computation time = {elapsed:.6f}")
        else:
            query = queries[qnum]
            start = time.time()
            res = func(query)
            elapsed = time.time() - start
            print(f"{name} result:")
            print(set(res))
            print(f"{name} Computation time = {elapsed:.6f}")

if __name__ == '__main__':
    main()
