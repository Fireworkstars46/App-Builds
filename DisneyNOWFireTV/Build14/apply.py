#!/usr/bin/env python3
from pathlib import Path
import argparse,base64,hashlib,io,zipfile
BASE={'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '2ace504d804fb354263c83e576c78910f2360e3f83ee25dd090260302190e055', 'app/build.gradle': '03997107cdec224b322613b7efc98a93abe7972a12f898895fc437e89e5b7d27', 'BUILD_INFO.md': '5df4ee811a42c92b83e0ca55d24098c6d43fd2d30b23275bd70f6c9836b17b74', 'README.md': '1c99c15d377cd9d26cf5527f3169b07b4fb23087cd1323a6667b823e6c3c1d0e', 'tools/static_audit.py': 'ed284d72750df93bf96fa50e17b0e3197ab57c7c58c6cee7686e3b2987a8fbf7'}
RESULT={'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '666db196e93161faaac3f7b15bd109cf16b081a7e9f80c40e3d94b064454047f', 'app/build.gradle': 'da9d541b6d854acdbab403c0244c67bc6a736863d8c86d5fecd2e725e4d21bea', 'BUILD_INFO.md': '08ae068d2c4e7977156446906bffd517276c6cd0af5ae81aff0ee184af5168cf', 'README.md': '876997b47b4dbaa86ca28d1543aa5824e184467e126a843f17f6d049a62898f6', 'tools/static_audit.py': '89da46d4b864320dcd4b4e65556e42efa97837f851d9a6106ab6d60eee7ef28c'}
PATCH_ZIP_SHA256='ab11b2d1e6e8c2c5067640f74b2ebb8a4c70f54bf204592a5171f053e96c1cef'
PATCH_PARTS=['part00.b64', 'part01.b64', 'part02.b64', 'part03.b64', 'part04.b64', 'part05.b64']
def sha(b): return hashlib.sha256(b).hexdigest()
def verify(root,expected,label):
 f=[]
 for r,w in expected.items():
  p=root/r; g=sha(p.read_bytes()) if p.is_file() else 'missing'
  if g!=w:f.append(f"{r}: expected {w}, got {g}")
 if f: raise SystemExit(label+' hash verification failed:\n'+'\n'.join(f))
def main():
 pa=argparse.ArgumentParser();pa.add_argument('--source',required=True);a=pa.parse_args();root=Path(a.source).resolve();verify(root,BASE,'Build 13 baseline')
 d=Path(__file__).resolve().parent/'patch_parts';data=base64.b64decode(''.join((d/n).read_text() for n in PATCH_PARTS),validate=True)
 if sha(data)!=PATCH_ZIP_SHA256: raise SystemExit('Build 14 patch ZIP SHA-256 mismatch')
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  if set(z.namelist())!=set(RESULT): raise SystemExit('Build 14 patch entries mismatch')
  for r in RESULT:
   b=z.read(r)
   if sha(b)!=RESULT[r]: raise SystemExit('Build 14 payload hash mismatch: '+r)
   p=(root/r).resolve()
   if root not in p.parents: raise SystemExit('Unsafe Build 14 patch path: '+r)
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 verify(root,RESULT,'Build 14 result');print('Build 14 lag/stability patch applied and verified.')
if __name__=='__main__': main()
