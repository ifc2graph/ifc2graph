"""IFC geometry loading and intersection/collision detection."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import ifcopenshell
import ifcopenshell.geom


@dataclass(frozen=True)
class Clash:
    """A dataclass to store clash information."""

    element1: str
    """IFC ``GlobalId`` of the first entity."""
    element2: str
    """IFC ``GlobalId`` of the second entity."""
    rel_type: str
    """Edge type derived from IFC class names, e.g. ``Wall-Slab``."""
    collision_type: str
    """One of `COLLISION_TYPES`."""


COLLISION_TYPES = ["protrusion", "pierce", "collision", "clearance"]
"""IfcOpenShell defined clash categories."""


def load_model(ifc_path: str):
    """Open an IFC file with IfcOpenShell.

    Args:
        ifc_path: Path to a ``.ifc`` file.

    Returns:
        An IfcOpenShell file object.
    """
    return ifcopenshell.open(ifc_path)


def build_geometry_tree(model):
    """Populate an IfcOpenShell geometry tree from the model.

    Args:
        model: An open IfcOpenShell file.

    Returns:
        A populated ``ifcopenshell.geom.tree`` used for clash queries.
    """
    tree = ifcopenshell.geom.tree()
    settings = ifcopenshell.geom.settings()
    iterator = ifcopenshell.geom.iterator(settings, model)

    if iterator.initialize():
        while True:
            tree.add_element(iterator.get())
            if not iterator.next():
                break

    return tree


def get_elements(model) -> list:
    """Return all ``IfcElement`` and ``IfcSpace`` instances in the model.

    Args:
        model: An open IfcOpenShell file.

    Returns:
        All ``IfcElement`` and ``IfcSpace`` instances.
    """
    return model.by_type("IfcElement") + model.by_type("IfcSpace")


def element_props(el) -> dict:
    """Extract properties to be used for graph nodes.

    Args:
        el: An ``IfcElement`` or ``IfcSpace`` instance.

    Returns:
        Mapping with ``global_id``, ``ifc_class``, and ``name``.
    """
    return {
        "global_id": el.GlobalId,
        "ifc_class": el.is_a(),
        "name": el.Name or "",
    }


def _clash_to_edge(clash) -> Clash:
    element1 = clash.a
    element2 = clash.b
    element1_id = element1.get_argument(0)
    element2_id = element2.get_argument(0)
    collision_type = COLLISION_TYPES[clash.clash_type]
    rel_type = (
        element1.is_a().split("Ifc")[-1] + "-" + element2.is_a().split("Ifc")[-1]
    )
    return Clash(element1_id, element2_id, rel_type, collision_type)


def detect_clashes(
    tree,
    elements: Sequence,
    *,
    tolerance: float = 0.002,
    allow_touching: bool = True,
) -> list[Clash]:
    """Detect geometry clash; return unique pairwise clashes.

    Combines IfcOpenShell ``clash_intersection_many`` and ``clash_collision_many``
    over the given ``IfcElement`` / ``IfcSpace`` set, and de-duplicates.

    Args:
        tree: Geometry tree from `build_geometry_tree`.
        elements: ``IfcElement`` / ``IfcSpace`` instances to test.
        tolerance: Intersection tolerance in model units.
        allow_touching: Whether touching (zero-volume) collisions count as hits.

    Returns:
        Unique pairwise clashes.
    """
    collisions = tree.clash_collision_many(elements, elements, allow_touching=allow_touching)
    intersections = tree.clash_intersection_many(
        elements, elements, tolerance=tolerance, check_all=True
    )

    clashes_graph: list[Clash] = []
    seen: set[tuple[str, str]] = set()

    for raw in (*intersections, *collisions):
        edge = _clash_to_edge(raw)
        key = tuple(sorted((edge.element1, edge.element2)))
        if key in seen:
            continue
        seen.add(key)
        clashes_graph.append(edge)

    return clashes_graph
