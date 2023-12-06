#!/usr/bin/env python3

import pyds
import time
from gi.repository import GLib, Gst
import sys
import gi
gi.require_version('Gst', '1.0')


Gst.init(None)
player = Gst.Pipeline.new("player")
print("Pipeline created")

v4l2Source = Gst.ElementFactory.make("v4l2src", "v4l2Source")
v4l2Source.set_property("device", "/dev/video0")
print("USB cam source created")

caps = Gst.Caps.from_string("video/x-raw")
filter = Gst.ElementFactory.make("capsfilter", "filter")
filter.set_property("caps", caps)

videoconvert = Gst.ElementFactory.make("videoconvert", "converter")

encoder = Gst.ElementFactory.make("x264enc", "venc")

parser = Gst.ElementFactory.make("h264parse", "parser")
parser.set_property("config-interval", 3)

muxer = Gst.ElementFactory.make("mp4mux", "muxer")

filesink = Gst.ElementFactory.make("filesink", "sinker")
filesink.set_property("location", "pvideo.mp4")

print("All elements created")

i = 0
for ele in [v4l2Source, filter, videoconvert, encoder, parser, muxer, filesink]:
    print(f"Element {i} added to the pipeline")
    player.add(ele)
    i += 1
print("All Elements added to the pipeline")
