# coding: utf8
from __future__ import print_function
import subprocess
import ConfigParser
import os.path as op
import re


def upload_to_youtube(FHD):
    """
    We will upload the FHD films of the last month to the youtube account NFG after every changes.
    It means that if we will change the video, program will upload this second time, and you will need to delete
    duplicates from youtube manually.
    FHD - fullpath to the video file
    """
    print (FHD)
    upload_to_youtube, keywords, category, privacyStatus = config_parser(FHD)
    title, description = get_title_and_description(FHD)
    print (title)
    print (description)
    script_path = '/home/netforgod/NFGMovieConverter/youtube_uploader/upload_video.py'
    cmd = 'python {0} --file="{1}" --title="{2}"  --description="{3}"  --keywords="{4}" ' \
          '--category="{5}" --privacyStatus="{6}" --noauth_local_webserver'\
           .format(script_path, FHD, title, description, keywords, category, privacyStatus)
    assert 'yes' in upload_to_youtube, 'Put "yes" in parameters.ini if you want to upload the video'
    subprocess.call(cmd, shell=True)


def get_title_and_description(fullpath):
    """
    The title of the video in youtube - 1st string from file FOI_YY_MM/textes/resume_EN.txt or resume_RU.txt
    Description for every language - string from file FOI_YY_MM/textes/resume_EN.txt or resume_RU.txt
    fullpath - name and path of the video file
    """
    filename = op.basename(fullpath) # filename = FOI_16_06_FR_FHD.mp4
    path_to_the_folder_textes = op.dirname(fullpath).replace('videos', 'textes/')
    LL = filename[10:12] # LL = RU or FR
    prefix = re.findall('\d\d_\d\d', fullpath) # find 16_05 = year and month
    description_path = get_description_path(LL, path_to_the_folder_textes) #resume_RU.txt
    if not op.exists(description_path): # if there are no resume_RN.txt - take another file
        LL = choose_alternative_lang(LL)
        description_path = get_description_path(LL, path_to_the_folder_textes)
    title, description = read_file(description_path)
    title = 'NFG_{0}_{1}_{2}'.format(prefix[0], LL, title) #NFG_Year_Month_Language_Title
    return title, description


def choose_alternative_lang(LL):
    if LL == 'JA':
        LL = 'EN'
    else:
        LL = 'FR' # RN, MU, MG
    return LL


def get_description_path(LL, path_to_the_folder_textes):
    description_file_name = 'resume_{0}.txt'.format(LL)
    description_path = path_to_the_folder_textes + description_file_name
    return description_path


def read_file(file_path):
    f = open(file_path, 'r')
    line = f.readlines()
    title = line[0] # take 1-st line
    descr = line[1:]
    description = ''
    for i in range(len(descr)): # read all the lines after 1
        description = description + descr[i] #compile all the lines
    f.close()
    title = clean_text(title)
    description = clean_text(description)
    return title, description


def clean_text(text):
    text = text.strip() # remove spaces from left and right
    text = text.replace('\n', '')
    text = text.replace('  ', ' ')
    return text


def config_parser(fullpath):
    # add config file with parameters of the video
    """
    read the config file with
    """
    path = fullpath.replace('videos/', '')
    path = op.dirname(path) + '/parameters.ini'
    #print(path)
    conf = ConfigParser.ConfigParser()
    conf.read(path)
    keywords = conf.get('youtube', 'keywords')
    category = conf.get('youtube', 'category')
    privacyStatus = conf.get('youtube', 'privacyStatus')
    upload_to_youtube = conf.get('youtube', 'upload_to_youtube')
    return upload_to_youtube, keywords, category, privacyStatus


# if __name__ == '__main__':
#     upload_to_youtube('/home/netforgod/export/FOI_16_06/videos/RU_MD.avi')
