# ifc2graph

Convert an IFC model into a graph.

<picture>
  <img src="https://ifc2graph.github.io/ifc2graph/images/ifc2graph-illustrations.png" alt="ifc2graph illustrations">
</picture>

ifc2graph loads every building element (`IfcElement` and `IfcSpace`) in an IFC model, runs clash detection (`protrusion`, `pierce`, or `collision`) on their geometry, and writes the resulting nodes and edges to a graph database. The graph generation is solely based on geometries and not on IFC relationship entities.

**The underlying idea is simple.** For every element in the IFC model, candidate elements are first identified using a [BVH tree](https://docs.ifcopenshell.org/ifcopenshell-python/geometry_tree.html). Clash detection is then performed against these candidates, and whenever the triangulated meshes of two elements are found to clash, ifc2graph connects them in the graph.

Overall, ifc2graph is useful for:

- treating an IFC file as a queryable graph of elements and spaces
- inferring adjacency from geometric interaction rather than from IFC relationship entities
- tracing navigable routes (via rooms, doors, and stairs) as paths through the graph
- inspecting how two elements interact, whether by protrusion, pierce, or collision

For more information, see 📝 [Documentation](https://ifc2graph.github.io/ifc2graph/):

- [Installation](https://ifc2graph.github.io/ifc2graph/installation/)
- [Usage](https://ifc2graph.github.io/ifc2graph/#usage)
- [Graph schema](https://ifc2graph.github.io/ifc2graph/graph/)
- [Examples](https://ifc2graph.github.io/ifc2graph/querying/)
- [API reference](https://ifc2graph.github.io/ifc2graph/api/)
- [License](https://ifc2graph.github.io/ifc2graph/license-dependencies/)


## Install

Requires Python 3.10 or newer.

```bash
pip install -U ifc2graph
```


## Usage

The API is straightforward. Pass an IFC model, Neo4j connection details (and optional arguments) to `ifc2graph()`.

```python
from ifc2graph import ifc2graph

clashes = ifc2graph(
    "model.ifc",    # IFC model                  
    
    # Neo4j connection (not required if "export_to_neo4j=False")
    uri="bolt://localhost:7687", 
    user="neo4j",
    password="password",
 
    # optional arguments: "export_to_neo4j", "tolerance" and "allow_touching".
)
```

**The target Neo4j database is cleared on every run** (`MATCH (n) DETACH DELETE n`) before anything is written. Point this at an empty or disposable database.

## Citation

Please cite the following paper if you use ifc2graph in your work:

```bibtex
@article{lamsal2026ifcllm,
      title={IfcLLM: Natural Language Querying of IFC Models through Complementary Relational and Graph Representations}, 
      author={Rabindra Lamsal and Sisi Zlatanova and Haowen Xu and Yafei Sun and Johnson Xuesong Shen},
      year={2026},
      eprint={2605.13236},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2605.13236}, 
}
```