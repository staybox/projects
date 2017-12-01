import sys
import subprocess
import argparse
from abc import ABCMeta, abstractmethod, abstractproperty


class Volume(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_size(self, args):
        """FInd size of some volume"""


class Disk(Volume):
    def find_size(self, cmd):
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

    def find_disk_size(self, platform):
        if 'linux' in platform:
            cmd = 'lsblk -d -io KNAME,SIZE -e 1,11'
        elif 'win' in platform:
            cmd = 'wmic diskdrive get size,index'
        self.find_size(cmd)

    def find_partition_size(self, platf, disk):
        if 'linux' in platf:
            cmd = 'lsblk -io KNAME,SIZE -e 1,11 | grep -E "^{0}[[:digit:]].|KNAME"'.format(disk)
        elif 'win' in platf:
            cmd = 'wmic partition where DiskIndex={0} get index,size'.format(disk)
        self.find_size(cmd)


def go(args):
    d = Disk()
    disk_number = args.disk
    platform = sys.platform
    assert ('linux' in platform or 'win' in platform)
    if disk_number == '': # no arguments -> check disks only
        d.find_disk_size(platform)
    else:
        d.find_partition_size(disk_number)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--disk', required=False, default='')
    args = parser.parse_args()
    go(args)
