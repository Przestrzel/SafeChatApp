from enum import Enum


class Frame:

    def __init__(self, data, frame_type, file_name=''):
        self.data = data
        self.file_name = file_name
        self.frame_type = frame_type


class FrameType(Enum):
    TEXT = 1
    FILE = 2
    SIZE = 3
