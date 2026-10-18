# SkinTokens rig program

A small Godot 4 project that runs the SkinTokens rig guest, `skintokens.elf`, on Godot's
RenderingDevice. It rigs one GLB file and writes the rigged GLB.

- In a browser it uses WebGPU and reads the weights with HTTP range requests. This is the rig
  preview on the Space [chibifire/skintokens-auto-rig](https://huggingface.co/spaces/chibifire/skintokens-auto-rig).
- On a desktop it uses Vulkan or Metal and reads the weights from files.

The desktop viewer [V-Sekai-fire/entities-model-explorer](https://github.com/V-Sekai-fire/entities-model-explorer)
has its own copy of the host loop (`AutoRig.gd`, press R).

## Build inputs

These files are not in the repo. Put them in place before you run or export:

- `skintokens.elf`: build it from
  [V-Sekai-fire/interactor-skintokens-guest](https://github.com/V-Sekai-fire/interactor-skintokens-guest).
- `addons/godot_sandbox/bin/libgodot_riscv.*`: the godot-sandbox libraries named in
  `godot-riscv.gdextension`, from the CI artifacts of
  [V-Sekai-fire/godot-sandbox](https://github.com/V-Sekai-fire/godot-sandbox).
- The weights: `mesh-encoder.gguf`, `skin-vae.gguf` and `tokenrig.gguf` from
  [chibifire/SkinTokens-GGUF-BF16](https://huggingface.co/chibifire/SkinTokens-GGUF-BF16).

The engine is a Godot 4.8 double-precision build.

## Run on a desktop

```sh
godot --path . --rendering-driver vulkan -- models=<weights dir> mesh=<in.glb> out=<out.glb>
```

Relative paths start at the project folder. The program prints `RIG-OK` with the size, the time
and the sha256 of the result, or `FAIL` with the reason.

## Export for the web

```sh
godot --headless --path . --export-pack Web index.pck
```

The page gives `models`, `mesh`, `opts` and `mem` as URL parameters. `mesh=local` reads the GLB
that the parent page put in `window.__rig_mesh_b64`.

## Tools

- `tools/pck_x.py <file.pck> <dir>` extracts a pck, so you can compare two exports with `diff -rq`.
- `tools/serve_range.py <dir> <port>` is a local test server with range requests and the
  cross-origin isolation headers that threads need.

## Tests

On an Apple M2 Pro, the desktop run with Metal and with Vulkan (MoltenVK) gave SK_Robot, SK_Alien
and MarocchinoLP output byte-identical to the reference rig. A GLB that is not valid stops with
`FAIL`.

## License

MIT. See `LICENSE`.
