#!/usr/bin/env python3

import numpy as np
import scipy.io.wavfile
import sys
import cv2
import io
import argparse
import moviepy.editor as mvpy
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

mpl.use('agg')


class AudioSpectrumDrawer():

    def __init__(self, story_date):
        parent_dirname = os.path.dirname(__file__)
        self.wav_filename = '{}/../wav/{}.wav'.format(
            parent_dirname, story_date)
        self.bg_filename = '{}/../thumb/{}.png'.format(
            parent_dirname, story_date)
        self.output_filename = '{}/../output/{}.mp4'.format(
            parent_dirname, story_date)

        # load audio file
        self.audio_rate, self.voice = scipy.io.wavfile.read(self.wav_filename)
        self.voice = self.voice / 32768
        self.voice_length = self.voice.shape[0] / self.audio_rate
        self.time = np.arange(
            0, self.voice.shape[0] / self.audio_rate, 1/self.audio_rate)

        # load background image
        self.bg_image = cv2.imread(self.bg_filename)

        self.bg_height, self.bg_width, _ = self.bg_image.shape
        self.spectrum_height = 200

        # matplotlib params
        mpl_dpi = mpl.rcParams["figure.dpi"]
        self.w_inch = self.bg_width / mpl_dpi
        self.h_inch = self.spectrum_height / mpl_dpi

        self.video_fps = 30.0
        self.K = int(self.audio_rate / self.video_fps)

    def overlay_rgb(self, overlay_image, x, y):

        res = self.bg_image.copy()
        for i in range(3):
            res[y:(y+overlay_image.shape[0]), x:(x+overlay_image.shape[1]), i] += \
                (overlay_image[:, :, 3].astype(float) *
                 overlay_image[:, :, i].astype(float) / 255.0).astype(np.uint8)

        return cv2.cvtColor(res, cv2.COLOR_BGRA2RGB)

    def makeFrame(self, t):

        start = int(self.audio_rate * t)

        fig = plt.figure(figsize=(self.w_inch, self.h_inch))
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.margins(0)
        plt.plot(self.time[start:(start + self.K)],
                 self.voice[start:(start + self.K)], color='#ffffff32', linewidth=5)
        plt.ylim([-1, 1])
        fig.patch.set_alpha(0)

        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', transparent=True)
        io_buf.seek(0)
        rendered_graph = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                                    newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        plt.close(fig)

        return self.overlay_rgb(rendered_graph, 0, self.bg_height - 250)

    def saveVideo(self):

        clip = mvpy.VideoClip(self.makeFrame, duration=self.voice_length)
        clip.audio = mvpy.AudioFileClip(self.wav_filename)
        clip.write_videofile(self.output_filename, fps=self.video_fps)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('story_date')
    args = parser.parse_args()

    drawer = AudioSpectrumDrawer(args.story_date)
    drawer.saveVideo()
