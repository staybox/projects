import sys
import subprocess
import argparse
import ctypes


def abc(args):
  a = args.size
  platf = sys.platform
  print platf
  if 'linux' in platf:
      if a != '':
        cmd = 'lsblk -io KNAME,SIZE'
      else:
        cmd = 'lsblk -io KNAME'
      subprocess.call(cmd, shell=True)
  elif 'Windows' in platf:
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', required=False, default='', help='to see a disk sizes')
    args = parser.parse_args()
    abc(args)