# Graph schema

### Nodes

Every `IfcElement` and every `IfcSpace` becomes a node labelled `:BuildingElement`.

| Property | Meaning |
| --- | --- |
| `global_id` | IFC `GlobalId` (unique) |
| `ifc_class` | IFC type name, e.g. `IfcWall`, `IfcSpace`, `IfcDoor` |
| `name` | IFC `Name`, or an empty string if unset |

`IfcSpace` is not a subtype of `IfcElement` in the IFC schema, which is why both are collected explicitly.

### Relationships

An edge is created whenever clash detection reports a hit between two items. The relationship type name is built from the two IFC class names with the `Ifc` prefix removed, for example `Wall-Slab` or `Space-Door`.

Each edge carries one property:

| Property | Values |
| --- | --- |
| `clash_type` | `protrusion`, `pierce`, or `collision` |

!!! note
    <b>Relationship direction</b>. Relationships in the graph represent clashs between two elements and are therefore semantically undirected. `A` clashing `B` is the same fact as `B` clashing `A`. Neo4j stores relationships with a direction, but this direction is used only as a storage convention and does not carry semantic meaning. During clash detection, element pairs are canonicalized by sorting their identifiers, so each pair is stored only once. Queries should therefore use undirected Cypher patterns such as `(a)--(b)` or `(a)-[r]-(b)`.
