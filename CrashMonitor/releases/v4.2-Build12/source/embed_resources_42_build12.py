from PIL import Image, ImageDraw
import io, struct
from pathlib import Path

build = Path(__file__).resolve().parent
src = build/'Crash_Monitor_v4.2_Build_12_Setup-noicon.exe'
out = build/'Crash_Monitor_v4.2_Build_12_Setup.exe'

manifest = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">\r\n  <assemblyIdentity version="4.2.12.0" processorArchitecture="amd64" name="CrashMonitor.Application" type="win32"/>\r\n  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">\r\n    <security>\r\n      <requestedPrivileges>\r\n        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>\r\n      </requestedPrivileges>\r\n    </security>\r\n  </trustInfo>\r\n  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">\r\n    <application>\r\n      <supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"/>\r\n      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>\r\n      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>\r\n      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>\r\n      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>\r\n    </application>\r\n  </compatibility>\r\n</assembly>\r\n'''
(build/'Crash_Monitor_v4.2_Build_12.manifest').write_bytes(manifest)

def make_icon(size):
    scale=4
    S=size*scale
    im=Image.new('RGBA',(S,S),(0,0,0,0))
    d=ImageDraw.Draw(im)
    pad=int(S*0.045)
    d.rounded_rectangle([pad,pad,S-pad-1,S-pad-1],radius=int(S*0.24),fill=(28,117,229,255))
    x0,y0,x1,y1=[int(v*S) for v in (0.19,0.25,0.81,0.68)]
    lw=max(2,int(S*0.045))
    d.rounded_rectangle([x0,y0,x1,y1],radius=int(S*0.05),outline=(255,255,255,255),width=lw)
    cx=S//2
    d.line([(cx,int(S*0.69)),(cx,int(S*0.78))],fill=(255,255,255,255),width=lw)
    d.line([(int(S*0.36),int(S*0.79)),(int(S*0.64),int(S*0.79))],fill=(255,255,255,255),width=lw)
    pts=[(0.25,0.48),(0.35,0.48),(0.41,0.40),(0.47,0.59),(0.54,0.35),(0.61,0.48),(0.75,0.48)]
    pts=[(int(x*S),int(y*S)) for x,y in pts]
    d.line(pts,fill=(255,255,255,255),width=max(2,int(S*0.035)),joint='curve')
    return im.resize((size,size),Image.Resampling.LANCZOS)

sizes=[16,32,48,256]
pngs=[]
for s in sizes:
    im=make_icon(s)
    bio=io.BytesIO(); im.save(bio,format='PNG',optimize=True); pngs.append(bio.getvalue())
make_icon(256).save(build/'Crash-Monitor-icon.png')
make_icon(256).save(build/'Crash-Monitor.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])

b=bytearray(src.read_bytes())
pe=struct.unpack_from('<I',b,0x3c)[0]
fh=pe+4
machine,nsec,ts,ptrsym,nsym,optsz,char=struct.unpack_from('<HHIIIHH',b,fh)
opt=fh+20
magic=struct.unpack_from('<H',b,opt)[0]
if magic!=0x20b: raise SystemExit('expected PE32+')
sec_table=opt+optsz
first_raw=min(struct.unpack_from('<I',b,sec_table+i*40+20)[0] for i in range(nsec))
if sec_table+(nsec+1)*40>first_raw: raise SystemExit('no room for section header')
section_align=struct.unpack_from('<I',b,opt+32)[0]
file_align=struct.unpack_from('<I',b,opt+36)[0]
def align(x,a): return (x+a-1)//a*a
last_end_va=0
for i in range(nsec):
    o=sec_table+i*40
    vs,va,rs,rp=struct.unpack_from('<IIII',b,o+8)
    last_end_va=max(last_end_va, va+max(vs,rs))
rsrc_va=align(last_end_va,section_align)
raw_ptr=align(len(b),file_align)
if len(b)<raw_ptr: b.extend(b'\0'*(raw_ptr-len(b)))

N=len(pngs)
# Root: RT_ICON(3), RT_GROUP_ICON(14), RT_MANIFEST(24)
root_off=0; root_size=16+3*8
icon_type_off=root_off+root_size; icon_type_size=16+N*8
icon_lang_offs=[]; pos=icon_type_off+icon_type_size
for _ in range(N): icon_lang_offs.append(pos); pos+=24
group_type_off=pos; pos+=24
group_lang_off=pos; pos+=24
manifest_type_off=pos; pos+=24
manifest_lang_off=pos; pos+=24
icon_data_entry_offs=[]
for _ in range(N): icon_data_entry_offs.append(pos); pos+=16
group_data_entry_off=pos; pos+=16
manifest_data_entry_off=pos; pos+=16
pos=align(pos,4)
icon_blob_offs=[]
for data in pngs:
    icon_blob_offs.append(pos); pos+=len(data); pos=align(pos,4)
entries=[]
for i,(s,data) in enumerate(zip(sizes,pngs),1):
    bw=0 if s>=256 else s; bh=0 if s>=256 else s
    entries.append(struct.pack('<BBBBHHIH',bw,bh,0,0,1,32,len(data),i))
group_blob=struct.pack('<HHH',0,1,N)+b''.join(entries)
group_blob_off=pos; pos+=len(group_blob); pos=align(pos,4)
manifest_blob_off=pos; pos+=len(manifest); pos=align(pos,4)
actual_size=pos
rsrc=bytearray(actual_size)
def wr(off,fmt,*vals): struct.pack_into(fmt,rsrc,off,*vals)
# Root directory: 3 ID entries
wr(root_off,'<IIHHHH',0,0,0,0,0,3)
wr(root_off+16,'<II',3,0x80000000|icon_type_off)
wr(root_off+24,'<II',14,0x80000000|group_type_off)
wr(root_off+32,'<II',24,0x80000000|manifest_type_off)
# Icons
wr(icon_type_off,'<IIHHHH',0,0,0,0,0,N)
for i in range(N):
    wr(icon_type_off+16+i*8,'<II',i+1,0x80000000|icon_lang_offs[i])
    lo=icon_lang_offs[i]
    wr(lo,'<IIHHHH',0,0,0,0,0,1)
    wr(lo+16,'<II',1033,icon_data_entry_offs[i])
# Group icon type -> ID 1 -> en-US
wr(group_type_off,'<IIHHHH',0,0,0,0,0,1)
wr(group_type_off+16,'<II',1,0x80000000|group_lang_off)
wr(group_lang_off,'<IIHHHH',0,0,0,0,0,1)
wr(group_lang_off+16,'<II',1033,group_data_entry_off)
# Manifest type -> ID 1 -> en-US
wr(manifest_type_off,'<IIHHHH',0,0,0,0,0,1)
wr(manifest_type_off+16,'<II',1,0x80000000|manifest_lang_off)
wr(manifest_lang_off,'<IIHHHH',0,0,0,0,0,1)
wr(manifest_lang_off+16,'<II',1033,manifest_data_entry_off)
# Data entries and blobs
for i,data in enumerate(pngs):
    wr(icon_data_entry_offs[i],'<IIII',rsrc_va+icon_blob_offs[i],len(data),0,0)
    rsrc[icon_blob_offs[i]:icon_blob_offs[i]+len(data)]=data
wr(group_data_entry_off,'<IIII',rsrc_va+group_blob_off,len(group_blob),0,0)
rsrc[group_blob_off:group_blob_off+len(group_blob)]=group_blob
wr(manifest_data_entry_off,'<IIII',rsrc_va+manifest_blob_off,len(manifest),65001,0)
rsrc[manifest_blob_off:manifest_blob_off+len(manifest)]=manifest

raw_size=align(len(rsrc),file_align)
rsrc.extend(b'\0'*(raw_size-len(rsrc)))
b.extend(rsrc)
sh=sec_table+nsec*40
chars=0x40000040
struct.pack_into('<8sIIIIIIHHI',b,sh,b'.rsrc\0\0\0',actual_size,rsrc_va,raw_size,raw_ptr,0,0,0,0,chars)
struct.pack_into('<H',b,fh+2,nsec+1)
sid=struct.unpack_from('<I',b,opt+8)[0]
struct.pack_into('<I',b,opt+8,sid+raw_size)
struct.pack_into('<I',b,opt+56,align(rsrc_va+actual_size,section_align))
# Resource data directory (PE32+ data dirs start at opt+112, resource index 2)
struct.pack_into('<II',b,opt+112+2*8,rsrc_va,actual_size)
out.write_bytes(b)
print('wrote',out,len(b),'resource bytes',actual_size,'rva',hex(rsrc_va),'raw',hex(raw_ptr))
