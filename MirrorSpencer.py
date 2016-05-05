## A Magic Mirror GUI for Lydian Academy
## We should use a grid layout

'''
To Do:
Make mirror pretty
add calendar
'''

from PyQt4 import QtGui
from PyQt4 import QtCore
import json
import sys
import urllib.request
from pprint import pprint
import time
import urllib.parse

class Mirror(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

## ______FONTS SET_______
        font = QtGui.QFont()
        futureWeatherFont = QtGui.QFont()
        #font.setBold(True)
        font.setPointSize(16)
        currentTempFont= QtGui.QFont()
        currentTempFont.setPointSize(45)
        futureWeatherFont.setPointSize(20)
        welcomeFont= QtGui.QFont()
        welcomeFont.setPointSize(12)
        subFont= QtGui.QFont()
        subFont.setPointSize(12)
        
##______AUTOMATED TIMERS SET_______
        self.timeTimer = QtCore.QTimer(self)
        self.timeTimer.timeout.connect(self.clockTime)
        self.timeTimer.start(1000)
        self.weatherTimer = QtCore.QTimer(self)
        self.weatherTimer.timeout.connect(self.weatherUpdate)
        self.weatherTimer.start(300000) 

        
##______HTTP REQUESTS AND CONVERSIONS________
        httpResponse = urllib.request.urlopen('http://api.wunderground.com/api/04915d9631bdf042/conditions/forecast/alerts/almanac/q/CA/Menlo_Park.json')
        strResponse = httpResponse.read().decode('utf-8')
        dictResponse = json.loads(strResponse)


        
##______TIME AND DATE_______
        self.currentTime = time.strftime('%A\n%H:%M')
        self.currentTime = QtGui.QLabel(self.currentTime, self)
        self.currentTime.move(900, 60)
        self.currentTime.setFont(font)
        monthDayYear = time.strftime('%m/%d/%y').split('/')
        dateDict = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
            }
        date = monthDayYear[1]+' '+dateDict[int(monthDayYear[0])]+' '+'20'+monthDayYear[2]
        if date[0] == '0':
            date = date[1:]
        date = QtGui.QLabel(date, self)
        date.move(900,120)
        date.setFont(font)

##______WEATHER STUFF______
        today = dictResponse['forecast']['simpleforecast']['forecastday'][0]['date']['weekday_short']
        tomorrowText = dictResponse['forecast']['simpleforecast']['forecastday'][1]['date']['weekday_short']
        twoDaysText = dictResponse['forecast']['simpleforecast']['forecastday'][2]['date']['weekday_short']
        threeDaysText = dictResponse['forecast']['simpleforecast']['forecastday'][3]['date']['weekday_short']

##_____CURRENT WEATHER___________________
        self.nowWeatherLabel = QtGui.QLabel(str(dictResponse['current_observation']['temp_f'])
                              + '\xb0F', self)
        self.nowWeatherLabel.move(10,100)
        self.nowWeatherLabel.setFont(currentTempFont)
        urllib.request.urlretrieve(dictResponse['current_observation']['icon_url'],
                                   "weather.png")
        #self.resize('weather.png', 100)
        weatherPixmap = QtGui.QPixmap("weather.png")
        weatherPixmap = QtGui.QPixmap(r'weather.png').scaled(100, 100, transformMode=QtCore.Qt.SmoothTransformation)
        self.weather = QtGui.QLabel(self)
        self.weather.setPixmap(weatherPixmap)
        self.weather.move(180,108)

##_____TODAY________________
        today += (": " + dictResponse['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'] + '\xb0')
        self. todayLabel = QtGui.QLabel(today, self)
        self.todayLabel.move(10,200)
        self.todayLabel.setFont(futureWeatherFont)
        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][0]['icon_url'],
                                   "today.png")
        todayPixmap = QtGui.QPixmap("today.png")
        todayPixmap = QtGui.QPixmap(r'today.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.todayMap = QtGui.QLabel(self)
        self.todayMap.setPixmap(todayPixmap)
        self.todayMap.move(180,190)
##_____TOMORROW____________
    
        tomorrowText += (": " + dictResponse['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit'] + '\xb0')
        self.tomorrowLabel = QtGui.QLabel(tomorrowText, self)
        self.tomorrowLabel.move(10,240)
        self.tomorrowLabel.setFont(futureWeatherFont)
        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][1]['icon_url'],
                                   "tomorrow.png")
        tomorrowPixmap = QtGui.QPixmap("tomorrow.png")
        tomorrow= QtGui.QPixmap(r'tomorrow.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.tomorrowMap = QtGui.QLabel(self)
        self.tomorrowMap.setPixmap(tomorrow)
        self.tomorrowMap.move(180,230)
##_____TWODAYS_________________

        twoDaysText += (": " + dictResponse['forecast']['simpleforecast']['forecastday'][2]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][2]['low']['fahrenheit'] + '\xb0')
        self.twoDaysTextLabel = QtGui.QLabel(twoDaysText, self)
        self.twoDaysTextLabel.move(10,280)
        self.twoDaysTextLabel.setFont(futureWeatherFont)
        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][2]['icon_url'],
                                   "twoDays.png")
        twoDaysPixmap = QtGui.QPixmap("twoDays.png")
        twoDays= QtGui.QPixmap(r'twoDays.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.twoDaysMap = QtGui.QLabel(self)
        self.twoDaysMap.setPixmap(twoDays)
        self.twoDaysMap.move(180,270)
##_____THREEDAYS_______________

        threeDaysText += (": " + dictResponse['forecast']['simpleforecast']['forecastday'][3]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][3]['low']['fahrenheit'] + '\xb0')
        self.threeDaysTextLabel = QtGui.QLabel(threeDaysText, self)
        self.threeDaysTextLabel.move(10,320)
        self.threeDaysTextLabel.setFont(futureWeatherFont)
        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][3]['icon_url'],
                                   "threeDays.png")
        threeDaysPixmap = QtGui.QPixmap("threeDays.png")
        threeDaysPixmap= QtGui.QPixmap(r'threeDays.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.threeDaysMap = QtGui.QLabel(self)
        self.threeDaysMap.setPixmap(threeDaysPixmap)
        self.threeDaysMap.move(180,310)


##______LYDIAN LOGO_______
        logoPixmap = QtGui.QPixmap("LydianLogoBrightBlackFixed.png")
        logo = QtGui.QLabel(self)
        logo.setPixmap(logoPixmap)
        logo.move(200,0)

##______WELCOME TO LYDIAN_______
        self.welcomeToLydian = QtGui.QLabel('Welcome To Lydian', self)
        self.welcomeToLydian.move(100,10)
        self.welcomeToLydian.setFont(welcomeFont)
        self.subLydian = QtGui.QLabel('An innovative middle and high school in the heart of Silicon Valley.', self)
        self.subLydian.move(100,10)
        self.subLydian.setFont(subFont)

##______DISPLAY, PALETTE, AND SHOW______
        self.showFullScreen()
        pal=QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0))
        pal.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255,255,255))
        self.setPalette(pal)
        self.show()
        
    def resize(image, outsize, self):

        bitmap = QtGui.QPixmap(image)
        bitmap.scaled(QtCore.QSize(outSize, outSize), aspectMode=QtCore.Qt.KeepAspectRatio, mode = QtCore.Qt.SmoothTransformation) #original is larger than this
        file = QtCore.QFile(image)
        file.open(QtCore.QIODevice.WriteOnly)
        bitmap.save(file)
        file.close()
    
    def clockTime(self):
        self.currentTime.setText(time.strftime('%A\n%H:%M'))
        
##_____Weather Update_____________________________
    def weatherUpdate(self):
        '''Updates weather stuff'''
        print('banana')
        try:
            httpResponse = urllib.request.urlopen('http://api.wunderground.com/api/04915d9631bdf042/conditions/forecast/alerts/almanac/q/CA/Menlo_Park.json')
        except:
            pass
        strResponse = httpResponse.read().decode('utf-8')
        dictResponse = json.loads(strResponse)
        urllib.request.urlretrieve(dictResponse['current_observation']['icon_url'],
                                   "weather.png")
        weatherPixmap = QtGui.QPixmap("weather.png")
        weatherPixmap = QtGui.QPixmap(r'weather.png').scaled(100, 100, transformMode=QtCore.Qt.SmoothTransformation)
        self.weather.setPixmap(weatherPixmap)

        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][0]['icon_url'],
                                   "today.png")
        todayPixmap = QtGui.QPixmap("today.png")
        todayPixmap = QtGui.QPixmap(r'today.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.todayMap.setPixmap(todayPixmap)

        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][1]['icon_url'],
                                   "tomorrow.png")
        tomorrowPixmap = QtGui.QPixmap("tomorrow.png")
        tomorrow= QtGui.QPixmap(r'tomorrow.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.tomorrowMap.setPixmap(tomorrow)

        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][2]['icon_url'],
                                   "twoDays.png")
        twoDaysPixmap = QtGui.QPixmap("twoDays.png")
        twoDays= QtGui.QPixmap(r'twoDays.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.twoDaysMap.setPixmap(twoDays)

        urllib.request.urlretrieve(dictResponse['forecast']['simpleforecast']['forecastday'][3]['icon_url'],
                                   "threeDays.png")
        threeDaysPixmap = QtGui.QPixmap("threeDays.png")
        threeDaysPixmap= QtGui.QPixmap(r'threeDays.png').scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation)
        self.threeDaysMap.setPixmap(threeDaysPixmap)
        
        self.nowWeatherLabel.setText(str(dictResponse['current_observation']['temp_f'])
                              + '\xb0F')
        self.todayLabel.setText( ( dictResponse['forecast']['simpleforecast']['forecastday'][0]['date']['weekday_short']+": " + dictResponse['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'] + '\xb0'))

        self.tomorrowLabel.setText( ( dictResponse['forecast']['simpleforecast']['forecastday'][1]['date']['weekday_short']+": " + dictResponse['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit'] + '\xb0'))

        self.twoDaysTextLabel.setText( ( dictResponse['forecast']['simpleforecast']['forecastday'][2]['date']['weekday_short']+": " + dictResponse['forecast']['simpleforecast']['forecastday'][2]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][2]['low']['fahrenheit'] + '\xb0'))

        self.threeDaysTextLabel.setText( ( dictResponse['forecast']['simpleforecast']['forecastday'][3]['date']['weekday_short']+": " + dictResponse['forecast']['simpleforecast']['forecastday'][3]['high']['fahrenheit'] +  '\xb0' +
                  '/' + dictResponse['forecast']['simpleforecast']['forecastday'][3]['low']['fahrenheit'] + '\xb0'))
        
        '''do the above process for all of the labels and weather pixmaps. Change the labels to instance variable (add self).'''       

    def keyPressEvent(self, e):    
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
            
def main():
    app = QtGui.QApplication(sys.argv)
    mirror = Mirror()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
