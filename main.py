# PyQt5 Video player
#!/usr/bin/env python
# installar sudo apt-get install qtmultimedia5-examples

# Todo - change video stop to pause

 
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
from subtitle import GameFrame

# Constantes del sistema
_PATH_VIDEO = "/home/uidk4253/Documents/Hirvin/Projectos/Ted/video.mp4"
_PATH_SRT = "sub.srt"
_SPACE_BT_WORD = 4
_NUM_WORD_BY_SUB = 18

# variables de ambiente para la applicacion
_EXTRA_BUFFER = 500

class LbWord(object):
    """ controla todo lo relacionado con una palabra """
    def __init__(self):
        self.label = QLabel()
        self.cnt_letter = 2
        self.cnt_word = 3
        self.word = ''
        #self.label.hide()
        self.label.setText("X")

    def set_word(self, word):
        """setea la palabra"""
        self.word = word
        self.label.setText(word)
        self.label.update()

class SubView(object):
    """ todo lo necesario para controlar la vista subtitle """
    def __init__(self):
        self.lb_list = []
        self.layout = QHBoxLayout()
        self.layout.setSpacing(_SPACE_BT_WORD)
        # inicializaciones
        self.create_labels()
        self.set_layout()

    def create_labels(self):
        """ crea las 20 palabra por subtitulo"""
        for i_index in range(_NUM_WORD_BY_SUB):
            self.lb_list.append(LbWord())

    def set_layout(self):
        """set the layout with all the labels"""
        self.layout.addStretch()
        for i_index in range(_NUM_WORD_BY_SUB):
            self.layout.addWidget(self.lb_list[i_index].label)
        self.layout.addStretch()

    def set_frame(self, frame):
        if len(frame.words) >= _NUM_WORD_BY_SUB:
            print "Error: se necesitan mas palabras %d" %(len(frame.words))
            return False

        num_words = len(frame.words)

        for index, word in enumerate(frame.words):
            self.lb_list[index].set_word(word)

        for index in range(_NUM_WORD_BY_SUB - num_words):
            self.lb_list[num_words + index].set_word(" ")

        #self.layout.update()
        #self.label.setText(frame.text)
        return True

class SubPanel(object):
    """visualiza los subtitulos"""
    def __init__(self):
        self.layout = QVBoxLayout()
        self.sub1_v = SubView()
        self.sub2_v = SubView()

        #configurando el panel
        self.layout.addLayout(self.sub1_v.layout)
        self.layout.addLayout(self.sub2_v.layout)

    def set_frame(self, g_frame):
        """ set frame """
        self.sub1_v.set_frame(g_frame.frame1)
        self.sub2_v.set_frame(g_frame.frame2)

class PrevButton(object):
    """ controla el funcionamiento de los botones"""
    def __init__(self):
        self.button = QPushButton("Prev")
        self.first_frame = True
        self.button.setEnabled(False)
        self.button.setMaximumSize(60, 200)

    def enable(self):
        if self.first_frame == True:
            self.button.setEnabled(True)
            self.first_frame = False

class NextButton(object):
    """ controla el funcionamiento dl button next """
    def __init__(self):
        self.button = QPushButton("Next")
        self.button.setEnabled(False)
        self.last_frame = False
        self.button.setMaximumSize(60, 200)

    def enable_first_frame(self):
        print "entra aqui"
        self.button.setEnabled(True)

class VideoPlayerControl(object):
    """ despliega botones Next, Prev and subtitles"""
    def __init__(self):
        self.ctrl_lay = QHBoxLayout()
        self.prev_button = PrevButton()
        self.next_button = NextButton()


        self.sub_panel = SubPanel()

        # creando la estrurua del box
        self.ctrl_lay.addWidget(self.prev_button.button)
        #Hirvin
        self.ctrl_lay.addLayout(self.sub_panel.layout)
        self.ctrl_lay.addWidget(self.next_button.button)

        #Configuraciones 
        #self.prev_button.setMaximumSize(60, 200)
        #self.next_button.setMaximumSize(60, 200)

    def set_subtitle_view(self, g_frame):
        """ set frame """
        #hirvin
        self.sub_panel.set_frame(g_frame)
        pass

class VideoPlayer(object):
    """VideoPlayer, defines all methods for video player"""
    def __init__(self):
        # flags
        self.frame_time_start = 0
        self.frame_time_end = 0
        #video elements
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.video_control = VideoPlayerControl()

        # subtitle elements
        #self.subtitle_frames = Subtitle()
        self.game_frame = GameFrame()

        # slider elements
        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setRange(0, 0)
        # Video layout
        self.video_layout = QVBoxLayout()
        self.video_layout.addWidget(self.video_widget)
        self.video_layout.addWidget(self.video_slider)
        self.video_layout.addLayout(self.video_control.ctrl_lay)
        # signals
        self.media_player.positionChanged.connect(self.duration_scheduler)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.error.connect(self.video_handle_error)
        self.video_control.next_button.button.clicked.connect(self.next_clicked)
 
        #self.video_slider.sliderMoved.connect(self.set_new_video_position)

    def play(self):
        self.media_player.setPosition(self.frame_time_start)
        self.media_player.play()

    def video_handle_error(self):
        """Imprime los errores relaciones con el video player"""
        #self.playButton.setEnabled(False)
        print "Error Video: " + self.media_player.errorString()

    def set_new_video_position(self, position):
        """actualiza la posicion del video cuando el slider cambia"""
        self.media_player.setPosition(position)

    def position_changed(self, position):
        """sincroniza la posicion del slider con la del video"""
        self.video_slider.setValue(position)

    def duration_scheduler(self, position):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            if position > self.frame_time_end:
                print position
                # chage this for pause()
                self.media_player.stop()
                self.video_control.prev_button2.enable()
                self.video_control.next_button2.enable_first_frame()


    def duration_changed(self, duration):
        """actualiza el rango del slider con cada nuevo video"""
        self.video_slider.setRange(0, duration)

    def set_video_file(self, video_path):
        """set de video and start to play it"""
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.game_frame.set_srt_file(_PATH_SRT)
        self.frame_time_start = 0
        self.frame_time_end = self.game_frame.get_end_time()
        self.video_control.set_subtitle_view(self.game_frame.g_frame)
        self.media_player.play()

    def next_clicked(self):
        """ next button presionado """
        print "next fue precionado"
        self.video_control.next_button2.button.setText("Hola")
        g_frame = self.game_frame.get_next()
        self.frame_time_start = self.game_frame.get_start_time() 
        self.frame_time_end = self.game_frame.get_end_time() + _EXTRA_BUFFER
        print "start: %d end: %d" % (self.frame_time_start, self.frame_time_end)
        self.video_control.set_subtitle_view(g_frame)
        self.play()

class VideoWindow(QMainWindow):
    """Ventana Principal del Programa"""
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyTedict")
        #self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #videoWidget = QVideoWidget()
        self.video_player = VideoPlayer()
 
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_button)
 
 
        self.errorLabel = QLabel()
        self.errorLabel.setText("Este es el ejemplo de una etiqueta")
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
 
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
 
        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
 
        layout = QVBoxLayout()
        layout.addLayout(self.video_player.video_layout)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
 
        # Set widget to contain window contents
        wid.setLayout(layout)
 
        # conectando la senales
        ## Recordar #######################################3
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

        # incializando el video de forma automatica
        self.video_player.set_video_file(_PATH_VIDEO)
        #hasta aqui agregar
 
    # salida de la applicacion
    def exitCall(self):
        sys.exit(app.exec_())
        
    def play_button(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())