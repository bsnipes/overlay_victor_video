#!/usr/bin/env python
"""
Take a Victor Player zip file and create a video with the timestamp overlayed at the bottom
"""
import datetime
import os
import sys
import xmltodict
from zipfile import ZipFile

video_filenames = []


def convert_integer_to_datetime(dt):
    dt = datetime.datetime.fromtimestamp(dt / 1000.0)
    dt = dt.strftime("%m/%d/%Y %I:%M:%S %p (CST)")
    return dt


def convert_integer_to_epoch(dt):
    # subtract 21600 for U.S. Central timezone
    return dt / 1000.0 - 21600


def get_manifest_from_zip(zf, manifest_filename):
    # read the manifest.xml from the zip file
    with ZipFile(zf, 'r') as zf_content:
        return zf_content.read(manifest_filename)


if __name__ == '__main__':
    if sys.argv[1]:
        # get zip contents
        print('Working on ' + sys.argv[1] + '\n')
        with ZipFile(sys.argv[1], 'r') as zipfile:
            zipfile_filelist = zipfile.namelist()
        for item in zipfile_filelist:
            if '.mp4' in item:
                print('... MP4 found as ' + item + '\n')
                video_filenames.append(item)
            if 'manifest.xml' in item:
                print('... manifest.xml found as ' + item + '\n')
                fh_contents = xmltodict.parse(get_manifest_from_zip(sys.argv[1], item))

        room = fh_contents['sessions']['string'][1]

        # extract video
        for video in video_filenames:
            if not os.path.isfile(video):
                print('... MP4 not found so extracting video from zip - ' + sys.argv[1] + '\n')
                with ZipFile(sys.argv[1]) as zipfile:
                    zipfile.extract(video)
        for videoindex in range(0, len(video_filenames)):
            if len(video_filenames) == 1:
                mp4basename = fh_contents['sessions']['session']['string'][0]
                video_time = convert_integer_to_datetime(int(fh_contents['sessions']['session']['integer'][0]))
                epoch_time = convert_integer_to_epoch(int(fh_contents['sessions']['session']['integer'][0]))
            else:
                mp4basename = fh_contents['sessions']['session'][videoindex]['string'][0]
                video_time = convert_integer_to_datetime(
                    int(fh_contents['sessions']['session'][videoindex]['integer'][0]))
                epoch_time = convert_integer_to_epoch(int(fh_contents['sessions']['session'][videoindex]['integer'][0]))
            new_filename = ' timestamped_' + mp4basename
            print(sys.argv[1], mp4basename, video_filenames[videoindex], room, video_time, epoch_time)
            cmd = 'ffmpeg -nostdin -i "' + os.path.join(
                video_filenames[videoindex]) + '" -vf "drawtext=fontfile=font.ttf:fontsize=40:fontcolor=white:box=1:' \
                  + 'boxcolor=black@0.4:x=(w-text_w)/2:y=h-th-10:text=\'%{pts\:gmtime\:' \
                  + str(epoch_time) + '\:' + room + '   %m\/%d\/%Y %I\\\\\\\\\:%M\\\\\\\\\:%S %p CST}\'\"' \
                  + new_filename + ' 2> /dev/null'
            # print(cmd)
            if os.path.exists(new_filename):
                os.remove(new_filename)
            os.system(cmd)
