"""Open a browser 3D view of IFC elements and spaces."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import webbrowser
from collections.abc import Sequence
from pathlib import Path

import ifcopenshell.geom

_PALETTE = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
]


def visualize(model, guids: str | Sequence[str]) -> Path:
    """Look up elements and spaces by `GlobalId` and open a 3D view in the browser.

    Args:
        model: An open IfcOpenShell file (from `ifc2graph.clash.load_model`).
        guids: One IFC ``GlobalId``, or a list of them.

    Returns:
        Path to the generated HTML file.

    Raises:
        ValueError: If none of the GlobalIds have drawable geometry.
    """
    if isinstance(guids, str):
        guids = [guids]
    meshes = _meshes_from_guids(model, guids)
    if not meshes:
        raise ValueError("none of the given GlobalIds have drawable geometry")

    fd, html_path = tempfile.mkstemp(suffix=".html", prefix="ifc2graph-")
    os.close(fd)
    path = Path(html_path)
    path.write_text(_HTML.replace("__MESHES__", json.dumps(meshes)), encoding="utf-8")
    webbrowser.open(path.as_uri())
    return path


def _geom_settings():
    settings = ifcopenshell.geom.settings()
    try:
        settings.set("use-world-coords", True)
    except Exception:
        settings.set(settings.USE_WORLD_COORDS, True)
    return settings


def _color_for_class(ifc_class: str) -> str:
    idx = int(hashlib.md5(ifc_class.encode()).hexdigest(), 16) % len(_PALETTE)
    return _PALETTE[idx]


def _meshes_from_guids(model, guids: Sequence[str]) -> list[dict]:
    settings = _geom_settings()
    meshes: list[dict] = []
    for guid in guids:
        try:
            el = model.by_guid(guid)
            shape = ifcopenshell.geom.create_shape(settings, el)
        except Exception:
            continue
        geo = shape.geometry
        faces = list(geo.faces)
        if not faces:
            continue
        ifc_class = el.is_a()
        meshes.append(
            {
                "name": el.Name or "",
                "ifc_class": ifc_class,
                "verts": [round(v, 4) for v in geo.verts],
                "faces": faces,
                "color": _color_for_class(ifc_class),
                "opacity": 0.35 if ifc_class == "IfcSpace" else 1.0,
            }
        )
    return meshes


_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ifc2graph viewer</title>
<style>
  html, body { margin: 0; overflow: hidden; background: #ffffff; }
  #hud {
    position: absolute; top: 12px; left: 12px; color: #222;
    font: 13px/1.4 sans-serif; pointer-events: none;
  }
</style>
</head>
<body>
<div id="hud"></div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const MESHES = __MESHES__;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.01, 10000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(devicePixelRatio);
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 0.8);
sun.position.set(1, 2, 1);
scene.add(sun);

const group = new THREE.Group();
group.rotation.x = -Math.PI / 2;
for (const mesh of MESHES) {
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(mesh.verts, 3));
  geometry.setIndex(mesh.faces);
  geometry.computeVertexNormals();
  const material = new THREE.MeshLambertMaterial({
    color: mesh.color,
    opacity: mesh.opacity,
    transparent: mesh.opacity < 1,
    side: THREE.DoubleSide,
    depthWrite: mesh.opacity >= 1,
  });
  group.add(new THREE.Mesh(geometry, material));
}
scene.add(group);

const box = new THREE.Box3().setFromObject(group);
const size = box.getSize(new THREE.Vector3());
const center = box.getCenter(new THREE.Vector3());
const span = Math.max(size.x, size.y, size.z, 1);
camera.position.set(center.x + span, center.y + span * 0.7, center.z + span);
camera.lookAt(center);
controls.target.copy(center);

const classes = [...new Set(MESHES.map((m) => m.ifc_class))];
document.getElementById("hud").textContent =
  MESHES.length + " products · " + classes.join(", ") + "\\n drag to orbit · scroll to zoom";

addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

(function tick() {
  requestAnimationFrame(tick);
  controls.update();
  renderer.render(scene, camera);
})();
</script>
</body>
</html>
"""
