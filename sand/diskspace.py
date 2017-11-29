import sys
import subprocess
import argparse


def find_sizes(args):
  logicaldisk = args.logicaldisk
  partition = args.partition
  platf = sys.platform
  cmd = ''
  if 'linux' in platf:
      if logicaldisk != '':
          cmd = 'lsblk -d -io KNAME,SIZE -e 1,11'
      elif partition != '':
          cmd = 'lsblk -io KNAME,SIZE -e 1,11 | grep -E "^sda[[:digit:]].|KNAME"'

  elif 'win' in platf:
      if logicaldisk != '':
          cmd = 'wmic logicaldisk get size,name'
      elif partition != '':
          cmd = 'wmic partition get size,name'
      else:
          raise Exception('choose please one of the parameteres: --logicaldisk=1 or --partition=1')
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
    parser.add_argument('--partition', required=False, default='', help='to see partition sizes')
    parser.add_argument('--logicaldisk', required=False, default='', help='to see logicaldisk sizes')
    args = parser.parse_args()
    find_sizes(args)
