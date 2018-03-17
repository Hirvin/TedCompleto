import re

_FRAME_TIMES = r"([\d\:\,]+)[\>\-\s]+([\d\:\,]+)"
_SPLIT_TIME = r"(\d+):(\d+):(\d+)\,(\d+)"
_SHOW_TEXT = r"[a-zA-Z0-9]"

class SubFrameTime(object):
    """SubFrameTime, contiene informacion del tiempo de un sub frame"""
    def __init__(self):
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.mil = 0
        self.time_milis = 0

    def set_time(self, data):
        """ set time from data"""
        split_time = re.match(_SPLIT_TIME, data).groups()
        self.hour = int(split_time[0])
        self.min = int(split_time[1])
        self.sec = int(split_time[2])
        self.mil = int(split_time[3])
        self.time_milis = self.mil + (self.sec * 1000)
        self.time_milis += self.min * 60 * 1000
        self.time_milis += self.hour * 60 * 60 * 1000

    def __str__(self):
        txt = "%d:%d:%d.%d => %d" %(self.hour, self.min, self.sec, self.mil, self.time_milis)
        return txt



class SubFrame(object):
    """SubFrame, contiene la info de un solo frame"""
    def __init__(self):
        self.num_frame = 0
        self.start_frame = SubFrameTime()
        self.end_frame = SubFrameTime()
        self.text = ""
        self.show_text = "" # hay que eliminarlo 

    def get_num_frame(self, data):
        """obtiene el numero de frame"""
        self.num_frame = int(data)

    def get_time_frame(self, data):
        """obtiene los tiempos del frame"""
        frame_times = re.match(_FRAME_TIMES, data).groups()
        self.start_frame.set_time(frame_times[0])
        self.end_frame.set_time(frame_times[1])

    def get_text(self, data):
        self.text = data
        if data[0] != '(':
            self.show_text = re.sub(_SHOW_TEXT, "*", self.text)

    def __str__(self):
        num_txt = "num: %d\n" % self.num_frame
        start_txt = "start: " + str(self.start_frame) + "\n"
        end_txt = "end: " + str(self.end_frame) + "\n"
        text = self.text + "\n"
        show_text = self.show_text
        return num_txt + start_txt + end_txt + text + show_text


class Subtitle(object):
    """Subtitle class, contiene toda la info de los subtitulos"""
    def __init__(self, txt_sub):
        self.list_frames = []
        with open(txt_sub, 'r') as f_read:
            read_data = f_read.read()
            self.read_data_list = read_data.splitlines()
            self.read_data_list[0] = 1
            f_read.closed

    def get_frames(self):
        """Imprime los errores relaciones con el video player"""
        while self.read_data_list:
            line = self.read_data_list.pop(0)
            if line == '':
                continue
            frame = SubFrame()
            frame.get_num_frame(line)
            frame.get_time_frame(self.read_data_list.pop(0))
            frame.get_text(self.read_data_list.pop(0))
            self.list_frames.append(frame)
            print frame


subtitle = Subtitle("sub.srt")
subtitle.get_frames()


