"""End-to-end IFC → geometry graph → Neo4j pipeline."""

from __future__ import annotations

import os
import time

from ifc2graph.clash import (
    Clash,
    build_geometry_tree,
    detect_clashes,
    get_elements,
    load_model,
)
from ifc2graph.neo4j_io import write_to_neo4j


def ifc2graph(
    ifc_path: str,
    *,
    uri: str | None = None,
    user: str | None = None,
    password: str | None = None,
    tolerance: float = 0.002,
    allow_touching: bool = True,
) -> list[Clash]:
    """Load an IFC model, detect clash, write Neo4j.

    Nodes are all ``IfcElement`` and ``IfcSpace``. Edges are unique pairwise
    clash hits (protrusion, pierce, collision).
    The target Neo4j database is always cleared before writing.

    Neo4j connection defaults can be set via ``NEO4J_URI``, ``NEO4J_USER``,
    and ``NEO4J_PASSWORD`` environment variables.

    Args:
        ifc_path: Path to a ``.ifc`` file.
        uri: Neo4j Bolt URI. Defaults to ``NEO4J_URI`` or ``bolt://localhost:7687``.
        user: Neo4j username. Defaults to ``NEO4J_USER`` or ``neo4j``.
        password: Neo4j password. Defaults to ``NEO4J_PASSWORD``. Required.
        tolerance: Intersection tolerance.
        allow_touching: Whether touching (zero-volume) collisions count as hits.

    Returns:
        Unique pairwise clash written to Neo4j.

    Raises:
        ValueError: If no Neo4j password is provided or found in the environment.
    """
    uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = user or os.environ.get("NEO4J_USER", "neo4j")
    password = password if password is not None else os.environ.get("NEO4J_PASSWORD")
    if not password:
        raise ValueError(
            "Neo4j password required: pass password=... or set NEO4J_PASSWORD"
        )

    start_model_load_time = time.time()
    model = load_model(ifc_path)
    end_model_load_time = time.time()
    print(f"Model loaded in {end_model_load_time - start_model_load_time:.2f} seconds.")

    tree = build_geometry_tree(model)

    elements = get_elements(model)
    print(f"{len(elements)} elements retrieved.")

    print("Clash detection started.")
    start_clashes_detection_time = time.time()
    clashes = detect_clashes(
        tree, elements, tolerance=tolerance, allow_touching=allow_touching
    )
    end_clashes_detection_time = time.time()
    print(f"Clashes detected in {end_clashes_detection_time - start_clashes_detection_time:.2f} seconds.")  

    print(f"Writing {len(clashes)} clash relationships to Neo4j.")
    start_neo4j_write_time = time.time()
    write_to_neo4j(uri, (user, password), elements, clashes)
    end_neo4j_write_time = time.time()
    print(f"Neo4j written in {end_neo4j_write_time - start_neo4j_write_time:.2f} seconds.")

    return clashes
