import sys
import subprocess
import argparse
import re


class Volume(object):
    def find_size(self, cmd):
        disk_list = []
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            rline = re.search('^\d+', line)
            if rline is not None:
                rline = round(float(rline.group(0))/(1024**3), 1)
                rline = str(rline)+' GB'
                disk_list.append(rline)
        errcode = process.returncode
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', cmd)
        return disk_list


class System(Volume):

    def find_disk_size(self, platform):
        if 'linux' in platform:
            cmd = 'lsblk -d -io KNAME,SIZE -e 1,11'
        else:
            cmd = 'wmic diskdrive get size'
        disk_list = self.find_size(cmd)
        return disk_list


class Disk(Volume):

    def find_partition_size(self, platf, disk):
        if 'linux' in platf:
            cmd = 'lsblk -io KNAME,SIZE -e 1,11 | grep -E "^{0}[[:digit:]].|KNAME"'.format(disk)
        else:
            cmd = 'wmic partition where DiskIndex={0} get index,size'.format(disk)
        disk_list = self.find_size(cmd)
        return disk_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--disk', required=False, default='')
    args = parser.parse_args()
    d = Disk()
    s = System()
    disk_number = args.disk
    platform = sys.platform
    assert ('linux' in platform or 'win' in platform)
    if disk_number == '':  # no arguments -> check disks only
        res = s.find_disk_size(platform)
    else:
        res = d.find_partition_size(platform, disk_number)
    for i in res:
        print(i)
