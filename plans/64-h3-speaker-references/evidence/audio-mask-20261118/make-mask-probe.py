import struct
import subprocess

path = '/tmp/plan64-sr5-mask-probe.mkv'
values = [0, 32768, 65535, 12345]
frames = b''.join(struct.pack('<HHH', value, value, value) * 64 for value in values)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb48le',
                '-video_size', '8x8', '-framerate', '24', '-i', '-', '-c:v', 'ffv1',
                '-pix_fmt', 'gbrp16le', path], input=frames, check=True)
