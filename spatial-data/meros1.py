#!/usr/bin/env python3
#DIMITRA CHRISTINA GKARAVELA  ΑΜ: 5051
import argparse
import sys
from typing import List, Tuple
from pymorton import interleave_latlng
from operator import itemgetter

def morton(lat: float, lon: float) -> str:
    raw = interleave_latlng(lat, lon)             
    return raw.rjust(32, "0")

MAX = 20   # μέγιστος αριθμός εγγραφών σε κόμβο
MIN = 8    # ελάχιστος (0.4 × MAX)
MBR = Tuple[float, float, float, float]     # (xmin, xmax, ymin, ymax)


def mbr(points: List[Tuple[float, float]]) -> MBR:
    xs = []   
    ys = []   

    for (x, y) in points:
        xs.append(x)
        ys.append(y)

    xmin = min(xs)      # πιο αριστερό x
    xmax = max(xs)      # πιο δεξί   x
    ymin = min(ys)      # πιο χαμηλό y
    ymax = max(ys)      # πιο ψηλό   y

    return (xmin, xmax, ymin, ymax)


def pack(lst):
    groups = []
    i = 0
    while i < len(lst):
        groups.append( lst[i : i + MAX] )   # κόψε υπολίστα
        i += MAX                            # προχώρησε κατά MAX

    if len(groups) > 1:                       
        last_group      = groups[-1]          
        previous_group  = groups[-2]         

        if len(last_group) < MIN:            
            need = MIN - len(last_group)      
            to_move = previous_group[-need:]
            last_group[:0] = to_move         
            groups[-2] = previous_group[:-need]

    return groups


def mbr_union(entries):
    first_mbr = entries[0][1]          
    xmin, xmax, ymin, ymax = first_mbr
    for _cid, mbr in entries[1:]:
        child_xmin, child_xmax, child_ymin, child_ymax = mbr
        xmin = min(xmin, child_xmin)
        xmax = max(xmax, child_xmax)
        ymin = min(ymin, child_ymin)
        ymax = max(ymax, child_ymax)
    return (xmin, xmax, ymin, ymax)

def load(coords_file: str, offsets_file: str):
    points: List[Tuple[float, float]] = []

    with open(coords_file, "r") as fh:
        for line in fh:
            x_str, y_str = line.strip().split(",")
            points.append( (float(x_str), float(y_str)) )
    # offsets
    objects = []    

    with open(offsets_file, "r") as fh:
        for line in fh:
            line = line.strip()
            if line == "":            
                continue

            obj_id_str, start_str, end_str = line.split(",")

            obj_id = int(obj_id_str)
            start  = int(start_str)
            end    = int(end_str)

            poly_pts = points[start : end + 1]          # σημεία πολυγώνου
            mb       = mbr(poly_pts)                    # MBR του πολυγώνου

            cx = (mb[0] + mb[1]) / 2
            cy = (mb[2] + mb[3]) / 2
            z  = morton(cy, cx)

            objects.append((z, obj_id, mb)) 
  
    objects.sort(key=itemgetter(0))   # ταξινόμηση βάσει z
    return objects

def build(objects):
    levels = [] 
    # φύλλα 
    leaves = []
    for group in pack(objects):           # κόψε τα objects 20-20
        entries = []
        for _z, oid, mb in group:
            entries.append( (oid, mb) )
        leaves.append( {"leaf": True, "entries": entries} )
    levels = [leaves]

    # γονικά 
    level_index = 1 
    while len(levels[-1]) > 1:            # μέχρι να μείνει μία ρίζα
        prev_level = levels[-1]           # κόμβοι τρέχοντος επιπέδου
        parents = []

        for group in pack(prev_level):      
            parent_entries = []
            for child in group:
                parent_entries.append( (None, mbr_union(child["entries"])) )
            parents.append({
                "leaf": False,
                "entries": parent_entries,   
                "children": group            
            })
        levels.append(parents)     
        level_index += 1

    return levels


def flatten(levels):
    nodes = []
    for lvl in levels:         
        for node in lvl:      
            nodes.append(node)
    idmap = {}
    for i, node in enumerate(nodes):
        idmap[id(node)] = i  

    for node in nodes:
        if node["leaf"]:
            continue          

        new_entries = []
        for i in range(len(node["entries"])):
            mbr_child = node["entries"][i][1]          # Πάρε το mbr από το entry
            child_node = node["children"][i]           # Πάρε το αντίστοιχο παιδί
            child_id = idmap[id(child_node)]           # Βρες το id
            new_entries.append((child_id, mbr_child))  # Φτιάξε το νέο entry

        node["entries"] = new_entries    
        del node["children"]            

    return nodes


def save(nodes, path="Rtree.txt"):
    out_file = open(path, "w", encoding="utf-8")
    for node_id, node in enumerate(nodes):

        # αν είναι φύλλο  ->  isnonleaf = 0
        # αν είναι εσωτερικός ->  isnonleaf = 1
        if node["leaf"]:
            isnonleaf = 0
        else:
            isnonleaf = 1

        nice_entries = []
        for entry_id, mbr in node["entries"]:
            nice_entries.append([entry_id, list(mbr)])

        line = f"[{isnonleaf}, {node_id}, {nice_entries}]\n"
        out_file.write(line)

    out_file.close()

def main():
    coords = sys.argv[1]  
    offsets = sys.argv[2]  

    objects = load(coords, offsets)
    levels = build(objects)


    print()
    for lvl, nodes in enumerate(levels):
        n = len(nodes)
        word = "node" if n == 1 else "nodes"
        print(f"{n} {word} at level {lvl}")

    save(flatten(levels))

if __name__ == "__main__":
    main()

