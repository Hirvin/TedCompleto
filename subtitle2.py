
class sub_word(object):
    """ continene todo la estructura de cada palabra """
    def __init__(self):
        self.text = ""
        self.meaning = ""
        self.translate = ""

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def set_meaning(self, meaning):
        self.text = meaning

    def set_translate(self, translate):
        self.translate = translate



class SubBuffer(object):
    """ contine el buffer de datos del subtitle"""
    def __init__(self, txt_srt):
        with open(txt_srt, 'r') as f_read:
            read_data = f_read.read()
            self.buffer = read_data.replace("\n", " ").split(" ")
            self.buffer[0] = 1
            f_read.closed

    def get_word(self):
        if self.buffer != []:
            return self.buffer.pop(0)
        else:
            print "Buffer vacio"
            return None

    def is_empty(self):
        if self.buffer != []:
            return True
        else:
            return False

    def get_len(self):
        return len(self.buffer)

    def has_head(self):
        return self.get_len() > 3

    def is_end_frame(self):
        if self.buffer[0] == "":
            self.buffer.pop(0)
            return True
        else:
            return False

class Frame(object):
    """ contiene la estructura de un frame de subtitulo"""
    def __init__(self):
        self.number = None
        self.init_time = None
        self.end_time = None
        self.words = []

    def set_number(self, number):
        self.number = number

    def set_init_time(self, initTime):
        self.init_time = initTime

    def set_end_time(self, endTime):
        self.end_time = endTime

    def set_word(self, word):
        self.words.append(word)

    def set_head(self, buffer):
        if buffer.has_head():
            self.set_number(buffer.get_word())
            self.set_init_time(buffer.get_word())
            buffer.get_word()
            self.set_end_time(buffer.get_word())
            self.clean()
            return True
        else:
            return False

    def get_frame(self, buffer):
        if self.set_head(buffer):
            while buffer.is_end_frame() == False:
                self.set_word(buffer.get_word())
            return True
        else:
            return False

    def clean(self):
        self.words = []

    def __str__(self):
        number_txt = "number = " + str(self.number)
        init_txt = "init time: " + str(self.init_time)
        end_txt = "end time: " + str(self.end_time)
        words_txt = str(self.words)
        next_txt = " ******************* \n"
        return number_txt + '\n' + init_txt + '\n' + end_txt + '\n' + words_txt + '\n' + next_txt

class Subtiltle(object):
    """ continene toda la estrutura para leer los subtitulos """
    def __init__(self):
        self.l_frames = []
        pass

    def open_srt(self, txt_srt):
        """ carga el archivo srt en el buffer read_data_list """
        self.buffer = SubBuffer(txt_srt)

    def get_frames(self, buffer):
        while self.buffer.is_empty():
            self.l_frames.append(Frame())
            if self.l_frames[-1].get_frame(self.buffer) == False:
                self.l_frames.pop(-1)
                return True
        return True

    def set_subtitles(self, txt_srt):
        self.open_srt(txt_srt)
        self.get_frames(self.buffer)

    def print_frames(self):
        for e in self.l_frames:
            print e



sub = Subtiltle()
sub.set_subtitles("sub.srt")
sub.print_frames()