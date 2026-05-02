#!/usr/bin/env python3
# DIMITRA CHRISTINA GKARAVELA  ΑΜ 5051

import ast, heapq, math
import sys
from typing import List, Tuple, Dict

MBR   = Tuple[float, float, float, float]          # (xmin,xmax,ymin,ymax)
Entry = Tuple[int, MBR]                            # (id,   mbr)


def mindist(pt: Tuple[float, float], m: MBR) -> float:
    x, y = pt
    xmin, xmax, ymin, ymax = m
    if xmin <= x <= xmax:
        dx = 0  
    elif x < xmin:
        dx = xmin - x  
    else:
        dx = x - xmax 
    if ymin <= y <= ymax:
        dy = 0  
    elif y < ymin:
        dy = ymin - y  
    else:
        dy = y - ymax 

    return math.sqrt(dx**2 + dy**2)  


def load_rtree(path: str):
    nodes: Dict[int, Dict] = {}
    root_id = None
    with open(path) as f:
        for line in f:
            isnonleaf, node_id, entries = ast.literal_eval(line)
            nodes[node_id] = {"leaf": isnonleaf == 0, "entries": entries}
            root_id = node_id
    return nodes, root_id


def knn_search(nodes, root_id: int, q: Tuple[float, float], k: int) -> List[int]:
    heap = []                    
    root = nodes[root_id]
    for cid, m in root["entries"]:
        heapq.heappush(heap, (mindist(q, m), root["leaf"], cid, m))

    result = []
    while heap and len(result) < k:
        dist, is_leaf_entry, cid, m = heapq.heappop(heap)

        if is_leaf_entry:            
            result.append(cid)
            continue

        child = nodes[cid]
        for nid, cm in child["entries"]:
            heapq.heappush(heap, (mindist(q, cm), child["leaf"], nid, cm))

    return result


def main():
    rtree_file = sys.argv[1]       
    queries_file = sys.argv[2]     
    k = int(sys.argv[3])          

    nodes, root_id = load_rtree(rtree_file)

 
    with open(queries_file) as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split()
            q = (float(x_str), float(y_str))
            ids = knn_search(nodes, root_id, q, k)
            print(f"{idx}: {','.join(map(str, ids))}")

if __name__ == "__main__":
    main()