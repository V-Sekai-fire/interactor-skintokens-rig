#!/usr/bin/env python3
"""Extract a Godot 4 .pck (unencrypted): pck_x.py file.pck outdir"""
import io, os, struct, sys
d = open(sys.argv[1], 'rb').read(); out = sys.argv[2]
ver = struct.unpack('<I', d[4:8])[0]; b = io.BytesIO(d); base = 0
if ver >= 3:
    flags, base, dirpos = struct.unpack('<IQQ', d[20:40]); b.seek(dirpos)
else:
    b.seek(20 + 4 + 8 + 16 * 4)
n = struct.unpack('<I', b.read(4))[0]
for _ in range(n):
    ln = struct.unpack('<I', b.read(4))[0]
    path = b.read(ln).rstrip(b'\0').decode().removeprefix('res://')
    off, size = struct.unpack('<QQ', b.read(16)); b.read(16); b.read(4)
    p = os.path.join(out, path); os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'wb').write(d[base + off: base + off + size])
print(n, 'files')
