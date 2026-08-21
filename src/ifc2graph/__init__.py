"""Convert an IFC model into a graph."""

from ifc2graph.clash import (
    COLLISION_TYPES,
    Clash,
    build_geometry_tree,
    detect_clashes,
    element_props,
    get_elements,
    load_model,
)
from ifc2graph.neo4j_io import write_to_neo4j
from ifc2graph.pipeline import ifc2graph
from ifc2graph.viewer import visualize

__all__ = [
    "COLLISION_TYPES",
    "Clash",
    "build_geometry_tree",
    "detect_clashes",
    "element_props",
    "get_elements",
    "ifc2graph",
    "load_model",
    "visualize",
    "write_to_neo4j",
]

__version__ = "0.2.0"
