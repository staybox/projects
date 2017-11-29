import sys
import subprocess
import argparse


def find_sizes(args):
  disk = args.disk
  platf = sys.platform
  if 'linux' in platf:
      if disk == '':
          cmd = 'lsblk -d -io KNAME,SIZE -e 1,11'
      else:
          cmd = 'lsblk -io KNAME,SIZE -e 1,11 | grep -E "^{0}[[:digit:]].|KNAME"'.format(disk)

  elif 'win' in platf:
      if disk == '':
          cmd = 'wmic diskdrive get size,index'
      else:
          cmd = 'wmic partition where DiskIndex={0} get index,size'.format(disk)
  result = []
  process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
  for line in process.stdout:
      result.append(line)
  errcode = process.returncode
  for line in result:
      print(line)
  if errcode is not None:
      raise Exception('cmd %s failed, see above for details', cmd)
      

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--disk', required=False, default='')
    args = parser.parse_args()
find_sizes(args)
