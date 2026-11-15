import importlib.util
import struct
import unittest
import zlib
from pathlib import Path
HERE=Path(__file__).parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py')); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

class FloorTests(unittest.TestCase):
    def test_fill_preserves_original_and_binds_slots(self):
        m=load('comfy_floor'); original={'a':['__LS1_PREFIX__',{'seed':'__LS1_SEED__'}]}
        self.assertEqual(m.fill(original,'unique',7),{'a':['unique',{'seed':7}]}); self.assertEqual(original['a'][0],'__LS1_PREFIX__')
    def test_megapixel_fixture_is_valid_and_distinct(self):
        m=load('image_fixture'); png=m.make_image('one'); self.assertEqual(len(png),1048576); self.assertNotEqual(png,m.make_image('two'))
        pos=8; packed=b''; dimensions=None
        while pos<len(png):
            n=struct.unpack('>I',png[pos:pos+4])[0]; kind=png[pos+4:pos+8]; data=png[pos+8:pos+8+n]; crc=struct.unpack('>I',png[pos+8+n:pos+12+n])[0]
            self.assertEqual(crc,zlib.crc32(kind+data)&0xffffffff)
            if kind==b'IHDR': dimensions=struct.unpack('>II',data[:8])
            if kind==b'IDAT': packed+=data
            pos+=n+12
        self.assertEqual(dimensions,(1024,1024)); decoded=zlib.decompress(packed); self.assertEqual(len(decoded),(1024*3+1)*1024); self.assertEqual(pos,len(png))
    def test_png_size_chunks_and_distinct_content(self):
        m=load('runtime_floor'); a=m.make_payload(1048576,1,None); b=m.make_payload(1048576,2,None)
        self.assertNotEqual(a,b); self.assertEqual(len(a),1048576); self.assertEqual(a[:8],b'\x89PNG\r\n\x1a\n')
        pos=8; kinds=[]
        while pos<len(a):
            n=struct.unpack('>I',a[pos:pos+4])[0]; kind=a[pos+4:pos+8]; data=a[pos+8:pos+8+n]; crc=struct.unpack('>I',a[pos+8+n:pos+12+n])[0]
            self.assertEqual(crc,zlib.crc32(kind+data)&0xffffffff); kinds.append(kind); pos+=n+12
        self.assertEqual(kinds,[b'IHDR',b'IDAT',b'npAD',b'IEND']); self.assertEqual(pos,len(a))
if __name__=='__main__': unittest.main()
