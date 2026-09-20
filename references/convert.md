# Model Conversion Notes

The AR template consumes a **GLB** (and optionally a **USDZ** for iOS). Convert other formats first.

## Already GLB / GLTF
Ready to use — skip conversion. GLTF (with external `.bin`/textures) should be bundled into a single `.glb`
so it can be served as one file. Use `gltf-pipeline` (Node) or Blender's "Export → glTF Binary (.glb)".

## STL → GLB (Blender, cross-platform)

Blender (free) can be driven headless. Save this as `stl_to_glb.py` next to your file, then run:

```bat
blender --background --python stl_to_glb.py -- input.stl output.glb
```

```python
# stl_to_glb.py
import sys, bpy
argv = sys.argv
inp, outp = argv[argv.index("--") + 1], argv[argv.index("--") + 2]
bpy.ops.wm.stl_import(filepath=inp)
bpy.ops.export_scene.gltf(filepath=outp, export_format="GLB")
```

If the model is huge or off-center in AR, also recenter/scale it in Blender before export
(`Object → Set Origin → Origin to Geometry`, and apply a scale).

## 3MF → GLB (Blender)

Blender 3.x+ imports 3MF when the **3MF format** add-on is enabled
(Edit → Preferences → Add-ons → search "3MF" → enable). Then:

```bat
blender --background --python 3mf_to_glb.py -- input.3mf output.glb
```

```python
# 3mf_to_glb.py
import sys, bpy
argv = sys.argv
inp, outp = argv[argv.index("--") + 1], argv[argv.index("--") + 2]
bpy.ops.wm.usr_import?   # 3MF import operator name varies by Blender version
# Fallback: import via the UI operator name available in your Blender build, e.g.:
# bpy.ops.import_mesh.3mf(filepath=inp)
bpy.ops.export_scene.gltf(filepath=outp, export_format="GLB")
```

> If the 3MF operator name differs in your Blender version, open Blender, run the import from the UI once,
> and copy the exact operator from the Info editor.

## OBJ → GLB
Blender imports OBJ natively: `bpy.ops.wm.obj_import(filepath=inp)` then export GLB as above.

## GLB → USDZ (needed only for iOS AR)

- **macOS (easiest):** install **Reality Converter** (free, Apple) and open the GLB → Export USDZ.
  Or use the command-line `usdzconvert` from Apple's "USDZ Tools" / Xcode:
  ```bash
  usdzconvert model.glb model.usdz
  ```
- **Windows:** there is no first-party USDZ exporter. Options:
  1. Transfer the GLB to a Mac and convert there.
  2. Use a reputable online GLB→USDZ converter (upload only non-sensitive models).
  3. Build Pixar's USD toolset (`usd_from_gltf`) — heavy, not recommended for casual use.
- **Blender note:** Blender can export `.usdc`/`.usd` but not `.usdz` directly; do not rely on it for iOS AR.

## Quick decision

| Have | Need | Action |
|------|------|--------|
| `.glb` | Android only | Use as-is. |
| `.glb` | iOS too | Convert to `.usdz` (macOS/online). |
| `.stl`/`.3mf`/`.obj` | either | Convert to `.glb` via Blender, then optionally to `.usdz`. |
