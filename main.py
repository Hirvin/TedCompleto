# PyQt5 Video player
#!/usr/bin/env python
# installar sudo apt-get install qtmultimedia5-examples


 
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys

# Constantes del sistema
_PATH_VIDEO = "/home/uidk4253/Documents/Hirvin/Projectos/Ted/video2.mp4"

class VideoPlayer(object):
    """VideoPlayer, defines all methods for video player"""
    def __init__(self):
        #video elements
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        # slider elements
        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setRange(0, 0)
        # layout
        self.video_layout = QVBoxLayout()
        self.video_layout.addWidget(self.video_widget)
        self.video_layout.addWidget(self.video_slider)
        # signals
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.error.connect(self.video_handle_error)
        self.video_slider.sliderMoved.connect(self.set_new_video_position)

    def video_handle_error(self):
        #self.playButton.setEnabled(False)
        print "Error Video: " + self.media_player.errorString()

    def set_new_video_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        #if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        #    if position > 10000:
        #        print position
        #        self.mediaPlayer.pause()
        self.video_slider.setValue(position)

    def duration_changed(self, duration):
        self.video_slider.setRange(0, duration)

    def set_video_file(self, video_path):
        """set de video and start to play it"""
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.play()

class VideoWindow(QMainWindow):
 
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
        
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