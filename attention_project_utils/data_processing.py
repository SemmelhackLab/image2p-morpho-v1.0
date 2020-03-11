import cv2
import h5py
import os
import re


def hdf_to_avi(hdf_path):
    video = h5py.File(hdf_path, 'r')
    keys = video.keys()
    images = sorted([int(re.findall('\d+', i)[0]) for i in keys])
    video_name = os.path.splitext(hdf_path)[0] + '.avi'
    height, width = video[0][:].shape
    video_out = cv2.VideoWriter(video_name, (width, height), isColor=False)

    for image in images:
        image = video[str(image)][:]
        video_out.write(image)

    video_out.release()
