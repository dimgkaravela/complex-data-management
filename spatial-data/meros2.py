#!/usr/bin/env python3
# DIMITRA CHRISTINA GKARAVELA  ΑΜ: 5051


from ast import literal_eval
import sys
from typing import List, Tuple, Dict

MBR = Tuple[float, float, float, float]          
Node = Dict[str, object]                         


def intersects(a: MBR, b: MBR) -> bool:
    ax1, ax2, ay1, ay2 = a       
    bx1, bx2, by1, by2 = b
    x_overlap = (ax1 <= bx2) and (ax2 >= bx1)
    y_overlap = (ay1 <= by2) and (ay2 >= by1)
    return x_overlap and y_overlap


def range_search(tree: List[Node], root_id: int,
                 window: MBR, out: List[int]) -> None:
    node = tree[root_id]

    if node['leaf']:
        # κάθε entry = [object_id, MBR]
        for oid, mbr in node['entries']:
            if intersects(mbr, window):
                out.append(oid)
    else:
        # κάθε entry = [child_id, MBR]
        for child_id, mbr in node['entries']:
            if intersects(mbr, window):
                range_search(tree, child_id, window, out)


def load_tree(path: str) -> List[Node]:
    nodes: List[Node] = []

    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = literal_eval(line.strip())  
            isnonleaf = parts[0]
            node_id = parts[1]
            entries = parts[2]

            while len(nodes) <= node_id:
                nodes.append(None)           
            nodes[node_id] = {
                'leaf': (isnonleaf == 0),
                'entries': entries            
            }

    return nodes


def run_queries(tree: List[Node], queries_path: str) -> None:
    with open(queries_path) as f:
        for line_no, line in enumerate(f):
            if not line.strip():
                continue

            x_low, y_low, x_high, y_high = map(float, line.split())
            window = (x_low, x_high, y_low, y_high)

            results: List[int] = []
            range_search(tree, root_id=len(tree) - 1,   # ρίζα = τελευταία γραμμή
                         window=window, out=results)

            ids_txt = ",".join(map(str, results))
            print(f"{line_no} ({len(results)}): {ids_txt}")


def main():
    rtree_file = sys.argv[1]
    queries_file = sys.argv[2]
    tree = load_tree(rtree_file)
    run_queries(tree, queries_file)


if __name__ == "__main__":
    main()
