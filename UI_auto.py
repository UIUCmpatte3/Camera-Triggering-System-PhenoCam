#import libraries for date/time as well as GoPro API
from datetime import datetime, timedelta
from goprocam import GoProCamera, constants

#import libraries for reading/interpreting webserver data
import requests as req
import re

#import library to enable switching between WiFi
import os

#import library for keeping track of time
import time

#import library for generating a GUI
import PySimpleGUI as sg

import sys

os.system('cmd /c "netsh wlan show networks"')

def connect2wifi():
    name_of_router = "GalaxyA71"

    os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    
def connect2gp():
    name_of_router = "GP25763318"

    os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    
def getInfo():
    og_stdout = sys.stdout
    with open('CamInfo.txt', 'w') as f:
        sys.stdout = f
        gopro.overview()
        sys.stdout = og_stdout
        
    f = open("CamInfo.txt", "r")
    return f.readlines()

def setAlarms(start,inter,b):
    alarms = []
    td = b / inter
    for i in range(inter):
        start = start + timedelta(minutes = td)
        alarms.append(start.strftime("%H:%M"))
    return(alarms)
    
    

suffix = '.jpg'
zoom = 0
displayZoom = zoom*0.01 + 1
ZoomStr = str(displayZoom) + "x"

W = 10
L = 1000
D = 20

gopro = GoProCamera.GoPro(constants.gpcontrol)
gopro.mode("1")
gopro.setZoom(zoom)

lines = getInfo()

t_begin = datetime(1,1,1,7,0)
bank = 12*60
alarms = []

sg.theme('DarkTeal7')

layout = [
    
    [sg.Text('Camera info:'), sg.Text(size=(30,1), key='-INFO-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO1-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO2-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO3-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO4-'), sg.VSeperator(), sg.Text('Battery Life:'), sg.Text(size=(3,1), key= '-BAT-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO5-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO6-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO7-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO8-')],
    
    [sg.Text('                   '), sg.Text(size=(30,1), key='-INFO9-')],
    
    [sg.Text('Desired zoom level (0 - 100%):'), sg.Text(size=(7,1), key='-ZOOM-'), sg.Input(key='-IN-'), sg.Button('Update')],
    
    [sg.Text('Desired Wind Threshold:'), sg.Text(size=(10,1), key='-WINDd-'), sg.Input(key='-WIND-'), sg.Button('Set Wind')],
    
    [sg.Text('Desired Dark Threshold:'), sg.Text(size=(10,1), key='-DARKd-'), sg.Input(key='-DARK-'), sg.Button('Set Darkness')],
    
    [sg.Text('Desired Light Threshold:'), sg.Text(size=(10,1), key='-LUXd-'), sg.Input(key='-LUX-'), sg.Button('Set Light')],
    
    [sg.Text('Input desired number of photos per day:'), sg.Listbox(values=['3','6','9','12'], size=(30,10), key='-ALARM-'), sg.Button('Set')],
    
    [sg.Text('Wind Value of Last Scan:'), sg.Text(size=(10,1), key='-WINDS-')],
    
    [sg.Text('Light Value of Last Scan:'), sg.Text(size=(10,1), key='-LUXS-')],
    
    [sg.Text('Take photo:'), sg.Button('Trigger'), sg.VSeperator(), sg.Text('Take photo regardless of conditions:'), sg.Button('Enter')],

    [sg.Text('Delete photos from GoPro'), sg.Checkbox('', default = False, key ='-DEL-')]
    
    ]


window = sg.Window('PhenoCam', layout, finalize=True)

window['-ZOOM-'].update(ZoomStr)

Wstring = str(W) + ' MPH'
window['-WINDd-'].update(Wstring)

Dstring = str(D) + ' LUX'
window['-DARKd-'].update(Dstring)

Lstring = str(L) + ' LUX'
window['-LUXd-'].update(Lstring)

while True: 
    
    print('Loop Test')
    
    check = datetime.now().strftime("%H:%M")
    if check in alarms:
        connect2wifi()
        time.sleep(10)
        
        resp = req.get("http://192.168.145.80/")
        content = resp.text
        stripped = re.sub('<[^<]+?>', '', content)
        piezas = stripped.split('\n')
        
        viento = int(piezas[3])
        luz = int(piezas[5])
        
        connect2gp()
        
        Sen1 = str(viento) + ' MPH'
        window['-WINDS-'].update(Sen1)
        
        Sen2 = str(luz) + ' LUX'
        window['-LUXS-'].update(Sen2)
        
        if viento>W or (luz<D or luz>L):
            pass
        else:
            gopro.take_photo()
            now = datetime.now()
            dt = now.strftime("%m-%d-%Y %H;%M;%S")
            filename = dt + suffix
            gopro.downloadLastMedia(custom_filename=filename)
        
    
    lines = getInfo()
    window['-INFO-'].update(lines[12])
    window['-INFO1-'].update(lines[14])
    window['-INFO2-'].update(lines[13])
    window['-INFO3-'].update(lines[9])
    window['-INFO4-'].update(lines[7])
    window['-INFO5-'].update(lines[8])
    window['-INFO6-'].update(lines[3])
    window['-INFO7-'].update(lines[6])
    window['-INFO8-'].update(lines[4])
    window['-INFO9-'].update(lines[5])
        
    Battery = gopro.getStatus("status","70")
    BatteryPercentage = str(Battery) + "%"
    window['-BAT-'].update(BatteryPercentage)
    
    event, values = window.read(timeout=60000)
    print(event, values)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Set':
        intervals = int(values('-ALARM-'))
        alarms = setAlarms(t_begin, intervals, bank)
    
    if event == 'Update':
        zoom = int(values['-IN-'])
        gopro.setZoom(zoom)
        displayZoom = zoom*0.01 + 1
        ZoomStr = str(round(displayZoom,2)) + "x"
        window['-ZOOM-'].update(ZoomStr)
        
    if event == 'Set Wind':
        W = int(values['-WIND-'])
        Wstring = str(W) + ' MPH'
        window['-WINDd-'].update(Wstring)

    if event == 'Set Darkness':
        D = int(values['-DARK-'])
        Dstring = str(D) + ' LUX'
        window['-DARKd-'].update(Dstring)

    if event == 'Set Light':
        L = int(values['-LUX-'])
        Lstring = str(L) + ' LUX'
        window['-LUXd-'].update(Lstring)
        
    if event == 'Enter':
        gopro.take_photo()
        now = datetime.now()
        dt = now.strftime("%m-%d-%Y %H;%M;%S")
        filename = dt + suffix
        gopro.downloadLastMedia(custom_filename=filename)
        
        sg.popup('Picture Taken','Picture has been taken regardless of ambient conditions and saved onto the PC as ' + filename)
        
        if values['-DEL-'] == True:
            gopro.delete("last")
        
    if event == 'Trigger':
        connect2wifi()
        time.sleep(10)
        
        resp = req.get("http://192.168.145.80/")
        content = resp.text
        stripped = re.sub('<[^<]+?>', '', content)
        piezas = stripped.split('\n')
        
        viento = int(piezas[3])
        luz = int(piezas[5])
        
        connect2gp()
        
        Sen1 = str(viento) + ' MPH'
        window['-WINDS-'].update(Sen1)
        
        Sen2 = str(luz) + ' LUX'
        window['-LUXS-'].update(Sen2)
        
        if viento>W or (luz<D or luz>L):
            sg.popup("Conditions NOT suitable for photo!")
        else:
            sg.popup("Conditions suitable for photo!")
            gopro.take_photo()
            now = datetime.now()
            dt = now.strftime("%m-%d-%Y %H;%M;%S")
            filename = dt + suffix
            gopro.downloadLastMedia(custom_filename=filename)
            
            sg.popup('Picture Taken','Picture has been taken regardless of ambient conditions and saved onto the PC as ' + filename)


window.close()