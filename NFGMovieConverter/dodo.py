# coding=utf-8
"""
The doit command file for building the NFG movies

to use it, do:
>doit --dir path/to/export_dir
run: doit --dir ~/export_tests/
change after to: doit --dir ~/export/
"""
from __future__ import print_function
import glob
import os
import os.path as op
import subprocess
from time import strftime
import converters
import run_uploads
import doit


###### CONFIGURATION ############

DOIT_CONFIG = {
    # backend of db in json, for easier debugging
    'backend': 'json',
    # any change in the date will trigger execution - more greedy, but faster than MD5.
    # 'check_file_uptodate': 'timestamp',
    # output from actions should be sent to the terminal/console
    'verbosity': 2,
    # does not stop execution on first task failure
    'continue': True,
    # doit should only report on executed actions
    # 'reporter': 'executed-only',
    # use multi-processing / parallel execution
    'num_process': 1,
}

DOIT_CONFIG['reporter'] = 'executed-only'

###################### lists of targets
# on the saul4 we should use absolute path because video folder export_tests is not inside the NFGMovieConverter folder
LIST_OF_WAV = glob.glob('FOI_*/sons/*.wav')
LIST_OF_FHD = glob.glob('FOI_*/FOI*.mp4')
LIST_OF_LL_FHD = glob.glob('FOI_*/videos/*FHD.mp4')
LIST_OF_video = glob.glob('FOI_*/*.avi') + glob.glob('FOI_*/*.mp4')


# and dependet targets
def change_ext_in_list(lst, new_ext):
    """change all extensions in file names in list"""
    return [op.splitext(l)[0] + new_ext for l in lst]


def change_name_in_list(lst, new_name):
    """change all name in file names in list"""
    return [op.split(l)[0] + new_name for l in lst]



class Converters(object):
    # fake actions - for testing - only create empty files
    # real actions are in converters
    def action(self, typea, infile, outfile, ):
        print("Action", typea, infile, outfile)
        subprocess.call('echo %s - %s > %s' % (typea, infile, outfile), shell=True)

    def wav2ac3(self, infile, outfile):
        self.action("WAV to AC3 :", infile, outfile)

    def wav2mp3(self, infile, outfile):
        self.action("WAV 2 MP3 :", infile, outfile)

    def to_MD(self, infile, outfile):
        self.action("to MD :", infile, outfile)

    def to_HD(self, infile, outfile):
        self.action("to HD :", infile, outfile)

    def mux(self, infile, infile2, outfile):
        self.action("Mux :", "%s-%s" % (infile, infile2), outfile)


###################### DOIT Tasks
def task_wav_convert():
    """ Sounds conversion from wav to ac3 and from wav to mp3"""
    for fname in LIST_OF_WAV:
        fullpath = op.abspath(fname)
        outname = op.splitext(fname)[0] + '.ac3'
        yield {
            'name': outname,  # name required to identify tasks
            'file_dep': [fullpath],  # file dependency
            'targets': [outname],
            # In case there is no modification in the dependencies and the targets already exist, it skips the task.
            # If a target doesn’t exist the task will be executed.
            'actions': [(converters.wav2ac3, (fname, outname))],
        }
        outname2 = op.splitext(fname)[0] + '.mp3'
        yield {
            'name': outname2,  # name required to identify tasks
            'file_dep': [fullpath],  # file dependency
            'targets': [outname2],
            'actions': [(converters.wav2mp3, (fname, outname2))],
        }


def task_FHD_convert():
    """ Video conversion
     we should calculate the path to the directory with config file
     """
    for fname in LIST_OF_FHD:
        fullpath = op.abspath(fname)
        outname = op.join(op.dirname(fname), 'HD.mp4')  # new name after the conversion
        yield {
            'name': outname,  # name required to identify tasks
            'file_dep': [fullpath],  # file dependency
            'targets': [outname],
            'actions': [(converters.to_HD, (fname, outname))],
        }
        outname2 = op.join(op.dirname(fname), 'MD.avi')
        yield {
            'name': outname2,  # name required to identify tasks
            'file_dep': [fullpath],  # file dependency
            'targets': [outname2],
            'actions': [(converters.to_MD, (fname, outname2))],
        }


# @create_after('FHD_convert', target_regex='.+\.mp4$')
def task_mux():
    """ Muxing FHD, HD, MD with mp3 """
    for videoname in LIST_OF_video:
        fullpath = op.abspath(videoname)
        dirname = op.dirname(videoname)
        fname = op.basename(videoname)
        if fname.startswith('FOI_'):  # rename Full HD to standard name
            fname = 'FHD.mp4'
        list_of_mp3 = glob.glob(op.join(dirname, "sons/*.mp3"))
        if DEBUG:
            print("list of MP3", list_of_mp3)
        for fname_mp3 in list_of_mp3:
            LL = op.basename(fname_mp3)[0:-4]
            outname = op.join(dirname, "videos", dirname + "_" + LL + "_" + fname) # FOI_16_06_FR_HD.mp4
            try:
                os.mkdir(op.join(dirname, "videos"))
            except OSError:
                pass  # error if dir already exists
            yield {
                'name': outname,  # name required to identify tasks
                'file_dep': [fullpath, fname_mp3],  # file dependency
                'targets': [outname],
                'actions': [(converters.mux, (videoname, fname_mp3, outname))],
            }


def task_upload_to_youtube_this_month():
    """
    run the run_uploads.py which will runs the upload_video.py with the parameters
    fname = export_tests/FOI_YY_MM/videos/FOI_16_06_FR_FHD.mp4
    fullpath = /home/alex/Documents/my_project/CCN/NFGMovieConverter/export_tests/FOI_YY_MM/videos/FOI_16_06_FR_FHD.mp4
    Send fullpath to the youtube uploader.
    if this_month... - to check if fname folder is folder of the current month or not. If yes - upload it to youtube.
    LIST_OF_LL_FHD = ['FOI_15_05/videos/FOI_15_05_MU_FHD.mp4', ..., 'FOI_16_10/videos/FOI_16_10_PT_FHD.mp4', 'FOI_20_20/videos/FOI_20_20_FR_FHD.mp4']
    this_month = '16_10'
    """
    LIST_OF_LL_FHD = glob.glob('FOI_*/videos/*FHD.mp4')
    #print(LIST_OF_LL_FHD)
    this_month = strftime("%y_%m")
    for fname in LIST_OF_LL_FHD:
        #if this_month in fname:
        if this_month in fname or '20_20' in fname:
            fullpath = op.abspath(fname)
            #print(fullpath)
            yield {
                'name': fname,       # name required to identify tasks
                'file_dep': [fullpath],  # file dependency
                'actions': [(run_uploads.upload_to_youtube, (fullpath,))]
                }


# if __name__ == '__main__':
#     task_upload_to_youtube_this_month()
