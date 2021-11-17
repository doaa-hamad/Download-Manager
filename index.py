import sys
#  pyuic5.bat .\main.ui -o main.py                      font: 63 8pt "Yu Gothic UI Semibold";
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType  # To Handle Life With Designer in Qt Program
import urllib.request
import re
import requests

import os
from os import path  # To Handle With Path in Windows
import sys  # ss = system
import pafy  # For Download From Youtube
import humanize
from pytube import Playlist

FROM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # import ui file ,,, "FROM_CLASS, _" Mmust


# Write It As This Shape ,,, "__file__"  To Get THe Python File , { join(path.dirname(__file__), "main.ui") } To Join
# both python File and Designer File


############ Initiate ui file ################
class mainapp(QMainWindow, FROM_CLASS):  # Here Create Class By QMainWindow Which Exist in FROM_CLASS File "main.ui"
    # ,, QMainWindow because the applicate create it by main window in Qt Designer
    def __init__(self, parent=None):
        super(mainapp, self).__init__(parent)
        QMainWindow.__init__(self)  # QMainWindow Start to work
        self.setupUi(self)
        self.Handle_Design()
        self.Handle_Buttons()
        #  self.Handle_Progress()

    def Handle_Design(self):  # To Handle With Design Self
        self.setWindowTitle("SnapTube")
        self.setFixedSize(570, 311)

    def Handle_Buttons(self):  # To Connect every Button in App With it Function Which Special it(Handle With any
        # Button in App)
        self.pushButton.clicked.connect(self.get_save_Browse)
        self.pushButton_2.clicked.connect(self.Handle_Download)

        self.pushButton_5.clicked.connect(self.get_Youtube_video)  # *
        self.pushButton_3.clicked.connect(self.get_save_Browse)
        self.pushButton_4.clicked.connect(self.Download_Youtube_video)

        self.pushButton_7.clicked.connect(self.Download_playlist)
        self.pushButton_6.clicked.connect(self.get_save_Browse)


    def Handle_Browse(self):  # To Handle With any Browse Button(Special)

        # caption: Name of Dialog(Window Specialize Save as),,, directory Equal "." To Open Basic partition,,,,
        # filter Equals (*.*) To Accept Any FileName With extension
        save_Place = QFileDialog.getSaveFileName(self, caption="Sava As", directory=".", filter="All Files(*.*)")
        # print(type(save_Place)) # Tuple
        text = str(save_Place)  # Convert Tpo Str To Can Make Slicing For it To Print It In lineEdit_3 (Which Specialize
        # save_place)
        name = text[2:].split(",")[0].replace("'", "")  # Slicing For Path File To Get it Without "(" and ... etc
        self.lineEdit_3.setText(name)

    # Every Part In SizeFile called Block ,,, Example: FileSize=100MD We divide To Blocks ,, Every Block Have size 10
    # So Will Be Have Blocknum = 10 and blocksize=10 Because 10+ 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 = 100MB

    def get_save_Browse(self):
        save = QFileDialog.getExistingDirectory(self,
                                                "Select Download Directory")  # Download The Video With it Name Without I specific Name & File To Get Place Which I Choose it(Specific)
        self.lineEdit_3.setText(save)
        self.lineEdit_4.setText(save)
        self.lineEdit_6.setText(save)
        QApplication.processEvents()

    # ============================================= Download Any File ======================================================

    def Handle_Progress_Files(self, blocknum, blocksize,
                              totalsize):  # This Function Return Information To Can Handle With progress bar
        read = blocknum * blocksize
        if totalsize > 0:
            precent = read * 100 / totalsize
            self.progressBar.setValue(precent)
            QApplication.processEvents()  # To Avoid "Not Responding" [ but This partial solution ^_^ ]

    def Handle_Download(self):  # To Handle With Download Operation
        #  lineEdit,lineEdit_3 That ObjectName in Qt Designer
        url = self.lineEdit.text()  # To Get Text in lineEdit
        save_location = self.lineEdit_3.text()  # To Get Text in lineEdit
        #  print(f"That URL :{url}, save location :{save_location}")
        if url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                # To Download Video :
                urllib.request.urlretrieve(url, save_location,
                                           self.Handle_Progress_Files)  # To Give Me Information About Size of Video
                QMessageBox.information(self, "Download Finished", "Uploaded successfully *_^")  # QMessageBox(self,

            except Exception:
                QMessageBox.warning(self, "Error Download",
                                    "Download Failed")  # in [ QMessageBox.warning ] THe letter "i' it Not Capital To Avoid Error
                return
        # in [ QMessageBox.information ] THe letter "i' it Not Capital To Avoid Error
        # TitleMessage,
        # ContentMessage)# First parameter = self Because This
        # Message Appear in QMainWindow Class

        self.progressBar.setValue(0)
        self.lineEdit.setText("")
        self.lineEdit_3.setText("")

    # ============================================= Download Single Video ==================================================

    def get_Youtube_video(self):
        try:
            video_link = self.lineEdit_2.text()  # Get The Link Of Video
            v = pafy.new(video_link)
            # print(v.title)
            # print(v.duration)
            # print(v.rating)
            # print(v.author)
            # print(v.length)
            #  print(v.keywords) # This Video Not Have Keywords So Will Be Error ,,, Cause Stopped Program
            # print(v.thumb)
            # print(v.videoid)
            # print(v.viewcount)
            available_Qualities = v.allstreams
            # print(v.allstreams)  # Print Available Qualities To Download Video
            for stream in available_Qualities:
                file_size = humanize.naturalsize(stream.get_filesize())  # To Convert The Size Of Vide From B To MB
                data = f"{stream.mediatype}  {stream.extension}  {stream.quality}  {file_size}"  # Convert To String TO Accept AS Parameter In [ addItem() ] Because Not Accept Tuble
                self.comboBox.addItem(data)
                QApplication.processEvents()  # Because The Program Not responding while print Qualities,,, The problem has been resolved *_^
                # * Notice : Will Print File Size in Bit So Will Convert To MB
        except:
            QMessageBox.information(self, "Error Download", "Enter an available YouTube video link")

    def Download_Youtube_video(self):
        link_video = self.lineEdit_2.text()
        save_Location = self.lineEdit_4.text()

        if link_video == '' or save_Location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")
        else:
            video = pafy.new(link_video)  # To Get Video By it Link
            available_Qualities = video.allstreams  # List of Available Qualities
            Quality = self.comboBox.currentIndex()
            QApplication.processEvents()
            #  print(Quality) # Will Print Index For Quality Which I Choose it fom List[ available_Qualities ]
            download_video = available_Qualities[Quality].download(filepath=save_Location, callback=self.Video_Progress)
            QApplication.processEvents()
            QMessageBox.information(self, "Download Finished", "The Video Download Finished ^_^")  # QMessageBox(self,
            QApplication.processEvents()

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            QApplication.processEvents()
            remaining_time = round(time / 60, 2)
            self.label_10.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    # ============================================= Download playlist ==================================================

    def Download_playlist(self):
        playlist_URL = self.lineEdit_5.text()
        # print("playlist URL: ",playlist_URL)
        save_Location = self.lineEdit_6.text()
        # print("save Location : ",save_Location)

        if playlist_URL == '' or save_Location == '':  # if User Not Enter URL playlist or save location
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = Playlist(playlist_URL)
            # playlist = pafy.get_playlist(playlist_URL)  # To Get playlist From YouTube
            # playlist_videos = playlist['items']  # To Get All Videos IN playlist in list Called videos
            playlist_videos = playlist.videos
            self.lcdNumber.display(len(playlist))  # To set number of Videos in Playlist in lcdNumber

        os.chdir(save_Location)  # Enter To Save location
        titlePlaylist = str(playlist_videos[0].title).split(" ")[0]
        if os.path.exists(
                titlePlaylist):  # check whether the given path refers to an open file descriptor or not & used to check whether the specified path exists or not
            os.chdir(titlePlaylist)  # To Enter Folder

        else:
            os.mkdir(
                titlePlaylist)  # Create Folder (To Download Playlist inside it) ,, as name playlist Inside save Location
            os.chdir(titlePlaylist)  # To Enter Folder Special Playlist Videos
        current_video_in_download = 1
        QApplication.processEvents()
        for video in playlist_videos:
            video_down = pafy.new(video)  # To Get Information About Video
            best_Quality = video_down.getbest(preftype='mp4')  # To Get Best Quality for video in Type mp4
            self.lcdNumber_2.display(current_video_in_download)
            download = best_Quality.download()
            QApplication.processEvents()

            current_video_in_download += 1







def main():
    app = QApplication(sys.argv)
    window = mainapp()  # Object From main App Class
    window.show()
    app.exec_()  # To Draw The Program On Screen


if __name__ == '__main__':
    main()
