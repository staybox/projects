# coding: utf8
import subprocess
import time


def upload_to_jonas():
    """
    Sync the folder Jonas.
    NFG_Movies - all the folder 'export' exclude mp3 and texts. There are no any deletes on Jonas here, only upload.
    NFG_DropBox - folder for one month only for Dropbox. Will renew the files every month: delete the old files and
    upload new. Only the folder 'videos' with 3 different qualities.
    path_from - the path to all of the videos on the server
    path_to - folder on Jonas for uploading
    path_from2 - folder of this month
    path_to2 - folder for synchronization with Dropbox (upload only)
    """
    login_pass = 'pass'
    ip = '10.66.20.223'

    exclude = "{0} textes/ {1} *.mp3 {1} *.log {1} *.mbtree {1} *.ini {1} *.db".format("--exclude", "--exclude-glob")
    #dry_run = "--dry-run"
    dry_run = ''
    delete = '--delete'

    path_from1 = '/home/netforgod/export/'
    path_to1 = 'Com-NFG_Saul5/NFG_Movies'

    this_month = time.strftime("%y_%m")  # this month YY_MM = 16_05
    path_from2 = "/home/netforgod/export/FOI_{0}/videos/".format(this_month)
    db_folder_name = time.strftime("%Y_%B").upper()  # this month YYYY_MONTH = 2016_JUNE
    path_to2 = 'Com-NFG_Saul5/NFG_Dropbox/Films_Net_for_God/' + db_folder_name
    print(path_to2)
    cmd = "lftp -e 'mirror -c -R {0} {1} {2} {3}; bye;' -u {4} {5}"\
        .format(exclude, dry_run, path_from1, path_to1, login_pass, ip)

    cmd2 = "lftp -e 'mirror -c -R {0} {1} {2} {5}; bye;' -u {3} {4}"\
        .format(dry_run, path_from2, path_to2, login_pass, ip, delete)

    subprocess.call(cmd, shell=True)
    print(cmd)
    #subprocess.call(cmd2, shell=True) #we don't need anymore (29.09.2016) to have second for Dropbox. Every movie folder will be on Dropbox.
    #print(cmd2)


if __name__ == '__main__':
    upload_to_jonas()
