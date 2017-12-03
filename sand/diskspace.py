import sys
import subprocess
import argparse
import re

"""
Launch from Windows:
diskspace.py or diskspace.py --disk=0
Launch from Linux:
python diskspace.py or python diskspace.py --disk=0
"""

class Volume(object):
    def find_size(self, cmd):
        disk_list = {}
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        number = 0
        for line in process.stdout:
            size = re.search('\d{3,}', line) #more than 3 digits in the string
            if size is not None and 'Size' not in line:
                index = re.search('^\S{1,4}', line)  # non spaces from the beginning
                index = index.group(0)
                size = round(float(size.group(0))/(1024**3), 1)
                disk_list.update({number: [index, size]})
                number += 1
        errcode = process.returncode
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', cmd)
        return disk_list


class System(Volume):

    def find_disk_size(self, platform):
        if 'linux' in platform:
            cmd = 'lsblk -d -io KNAME,SIZE -e 1,11 --byte'
        else:
            cmd = 'wmic diskdrive get index,size'
        disk_list = self.find_size(cmd)
        return disk_list


class Disk(Volume):

    def find_partition_size(self, platf, disk_number, res):
        disk_number = int(disk_number)
        cmd = ''
        #res = {0: ['1', 55.9], 1: ['0', 29.1]}
        #res = {0: ['sda', 12.0]}
        for k, v in res.items():
            if k == disk_number:
                disk_id = v[0]
                if 'linux' in platf:
                    cmd = "lsblk -io KNAME,SIZE,TYPE -e 1,11 --byte | grep '^{0}[[:digit:]]'".format(disk_id)
                else:
                    cmd = 'wmic partition where DiskIndex={0} get index,size'.format(disk_id)
        print cmd
        if cmd == '':
                raise Exception('Invalid disk_number (--disk={0})'.format(disk_number))
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
    res = s.find_disk_size(platform)
    if disk_number != '':  # no arguments -> check disks only
        res = d.find_partition_size(platform, disk_number, res)
    for k, v in res.items():
        print '#{0} = {1}GB;'.format(k, v[1])
