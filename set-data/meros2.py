#DIMITRA CHRISTINA GKARAVELA AM:5051
import sys
import time
import ast
from collections import defaultdict

def read_transactions(file_path):
    transactions = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = ast.literal_eval(line)
            transactions.append([str(i) for i in items])
    return transactions

def build_inverted_index(transactions):
    inverted = defaultdict(lambda: defaultdict(int))  # item -> {tid: occ}
    trf = defaultdict(int)  # item -> number of transactions containing item
    T = len(transactions)
    for tid, items in enumerate(transactions):
        seen = set()
        for item in items:
            inverted[item][tid] += 1
            if item not in seen:
                trf[item] += 1
                seen.add(item)
    weights = {item: T / freq for item, freq in trf.items()}
    inv_lists = {
        item: sorted([[tid, occ] for tid, occ in tids.items()], key=lambda x: x[0])
        for item, tids in inverted.items()
    }
    return inv_lists, weights, T

def write_invfile(inv_lists, weights, output_path):
    with open(output_path, 'w') as f:
        for item in sorted(inv_lists.keys(), key=lambda x: int(x) if x.isdigit() else x):
            f.write(f"{item}: {weights[item]}, {inv_lists[item]}\n")

def read_queries(file_path):
    queries = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = ast.literal_eval(line)
            queries.append([str(i) for i in items])
    return queries

def naive_method(query, transactions, weights, k):
    rels = []
    for tid, items in enumerate(transactions):
        count = defaultdict(int)
        for i in items:
            if i in query:
                count[i] += 1
        rel = sum(count[i] * weights.get(i, 0) for i in query)
        if rel > 0:
            rels.append([rel, tid])
    rels.sort(key=lambda x: x[0], reverse=True)
    return rels[:k]

def inverted_method(query, inv_lists, weights, k):
    rel_dict = defaultdict(float)
    for i in query:
        if i not in inv_lists:
            continue
        w = weights.get(i, 0)
        for tid, occ in inv_lists[i]:
            rel_dict[tid] += occ * w
    rels = [[rel, tid] for tid, rel in rel_dict.items() if rel > 0]
    rels.sort(key=lambda x: x[0], reverse=True)
    return rels[:k]

def main():
    if len(sys.argv) != 6:
        print("Usage: python relevance_queries.py <transactions> <queries> <qnum> <method> <k>")
        sys.exit(1)
    tx_file, q_file, qnum_str, method_str, k_str = sys.argv[1:]
    qnum = int(qnum_str)
    method = int(method_str)
    k = int(k_str)

    transactions = read_transactions(tx_file)
    inv_lists, weights, T = build_inverted_index(transactions)
    write_invfile(inv_lists, weights, 'invfileocc.txt')

    queries = read_queries(q_file)

    # Naive method timing/result
    if method in (-1, 0):
        t0 = time.time()
        if qnum == -1:
            # τρέχουμε για όλες τις ερωτήσεις, χωρίς εκτύπωση
            for q in queries:
                _ = naive_method(q, transactions, weights, k)
        else:
            res = naive_method(queries[qnum], transactions, weights, k)
            print("Naive Method result:")
            print(res)
        t1 = time.time()
        print(f"Naive Method total computation time = {t1 - t0:.6f}s")

    # Inverted-file method timing/result
    if method in (-1, 1):
        t0 = time.time()
        if qnum == -1:
            # τρέχουμε για όλες τις ερωτήσεις, χωρίς εκτύπωση
            for q in queries:
                _ = inverted_method(q, inv_lists, weights, k)
        else:
            res = inverted_method(queries[qnum], inv_lists, weights, k)
            print("Inverted File result:")
            print(res)
        t1 = time.time()
        print(f"Inverted File total computation time = {t1 - t0:.6f}s")

if __name__ == '__main__':
    main()
