import sys,os,datetime,subprocess,random,pathlib,time
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import *

from win32 import win32api
from win32 import win32process
from win32 import win32gui

def callback(hwnd, pid):
  if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
    # hide window
    win32gui.ShowWindow(hwnd, 0)

# find hwnd of parent process, which is the cmd.exe window
win32gui.EnumWindows(callback, os.getppid())

def callback2(hwnd, pid):
  if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
    # hide window
    win32gui.ShowWindow(hwnd, 1)
	
class Goofys_Video_Splitter(QThread):

    signal = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)
        self.inputvideo = ""
        self.starttime= ""
        self.endtime= ""
        self.fileext= ""
        self.installffmpeg= ""
        self.checked= ""

    def run(self):
        addanumber=random.randint(1,1000000)
        if self.checked:
            ffmpegstring="ffmpeg -i " + '"' + self.inputvideo + '"' +" -ss " + self.starttime + " -to " + self.endtime + " -c:v libx264 -c:a aac -strict experimental -b:a 128k " + "converted"+str(addanumber)+".mp4"
        else:
            ffmpegstring="ffmpeg -i " + '"' + self.inputvideo + '"' +" -ss " + self.starttime + " -to " + self.endtime + " -vcodec copy -acodec copy " + "converted"+str(addanumber)+"."+self.fileext
        #this command simply trims the video preserving the original video encoding
        #ffmpeg -i "2019-09-21 18-03-58.flv" -ss 00:01:00.000 -t 00:01:10.000 -vcodec copy -acodec copy test.flv
        #the command below reencodes the video
        #p=subprocess.call("ffmpeg -loglevel quiet -i " + '"' + self.inputvideo + '"' +" -ss " + self.starttime + " -to " + self.endtime + " -c:v libx264 -c:a aac -strict experimental -b:a 128k " + "converted"+str(addanumber)+".mp4", shell=False)
        #p=subprocess.call("ffmpeg -i " + '"' + self.inputvideo + '"' +" -ss " + self.starttime + " -to " + self.endtime + " -vcodec copy -acodec copy " + "converted"+str(addanumber)+"."+self.fileext, shell=False)
        p = subprocess.Popen(ffmpegstring, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print (line.rstrip().decode("utf-8"))
            self.signal.emit(line.rstrip().decode("utf-8"))
            if line == b'':
                break
        if self.checked:
            self.signal.emit("DONE! Your output video name is: "+"converted"+str(addanumber)+".mp4")
        else:
            self.signal.emit("DONE! Your output video name is: "+"converted"+str(addanumber)+"."+self.fileext)

class Install_FFMPEG(QThread):

    signal = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)
        self.psc1 = "powershell Invoke-WebRequest -Uri 'https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.2/ffmpeg-4.2-win-32.zip' -OutFile 'c:\\users\\public\\ffmpeg.zip'"
        self.psc2= "powershell expand-archive -path 'c:\\users\\public\\ffmpeg.zip' -destinationpath 'c:\\users\\%username%\\ffmpeg\'"
        self.rgc= 'reg add HKCU\Environment /v PATH /d "%PATH%;c:\\users\\%USERNAME%\\ffmpeg " /f'


    def run(self):
        self.signal.emit("FFMPEG, the tool we use to split videos, is not installed.  I'll install it for you and then this tool will close and restart your windows explorer process so changes take effect.  if you wish to close out before installation begins and save your opened programs, you have 10 seconds to do so before the script begins.")
        time.sleep(10)
        self.signal.emit("OK.  downloading FFMPEG now...")
        p = subprocess.Popen(self.psc1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print (line.rstrip().decode("utf-8"))
            self.signal.emit(line.rstrip().decode("utf-8"))
            if line == b'':
                break
        self.signal.emit("extracting FFMPEG...")
        p = subprocess.Popen(self.psc2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print (line.rstrip().decode("utf-8"))
            self.signal.emit(line.rstrip().decode("utf-8"))
            if line == b'':
                break
        self.signal.emit("Adding FFMPEG to the user %PATH% variable...")
        p = subprocess.Popen(self.rgc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print (line.rstrip().decode("utf-8"))
            self.signal.emit(line.rstrip().decode("utf-8"))
            if line == b'':
                break
        self.signal.emit("Installation of FFMPEG is complete!  closing program and logging off in 3 seconds.")
        time.sleep(3)
        logoffcmd="shutdown -l -f"
        p = subprocess.Popen(logoffcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(482, 357)
        Form.setMinimumSize(QtCore.QSize(482, 357))
        Form.setMaximumSize(QtCore.QSize(482, 357))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Pictures/East_bound_and_down_112.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(15.0)
        Form.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 270, 161, 81))
        self.pushButton.setStyleSheet("font: 11pt \"Segoe Script\";")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 451, 31))
        self.textEdit.setTabChangesFocus(True)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 461, 16))
        self.label.setStyleSheet("font: 14pt \"Segoe Script\";")
        self.label.setObjectName("label")
        self.startHour = QtWidgets.QTextEdit(Form)
        self.startHour.setGeometry(QtCore.QRect(10, 150, 41, 31))
        self.startHour.setTabChangesFocus(True)
        self.startHour.setObjectName("startHour")
        self.startMin = QtWidgets.QTextEdit(Form)
        self.startMin.setGeometry(QtCore.QRect(60, 150, 41, 31))
        self.startMin.setTabChangesFocus(True)
        self.startMin.setObjectName("startMin")
        self.startSec = QtWidgets.QTextEdit(Form)
        self.startSec.setGeometry(QtCore.QRect(110, 150, 41, 31))
        self.startSec.setTabChangesFocus(True)
        self.startSec.setObjectName("startSec")
        self.endHour = QtWidgets.QTextEdit(Form)
        self.endHour.setGeometry(QtCore.QRect(270, 150, 41, 31))
        self.endHour.setTabChangesFocus(True)
        self.endHour.setObjectName("endHour")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 51, 16))
        self.label_2.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(160, 160, 20, 21))
        self.label_3.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(70, 130, 31, 16))
        self.label_4.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(50, 150, 16, 21))
        self.label_5.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(100, 150, 16, 21))
        self.label_6.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(120, 130, 31, 16))
        self.label_7.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(170, 130, 41, 16))
        self.label_8.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_8.setObjectName("label_8")
        self.startMilli = QtWidgets.QTextEdit(Form)
        self.startMilli.setGeometry(QtCore.QRect(170, 150, 41, 31))
        self.startMilli.setTabChangesFocus(True)
        self.startMilli.setObjectName("startMilli")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(420, 160, 20, 21))
        self.label_9.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(310, 150, 16, 21))
        self.label_10.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(360, 150, 16, 21))
        self.label_11.setStyleSheet("font: 26pt \"Segoe Script\";")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(380, 130, 31, 16))
        self.label_12.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_12.setObjectName("label_12")
        self.endMin = QtWidgets.QTextEdit(Form)
        self.endMin.setGeometry(QtCore.QRect(320, 150, 41, 31))
        self.endMin.setTabChangesFocus(True)
        self.endMin.setObjectName("endMin")
        self.endSec = QtWidgets.QTextEdit(Form)
        self.endSec.setGeometry(QtCore.QRect(370, 150, 41, 31))
        self.endSec.setTabChangesFocus(True)
        self.endSec.setObjectName("endSec")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(270, 130, 51, 16))
        self.label_13.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(330, 130, 31, 16))
        self.label_14.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_14.setObjectName("label_14")
        self.endMilli = QtWidgets.QTextEdit(Form)
        self.endMilli.setGeometry(QtCore.QRect(430, 150, 41, 31))
        self.endMilli.setTabChangesFocus(True)
        self.endMilli.setObjectName("endMilli")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(430, 130, 41, 16))
        self.label_15.setStyleSheet("font: 10pt \"Segoe Script\";")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(40, 100, 141, 16))
        self.label_16.setStyleSheet("font: 14pt \"Segoe Script\";")
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(310, 100, 141, 16))
        self.label_17.setStyleSheet("font: 14pt \"Segoe Script\";")
        self.label_17.setObjectName("label_17")
        self.status = QtWidgets.QTextEdit(Form)
        self.status.setGeometry(QtCore.QRect(190, 190, 281, 161))
        self.status.setReadOnly(True)
        self.status.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.status.setObjectName("status")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(10, 240, 161, 17))
        self.checkBox.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 210, 171, 17))
        self.checkBox_2.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.checkBox_2.setObjectName("checkBox_2")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.textEdit, self.startHour)
        Form.setTabOrder(self.startHour, self.startMin)
        Form.setTabOrder(self.startMin, self.startSec)
        Form.setTabOrder(self.startSec, self.startMilli)
        Form.setTabOrder(self.startMilli, self.endHour)
        Form.setTabOrder(self.endHour, self.endMin)
        Form.setTabOrder(self.endMin, self.endSec)
        Form.setTabOrder(self.endSec, self.endMilli)
        Form.setTabOrder(self.endMilli, self.pushButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "GOOFY\'S VIDEO EDITOR"))
        self.pushButton.setText(_translate("Form", "EXECUTE IT!"))
        self.label.setText(_translate("Form", "DRAG YOUR VIDEO INTO THE BOX BELOW"))
        self.startHour.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00</p></body></html>"))
        self.endHour.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00</p></body></html>"))
        self.label_2.setText(_translate("Form", "HOUR"))
        self.label_3.setText(_translate("Form", "."))
        self.label_4.setText(_translate("Form", "MIN"))
        self.label_5.setText(_translate("Form", ":"))
        self.label_6.setText(_translate("Form", ":"))
        self.label_7.setText(_translate("Form", "SEC"))
        self.label_8.setText(_translate("Form", "MILLI"))
        self.startMilli.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">000</p></body></html>"))
        self.label_9.setText(_translate("Form", "."))
        self.label_10.setText(_translate("Form", ":"))
        self.label_11.setText(_translate("Form", ":"))
        self.label_12.setText(_translate("Form", "SEC"))
        self.label_13.setText(_translate("Form", "HOUR"))
        self.label_14.setText(_translate("Form", "MIN"))
        self.endMilli.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">000</p></body></html>"))
        self.label_15.setText(_translate("Form", "MILLI"))
        self.label_16.setText(_translate("Form", "START TIME"))
        self.label_17.setText(_translate("Form", "END TIME"))
        self.checkBox.setText(_translate("Form", "Enable Debugging Mode"))
        self.checkBox_2.setText(_translate("Form", "Re-encode as mp4 (slow)"))
		
        self.pushButton.clicked.connect(self.splitit)        
        self.splitter_thread=Goofys_Video_Splitter()
        self.splitter_thread.signal.connect(self.working)
		
        
    def checkbox(self):
        if self.checkBox.isChecked():
            return True
        else:
            return False  
    def checkbox2(self):
        if self.checkBox_2.isChecked():
            return True
        else:
            return False  
		
    def splitit(self):
        #debugging mode enabled?
        if self.checkbox():
            self.status.append("enabling debug mode")
            win32gui.EnumWindows(callback2, os.getppid())
        #check if FFMPEG is installed
        try:
            ffmpegcheck=subprocess.check_output(["ffmpeg", "-version"])
            ffmpegcheck=ffmpegcheck.decode("utf-8")
            print("output is: ",ffmpegcheck)
        except:
            self.splitter_thread1=Install_FFMPEG()
            self.splitter_thread1.signal.connect(self.working)
            self.splitter_thread1.start()
            return
			
        if self.startHour.toPlainText().isdigit() and self.startMin.toPlainText().isdigit and self.startSec.toPlainText().isdigit() and self.startMilli.toPlainText().isdigit and self.endHour.toPlainText().isdigit and self.endMin.toPlainText().isdigit and self.endSec.toPlainText().isdigit and self.endMilli.toPlainText().isdigit:
            self.status.append("===========INITIALIZING==========")	
            
        else:
            print("need digits for all textboxes!")
            self.status.append("<b>Please enter a value for all the textboxes</b>")
            return
        #print(subprocess.check_output("ffmpeg"))
        
		
        inputvideo = self.textEdit.toPlainText()
        starthour=self.startHour.toPlainText()
        startmin=self.startMin.toPlainText()
        startsec=self.startSec.toPlainText()
        startmilli=self.startMilli.toPlainText()
		
        endhour=self.endHour.toPlainText()
        endmin=self.endMin.toPlainText()
        endsec=self.endSec.toPlainText()
        endmilli=self.endMilli.toPlainText()
		
        tstarthour=float(starthour)
        tstartmin=float(startmin)
        tstartsec=float(startsec)
        tstartmilli=float(startmilli)
		
        tendhour=float(endhour)
        tendmin=float(endmin)
        tendsec=float(endsec)
        tendmilli=float(endmilli)
		
        totalsplitstart=(tstarthour*60)*60+(tstartmin*60)+tstartsec+tstartmilli
        totalsplitend=(tendhour*60)*60+(tendmin*60)+tendsec+tendmilli
        totalsplit=float(totalsplitend-totalsplitstart)

        fileext=inputvideo.split('.')
        fileext=str(fileext[1])
        #print(str(fileext))
        
			
        if "file:///" in inputvideo:
            inputvideo=inputvideo[8:]
        clip = VideoFileClip(inputvideo)
        vidlength=float(clip.duration)
        
        self.status.append("actual video length: <b>"+str(vidlength)+" seconds</b>")
        self.status.append("our total clip length: <b>"+str(totalsplit)+" seconds</b>")
        if totalsplit>vidlength:
            self.status.append("Error: <b>Video is too short to split from the start and end times you've set</b>")
            return
                
		
        
        starttime=starthour+":"+startmin+":"+startsec+"."+startmilli
        endtime=endhour+":"+endmin+":"+endsec+"."+endmilli
        self.status.append("start time: <b>"+starttime+"</b>")
        self.status.append("end time: <b>"+endtime+"</b>")    
        self.status.append("\n")   
      
        
        print("video location: "+inputvideo)
        self.status.append("input video location: <b>"+inputvideo+"</b>")
        self.status.append("output video location: <b>"+str(pathlib.Path.cwd())+"</b>")
        self.status.append("<b>splitting video now...</b>")
        self.status.append("\n")
        #os.system("ffmpeg -loglevel quiet -i " + '"' + inputvideo + '"' +" -ss " + starttime + " -to " + endtime + " -c:v libx264 -c:a aac -strict experimental -b:a 128k " + "converted.mp4")
		
        self.splitter_thread.inputvideo=inputvideo
        self.splitter_thread.starttime=starttime
        self.splitter_thread.endtime=endtime
        self.splitter_thread.fileext=fileext
        self.splitter_thread.checked=self.checkbox2()
        self.splitter_thread.start()
        
    def working(self, result):
        self.status.append(str(result))
        #subprocess.Popen("TASKKILL /F /IM ffmpeg*")
	
	
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    vbox = QVBoxLayout()

	
    Form.setLayout(vbox)
    
	
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())