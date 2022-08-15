import sys,pyttsx3
from PyQt5.QtWidgets import QApplication,QMainWindow
from texttovoice import Ui_MainWindow
from ChooseLocation import *
import speech_recognition as sr
from check import Dict

class Speech:
    def __init__(self):
        self.converter = pyttsx3.init()
    def Dowload(self,text,Name):
        self.converter.save_to_file(text,Name+'.mp3')
        self.converter.runAndWait()
    def Rate(self,num):
        self.converter.setProperty('rate', num * 10 + 100)
    def Volume(self,num):
        self.converter.setProperty('volume', num / 10)
    def NumVoice(self):
        voices = self.converter.getProperty('voices')
        return len(voices)
    def Voice(self):
        data=[]
        voices = self.converter.getProperty('voices')
        for voice in voices:
            data.append(voice.name)
        return data

    def ChangeVoice(self,num):
        voices = self.converter.getProperty('voices')
        self.converter.setProperty('voice', voices[num].id)

    def Say(self,text):
        self.converter.say(text)
        self.converter.runAndWait()
S=Speech()
class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.LanguageSpeak=''
        self.uic.BOpenFolder.clicked.connect(self.OpenFolder)
        self.uic.BSetting.clicked.connect(self.OpenSetting)
        self.uic.BSave.clicked.connect(self.Save)
        self.uic.Voice.addItems(S.Voice())
        self.uic.BOK.clicked.connect(self.Speak)
        self.uic.BDowload.clicked.connect(self.Dowload)
        self.uic.FrameDowload.hide()
        self.uic.FrameChooseLanguage.hide()
        self.uic.BDowload2.clicked.connect(self.StartDowload)
        self.uic.BMic.clicked.connect(self.Listen)
        self.uic.BSettingLanguage.clicked.connect(self.ChooseLanguage)
        self.RunOldData()
        self.Language=[]
        self.Country=[]
        for value in Dict.keys():
            self.Language.append(value)
        self.uic.Language.addItems(self.Language)

    def ChooseLanguage(self):
        self.uic.FrameChooseLanguage.show()
        self.uic.BOK_Language.clicked.connect(self.ChooseCountry)

    def ChooseCountry(self):
        self.Country.clear()
        self.uic.Country.clear()
        data=self.uic.Language.currentText()
        for value in Dict[data].keys():
            self.Country.append(value)
        self.uic.Country.addItems(self.Country)
        self.uic.BOK_2.clicked.connect(self.SetLanguage)
    def SetLanguage(self):
        self.uic.FrameChooseLanguage.hide()
        L=self.uic.Language.currentText()
        C=self.uic.Country.currentText()
        key=Dict[L][C]
        self.LanguageSpeak=key
    def Listen(self):
        self.Get(self.LanguageSpeak)
    def Get(self,lang):
        recognizer = sr.Recognizer()

        ''' recording the sound '''

        with sr.Microphone() as source:
            print("Adjusting noise ")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 4 seconds")
            recorded_audio = recognizer.listen(source, timeout=4)
            print("Done recording")

        ''' Recorgnizing the Audio '''
        try:
            print("Recognizing the text")
            text = recognizer.recognize_google(
                recorded_audio,
                language=lang
            )
            print("Decoded Text : {}".format(text))
            self.uic.Edit.setText(text)

        except Exception as ex:
            print(ex)

    def RunOldData(self):
        file=open('Data.txt','r')
        data=file.read().split('|')
        self.uic.Volume.setValue(int(data[0]))
        self.uic.Rate.setValue(int(data[1]))
        i=S.Voice().index(data[2])
        self.uic.Voice.setCurrentIndex(i)
        S.ChangeVoice(i)

    def Dowload(self):
        self.uic.FrameDowload.show()

    def StartDowload(self):
        name=self.uic.Name.text()
        data = self.uic.Edit.toPlainText()
        S.Dowload(data, name)

    def Speak(self):
        data=self.uic.Edit.toPlainText()
        S.Say(data)

    def Save(self):
        self.uic.FrameMain.show()
        volume=self.uic.Volume.value()
        rate=self.uic.Rate.value()
        voice=self.uic.Voice.currentText()
        file=open('Data.txt','w')
        file.write(str(volume)+"|"+str(rate)+"|"+str(voice))
        S.Volume(volume)
        S.Rate(rate)
        num=S.Voice().index(voice)
        S.ChangeVoice(num)



    def OpenSetting(self):
        self.uic.FrameMain.hide()
        self.uic.FrameControll.show()

    def OpenFolder(self):
        A = App()
        A.show()
        file=open('Path.txt','r')
        data=file.read()
        file.close()
        file=open(data,'r')
        self.uic.Edit.setText(file.read())


    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())