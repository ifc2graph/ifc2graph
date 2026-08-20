"""Write IfcElement/IfcSpace nodes and intersection/collision edges to Neo4j."""

from __future__ import annotations
from collections.abc import Iterable, Sequence
from neo4j import GraphDatabase
from ifc2graph.clash import Clash, element_props


def create_node(tx, props: dict) -> None:
    """Merge a ``:BuildingElement`` node by ``global_id``."""
    tx.run(
        """
        MERGE (e:BuildingElement {global_id: $global_id})
        SET e.ifc_class = $ifc_class,
            e.name = $name
        """,
        **props,
    )


def create_relationship(
    tx, a_id: str, b_id: str, rel_type: str, clash_type: str
) -> None:
    """Merge an undirected clash relationship between two nodes."""

    tx.run(
        f"""
        MATCH (a:BuildingElement {{global_id: $a_id}})
        MATCH (b:BuildingElement {{global_id: $b_id}})
        MERGE (a)-[r:`{rel_type}`]-(b)
        SET r.clash_type = $clash_type
        """,
        a_id=a_id,
        b_id=b_id,
        clash_type=clash_type,
    )


def write_to_neo4j(
    uri: str,
    auth: tuple[str, str],
    elements: Iterable,
    clashes: Sequence[Clash],
) -> None:
    """Clear Neo4j, then write ``IfcElement`` / ``IfcSpace`` nodes and edges.

    Args:
        uri: Neo4j Bolt URI, e.g. ``bolt://localhost:7687``.
        auth: ``(username, password)`` tuple.
        elements: IFC products to store as ``:BuildingElement`` nodes.
        clashes: Pairwise edges from `~ifc2graph.clash.detect_clashes`.

    Warning:
        The target database is fully cleared before writing.
    """
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run(
            "CREATE CONSTRAINT unique_global_id IF NOT EXISTS "
            "FOR (e:BuildingElement) REQUIRE e.global_id IS UNIQUE"
        )

        for el in elements:
            session.execute_write(create_node, element_props(el))

        for clash in clashes:
            session.execute_write(
                create_relationship,
                clash.element1,
                clash.element2,
                clash.rel_type,
                clash.collision_type,
            )

    driver.close()
