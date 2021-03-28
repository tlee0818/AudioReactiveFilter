Welcome to Audio-Reactive Filter!

Run programFile.py

The program is straightforward with instructions on each screen. However, there are things to be careful.

1. Make sure path of ffmpeg is correct. This program uses ffmpeg and texture.jpg in a specific location. If you don’t know where your ffmpeg is, try “which ffmpeg” on your terminal.

data.ffmpeg and texture.jpg is in the init(data) function for you to modify

2. Use square images please! After all, it is for instagram.

3. make sure to download any library you current do not have.
#audio-related imports
from pydub import AudioSegment
import soundfile as sf
from aubio import source, tempo
import numpy as np
from numpy import median, diff
import wave
import pyaudio

#image-related imports
import cv2
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import PIL
from PIL import Image
import pylab

#others
import random
import os
import threading
import sys
import subprocess
import argparse
import time
import shutil

4. Have fun making videos for your instagram!



