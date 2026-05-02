# Complex Data Management

Implementations of relational, spatial, and set-valued data management algorithms.

This repository contains three independent assignments focused on core data management techniques, including relational operators, spatial indexing with R-trees, and query processing over transactional/set-valued data.

## Repository Structure

```text
complex-data-management/
├── relational-operators/
├── spatial-data/
├── set-data/
└── README.md
```

## 1. Relational Operators

Folder: ```relational-operators```

This assignment implements basic relational query operators over tabular data stored in TSV files.

### Implemented operations:

- Merge Join
- Union
- Intersection
- Set Difference
- Group-by Aggregation with Sum

The implementations focus on sequential file processing, sorted input handling, duplicate elimination, and memory-aware execution of relational operators.

## 2. Spatial Data and R-tree Indexing

Folder: ``` spatial-data ```

This assignment implements an R-tree index for spatial objects represented by polygon minimum bounding rectangles.

### Implemented functionality:

- Reading spatial objects from coordinate and offset files
- Computing Minimum Bounding Rectangles (MBRs)
- Bulk loading an R-tree
- Sorting spatial objects using z-order values
- Writing the constructed R-tree to an output file
- Executing range queries
- Executing k-nearest-neighbor queries using best-first search

The goal is to support efficient spatial query processing over non-traditional spatial data.

## 3. Set-Valued Data

Folder: ``` set-data ```

This assignment implements query processing methods for transactional and set-valued data.

### Implemented functionality:

- Containment queries
- Naive containment evaluation
- Exact signature file
- Exact bitslice signature file
- Inverted file
- Relevance queries
- Occurrence-aware inverted lists
- Top-k relevance ranking

The implementations compare simple scanning methods with indexed approaches for efficient query evaluation.


## Data Files
The original course datasets are not included in this repository.

The programs are designed to run with external input files provided through the course platform. This keeps the repository focused on the source code and documentation rather than the input datasets.

