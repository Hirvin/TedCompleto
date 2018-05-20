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
        self.len = 0
        self.words = []
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
        self.len = len(self.text)

        # esto podria estar obsoleto
        #self.words = self.text.split(' ')
        
    def get_end_time(self):
        return self.end_frame.time_milis

    def get_start_time(self):
        return self.start_frame.time_milis

    def __str__(self):
        num_txt = "num: %d\n" % self.num_frame
        start_txt = "start: " + str(self.start_frame) + "\n"
        end_txt = "end: " + str(self.end_frame) + "\n"
        text = self.text + "\n"
        show_text = self.show_text
        return num_txt + start_txt + end_txt + text + show_text


class Subtitle(object):
    """Subtitle class, contiene toda la info de los subtitulos"""
    def __init__(self):
        self.list_frames = []
        self.num_frames = 0
        self.frame_index = 0
        self.read_data_list = []

    def open_srt(self, txt_srt):
        """ carga el archivo srt en el buffer read_data_list """
        with open(txt_srt, 'r') as f_read:
            read_data = f_read.read()
            self.read_data_list = read_data.splitlines()
            self.read_data_list[0] = 1
            f_read.closed

    def get_frames(self):
        """lee el archivo str y lo convierte en frames"""
        while self.read_data_list:
            line = self.read_data_list.pop(0)
            if line == '':
                continue
            frame = SubFrame()
            frame.get_num_frame(line)
            frame.get_time_frame(self.read_data_list.pop(0))
            frame.get_text(self.read_data_list.pop(0))
            self.list_frames.append(frame)
            #print frame
        self.num_frames = len(self.list_frames)

    def set_srt_file(self, txt_srt):
        """ abre el archivo srt y lo convierte en frames """
        self.open_srt(txt_srt)
        self.get_frames()

    def next_frame(self):
        """ retorna next frame, retorno None si ya no hay mas frames """
        if self.frame_index < self.num_frames:
            frame = self.list_frames[self.frame_index]
            self.frame_index += 1
            return frame
        return None

    def prev_frame(self):
        """ retorna prev frame, retorna 0 en caso de ser el primero """
        index = self.frame_index - 2
        if index == -2:
            index = 0
        else:
            if index == -1:
                index = 1
            self.frame_index -= 1
        return self.list_frames[index]




class GFrame(object):
    """ estructura para pasar argumentos facilmente """
    def __init__(self):
        self.frame1 = None
        self.frame2 = None

class GameFrame(object):
    """ Controla todo lo relacionado con los subtitulos """
    def __init__(self):
        self.subtitle = Subtitle()
        self.g_frame = GFrame()
        #self.frame1 = None
        #self.frame2 = None

    def set_srt_file(self, txt_srt):
        """ carga el archivo srt y obtiene los primeros frames """
        self.subtitle.set_srt_file(txt_srt)
        self.g_frame.frame1 = self.subtitle.next_frame()
        self.g_frame.frame2 = self.subtitle.next_frame()

    def get_next(self):
        self.g_frame.frame1 = self.subtitle.next_frame()
        self.g_frame.frame2 = self.subtitle.next_frame()
        return self.g_frame

    def get_end_time(self):
        """ obtiene el tiempo final del GFrame """
        return self.g_frame.frame2.get_end_time()

    def get_start_time(self):
        """ obtiene el tiempo incial del Gframe """
        return self.g_frame.frame1.get_start_time()




