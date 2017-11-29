import sys
import subprocess
import argparse


def find_sizes(args):
  logicaldisks = args.logicaldisks
  partitions = args.partitions
  platf = sys.platform
  cmd = ''
  if 'linux' in platf:
      if logicaldisks != '':
          cmd = 'lsblk -io --bytes KNAME,SIZE'
      elif partitions != '':
          cmd = 'lsblk -io --bytes KNAME,SIZE'
      #subprocess.call(cmd, shell=True)
  elif 'win' in platf:
      if logicaldisks != '':
          cmd = 'wmic logicaldisk get size,name'
      elif partitions != '':
          cmd = 'wmic partition get size,name'
      else:
          raise Exception('choose please one of the parameteres: --logicaldisks=1 or --partitions=1')
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
    parser.add_argument('--partitions', required=False, default='', help='to see partitions sizes')
    parser.add_argument('--logicaldisks', required=False, default='', help='to see logicaldisks sizes')
    args = parser.parse_args()
    find_sizes(args)
