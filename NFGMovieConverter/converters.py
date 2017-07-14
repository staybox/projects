# coding: utf8
from __future__ import print_function
import subprocess
from multiprocessing import cpu_count
import ConfigParser
import os.path as op


def convertation_test():
    """
    function for testing other methods
    """
    mp3_languages = 'RU'
    FHD = 'export_tests/FOI_16_05/FOI_YY_MM_removed_sound.mp4'
    HD = 'export_tests/FOI_16_05/HD.mp4'
    MD = 'export_tests/FOI_16_05/MD.avi'
    wav = 'sons/RU.wav'
    mp3 = 'sons/RU.mp3'
    FHD_with_sound = 'RU_FHD.mp4'
    HD_with_sound = 'RU_HD.mp4'
    MD_with_sound = 'RU_MD.avi'

    #wav2mp3(wav, mp3)
    #to_HD(FHD, HD)
    to_MD(HD, MD)
    # mux(mp3, FHD, FHD_with_sound)
    # mux(mp3, HD, HD_with_sound)
    # mux(mp3, MD, MD_with_sound)

    print ('finished')


def to_HD(FHD, HD):
    """
    reformating video file from FHD.mp4 1080p to HD.mp4 720p
    ffmpeg -i export_tests/FOI_16_05/FOI_YY_MM.mp4 -threads 2 -an -vcodec h264 -b:v 2100k -s 960x720 -deinterlace -aspect 16:9 -pass 1 -passlogfile HD_pass -f mp4 -y /dev/null
    ffmpeg -i export_tests/FOI_16_05/FOI_YY_MM.mp4 -threads 2 -an -vcodec h264 -b:v 2100k -s 960x720 -deinterlace -aspect 16:9 -pass 2 -passlogfile HD_pass -f mp4 -y export_tests/FOI_16_05/HD.mp4
    :param FHD:
    :param HD:
    """
    #  -an = remove sound
    aspect = config_parser(FHD) #path to FHD file
    arguments = '-an -vcodec h264 -b:v 2100k -s 960x720 -deinterlace'
    cmd1 = 'ffmpeg -i {0} -threads {1} {2} -aspect {3} -pass 1 -passlogfile HD_pass -f mp4 -y {4}'\
        .format(FHD, cpu_count(), arguments, aspect, '/dev/null')
    cmd2 = 'ffmpeg -i {0} -threads {1} {2} -aspect {3} -pass 2 -passlogfile HD_pass -f mp4 -y {4}'\
        .format(FHD, cpu_count(), arguments, aspect, HD)
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)


def to_MD(HD, MD):
    """
    reformating video file from HD.mp4 720p to MD.avi 576p
    ffmpeg -i export_tests/FOI_16_05/HD.mp4 -threads 2 -an -c:v mpeg4 -b:v 1400k -bt 142k -maxrate 3316k -bufsize 663.2k -r 25 -s 720x576 -trellis 0 -me_range 16 -b_strategy 1 -mbd rd -g 200 -qmin 3 -qmax 51 -qdiff 4 -sc_threshold 40 -sn -f avi -vtag DX50 -deinterlace -aspect 16:9 -pass 1 -passlogfile MD_pass -f avi -y /dev/null
    ffmpeg -i export_tests/FOI_16_05/HD.mp4 -threads 2 -an -c:v mpeg4 -b:v 1400k -bt 142k -maxrate 3316k -bufsize 663.2k -r 25 -s 720x576 -trellis 0 -me_range 16 -b_strategy 1 -mbd rd -g 200 -qmin 3 -qmax 51 -qdiff 4 -sc_threshold 40 -sn -f avi -vtag DX50 -deinterlace -aspect 16:9 -pass 2 -passlogfile MD_pass -vtag DX50 -f avi -y export_tests/FOI_16_05/MD.avi
    :param HD: path to HD file
    :param MD: path to MD file
    :param config_path: to take aspect out from config
    """
    # cmd1 and cmd2 are different, why ' -vtag DX50' is doubled in cmd2 ?
    # netforgod@f55-srv-vm-nfg-saul4:netforgod-tv/postproduction/bin/toxvid
    aspect = config_parser(HD)
    arguments = '-an -c:v mpeg4 -b:v 1400k -bt 142k -maxrate 3316k -bufsize 663.2k -r 25 -s 720x576' \
                ' -trellis 0 -me_range 16 -b_strategy 1 -mbd rd -g 200 -qmin 3 -qmax 51 -qdiff 4 -sc_threshold 40 -sn' \
                ' -f avi -vtag DX50 -deinterlace'
    cmd1 = 'ffmpeg -i {0} -threads {1} {2} -aspect {3} -pass 1 -passlogfile MD_pass -f avi -y {4}'\
        .format(HD, cpu_count(), arguments, aspect, '/dev/null')
    cmd2 = 'ffmpeg -i {0} -threads {1} {2} -aspect {3} -pass 2 -passlogfile MD_pass -vtag DX50 -f avi -y {4}'\
        .format(HD, cpu_count(), arguments, aspect, MD)
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)


def wav2ac3(wav, ac3):
    """
    reformating audio file from LL.wav to LL.ac3 (RU.wav - RU.ac3).
    lame - program for ecnoding the sound
    :param wav:
    :param ac3:
    """
    #cmd = 'lame -b 224 --resample 48000 {0} {1}'.format(wav, ac3)
    cmd = 'ffmpeg -i {0} -threads {1} -ar 48000 -ab 224k -y {2}'.format(wav, cpu_count(), ac3)
    subprocess.call(cmd, shell=True)


def wav2mp3(wav, mp3):
    """
    reformating audio file from LL.wav to LL.mp3 (RU.wav - RU.mp3)
    :param wav:
    :param mp3:
    """
    #cmd = 'lame -b 192 --resample 44100 {0} {1}'.format(wav, mp3)
    cmd = 'ffmpeg -i {0} -threads {1} -acodec mp3 -ar 44100 -ab 192k -y {2}'.format(wav, cpu_count(), mp3)
    subprocess.call(cmd, shell=True)


def mux(sound, video_in, video_out):
    """
    mux the video with audio for all the languages. FHD.mp4, HD.mp4, MD.avi with LL.mp3 (FHD.mp4 + RU.mp3 = RU_FHD.mp4)
    :param sound:
    :param video_in:
    :param video_out:
    """
    cmd = 'ffmpeg -i ' + video_in + ' -i ' + sound + ' -c:v copy -c:a copy -y ' + video_out
    subprocess.call(cmd, shell=True)


# def remove_sound_FHD():
#     """
#     removing sound from the video if we need it. We will not use it as well
#     """
#     cmd = 'ffmpeg -i FOI_YY_MM.mp4 -c:v copy -an FOI_YY_MM_removed_sound.mp4'
#     subprocess.call(cmd, shell=True)


def config_parser(fname):
    """
    read the config file with aspect ratio parameters (16:9 or 4:3)
    :param fname: we gets path to the folder with the films and here it will be change for a config path.
    (export_tests/FOI_16_02/parametres_example.ini)
    """
    path = op.dirname(fname) + '/parameters.ini'
    print (path)
    conf = ConfigParser.ConfigParser()
    conf.read(path)
    aspect_ratio = conf.get('values', 'aspect_ratio')
    return aspect_ratio


# if __name__ == '__main__':
#     convertation_test()
