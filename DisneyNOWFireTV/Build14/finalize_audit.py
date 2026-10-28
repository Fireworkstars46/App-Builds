#!/usr/bin/env python3
from pathlib import Path
import argparse,base64,hashlib,io,zipfile
BASE={'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '666db196e93161faaac3f7b15bd109cf16b081a7e9f80c40e3d94b064454047f', 'tools/static_audit.py': '89da46d4b864320dcd4b4e65556e42efa97837f851d9a6106ab6d60eee7ef28c'}
RESULT={'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '5694f7e260df484f27a7ca7df26471f0a93f6d6dc94175607ab28b05fcd3fb3b', 'tools/static_audit.py': 'a253f91a74019a35183882b550187364f474103d3609ef29cd3314390e011d57'}
ZIP_SHA='d3b98c9447dfa7e69a85eb6b625a896b54eb5c73e4962cf81f3cf3059b542061'
PARTS=['part00.b64', 'part01.b64', 'part02.b64', 'part03.b64', 'part04.b64', 'part05.b64']
def h(b):return hashlib.sha256(b).hexdigest()
def check(root,want,label):
 bad=[]
 for r,x in want.items():
  p=root/r; y=h(p.read_bytes()) if p.is_file() else 'missing'
  if x!=y:bad.append(f"{r}: expected {x}, got {y}")
 if bad:raise SystemExit(label+' hash verification failed\n'+'\n'.join(bad))
def main():
 q=argparse.ArgumentParser();q.add_argument('--source',required=True);a=q.parse_args();root=Path(a.source).resolve();check(root,BASE,'Build 14 pre-finalization')
 d=Path(__file__).resolve().parent/'audit_final_parts';raw=base64.b64decode(''.join((d/n).read_text() for n in PARTS),validate=True)
 if h(raw)!=ZIP_SHA:raise SystemExit('Build 14 audit finalizer ZIP mismatch')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  if set(z.namelist())!=set(RESULT):raise SystemExit('Build 14 audit finalizer entries mismatch')
  for r,x in RESULT.items():
   b=z.read(r)
   if h(b)!=x:raise SystemExit('Build 14 audit finalizer payload mismatch: '+r)
   (root/r).write_bytes(b)
 check(root,RESULT,'Build 14 finalized');print('Build 14 audit finalization applied and verified.')
if __name__=='__main__':main()
