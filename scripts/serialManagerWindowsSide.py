"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
"""
import argparse
import subprocess
import os
import datetime
import sys
import re

import serial
import time

def spliter():
    print('--------------------------------------------------')

def simpleLogger(head:bool,msg:str):
    print(f'{str(datetime.datetime.now())}| [{head}] [{msg}]')
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    # must
    parser.add_argument("-port", "--port", help="which port to read from ? example : /dev/ttyUSB0", type=str, required=True, default=False)
    parser.add_argument("-speed", "--speed", help="what speed is needed for reading ? ", type=str, required=True, default=False)
    # optinal
    parser.add_argument("-session", "--session_timeout",help="for how much time to open the session (in sec)",required=False,type=int, default=60*2)
    parser.add_argument("-read", "--read", action='store_true',help="read from the serial", required=False, default=False)
    parser.add_argument("-read_max", "--read_max",help="read from the serial max X rows", required=False, default=False)
    parser.add_argument("-write", "--write",help="write to the serial", nargs='+',required=False, default=False)
    parser.add_argument("-state", "--state", help="what the state for the port - return open or close.", action='store_true', required=False, default=False)
    # mode
    parser.add_argument("-search", "--search", help="search inside the serial connection", nargs='+',required=False, default=False)
    parser.add_argument("-mq", "--mode_quiet", help="do silence reading", required=False, default=False)
    parser.add_argument("-mo", "--mode_output", help="output the session to output file , must to give only folder path", required=False, default=False)
    parser.add_argument("-msfm", "--mode_search_full_match", help="search inside each row item , only one action , full match", action='store_true', required=False, default=False)
    parser.add_argument("-mspm", "--mode_search_partion_match", help="search inside each row item , only one item , partion match", action='store_true', required=False, default=False)
    parser.add_argument("-bmw", "--break_match_when", help="break the session when match to word", required=False, default=False)
    return parser
# ------- # Class -> tamplateClass # ------- #
class SerialManager():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # Methods -> returnSerConnector # ------- #
    def createSerConnector(self,portName:str,speed:str):
        # port = '/dev/ttyUSB0'
        # baud = 460800
        # ser = serial.Serial(port, baud,bytesize=8, timeout=0.5, stopbits=serial.STOPBITS_ONE)
        _portName = portName
        _speed = speed
        _serConnector = serial.Serial(_portName, _speed,bytesize=8, timeout=0.2, stopbits=serial.STOPBITS_ONE)
        return _serConnector 

    # ------- # Methods -> showCurrentStatus # ------- #
    def showCurrentStatus(self,serConnector):
        if serConnector.isOpen():
            return 'Open'
        else:
            return 'Close'

    # ------- # Methods -> manageSerConnector # ------- #
    def manageSerConnector(self,serConnector:any,open:bool=False,close:bool=False,noPrint:bool=False):
        if open:
            serConnector.close()
            serConnector.open()
            if not noPrint:
                simpleLogger('manage status serial connection',f'Current status is change to [{self.showCurrentStatus(serConnector)}]')
        if close:
            serConnector.close()
            if not noPrint:
                simpleLogger('manage status serial connection',f'Current status is change to [{self.showCurrentStatus(serConnector)}]')
                
    # ------- # Methods -> writeToSer # ------- #
    def writeToSer(self,serConnector:any,msg:str,noPrint:bool=False):
        self.manageSerConnector(serConnector,open=True,noPrint=noPrint)
        _msg = str.encode(msg+'\n')
        serConnector.write(_msg)
        self.manageSerConnector(serConnector,close=True,noPrint=noPrint)
        if not noPrint:
            simpleLogger('info',f'Write to serial [{msg}]')
            
    # ------- # Methods -> readSer # ------- #
    def readSer(
        self,
        serConnector,
        breakWhenMatch:str,
        sessionTimeout:int,
        searchItem:str=False,
        modeSearchFullMatch:bool=False,
        modeSearchPartionMatch:bool=False,
        ):
        # init basic var
        self.manageSerConnector(serConnector,open=True)
        _setSessionTimeout = time.time() + sessionTimeout 
        _counterFullMatch = 0 
        _counterPartialMatch = 0 
        # get 3 auto enter

        while True:
            # check timeout
            if time.time() > _setSessionTimeout:
                spliter()
                simpleLogger('Timeout ended for session','Timeout for session is over , exit loop.')
                spliter()
                break
            # get the output
            bytesToRead = serConnector.inWaiting()
            _capReading = serConnector.read(bytesToRead).decode('utf-8','ignore').strip().split('\n')

            # if output is contain someting
            if _capReading:
                for _eachRow in _capReading:
                    _eachRow = _eachRow.replace('\r','')
                    if len(_eachRow) > 2:
                        # if need to search item
                        if breakWhenMatch:
                            if str(breakWhenMatch).strip() in _eachRow:
                                spliter()
                                simpleLogger('Break word Match',f'Found break word inside row --> [{_eachRow}] , Break the loop.')
                                spliter()
                                break
                        # search item
                        if searchItem:
                            for _eachSearchItem in searchItem:
                                # search parital match
                                if modeSearchPartionMatch:
                                    if _eachSearchItem.strip() in _eachRow:
                                        spliter()
                                        simpleLogger('Found Match',f'Found item word inside row --> [{_eachRow}] | itration [{_counterPartialMatch}]')
                                        spliter()
                                        _counterPartialMatch+=1
                                        

                                # search full match
                                if modeSearchFullMatch:
                                    if _eachSearchItem.strip() == _eachRow:
                                        spliter()
                                        simpleLogger('Found Match',f'Found item word inside row --> [{_eachRow}] | itration [{_counterFullMatch}]')
                                        spliter()
                                        _counterFullMatch+=1
                                if not modeSearchPartionMatch and not modeSearchFullMatch:
                                    if _eachSearchItem.strip() in _eachRow:
                                        spliter()
                                        simpleLogger('Found Match',f'Found item word inside row --> [{_eachRow}] | itration [{_counterPartialMatch}]')
                                        spliter()
                                        _counterPartialMatch+=1
                        simpleLogger('LoggerOutput',_eachRow)



    # ------- # Methods -> deploySerialMannger # ------- #
    def deploySerialMannger(
    self,
    portName:str,
    speed:str,
    sessionTimeout:int,
    read:bool=False,
    modeSearchFullMatch:str=False,
    modeSearchPartionMatch:str=False,
    breakWhenMatch:bool=False,
    write:bool=False,
    modeQuiet:bool=False,
    modeOutput:bool=False,
    searchItem:str=False
    ):

        spliter()
        simpleLogger('info',f'Attribute [portName]                        is set to [{portName}]')
        simpleLogger('info',f'Attribute [speed]                           is set to [{speed}]')
        simpleLogger('info',f'Attribute [searchItem]                      is set to [{searchItem}]')
        simpleLogger('info',f'Attribute [sessionTimeout]                  is set to [{sessionTimeout}]')
        simpleLogger('info',f'Attribute [read]                            is set to [{read}]')
        simpleLogger('info',f'Attribute [write]                           is set to [{write}]')
        simpleLogger('info',f'Attribute [modeQuiet]                       is set to [{modeQuiet}]')
        simpleLogger('info',f'Attribute [modeOutput]                      is set to [{modeOutput}]')
        simpleLogger('info',f'Attribute [modeSearchFullMatch]             is set to [{modeSearchFullMatch}]')
        simpleLogger('info',f'Attribute [modeSearchPartionMatch]          is set to [{modeSearchPartionMatch}]')
        simpleLogger('info',f'Attribute [breakWhenMatch]                  is set to [{breakWhenMatch}]')
        spliter()
        # check if the user is insert current port name and speed
        if len(portName) > 0 and len(speed) > 0:
            _setSerConnector = self.createSerConnector(portName=portName,speed=speed)
            _currentState = self.showCurrentStatus(serConnector=_setSerConnector)
            simpleLogger('info',f'Serial connector is create , current status is for serial is [{_currentState}]')
            # check read
            if read:
                self.writeToSer(serConnector=_setSerConnector,msg='     ',noPrint=True)
                self.readSer(
                    serConnector=_setSerConnector,
                    breakWhenMatch=breakWhenMatch,
                    sessionTimeout=sessionTimeout,
                    searchItem=searchItem,
                    modeSearchFullMatch=modeSearchFullMatch,
                    modeSearchPartionMatch=modeSearchPartionMatch
                    ) 
            # check write
            if write:
                for _eachItemToWrite in write:
                    
                    self.writeToSer(serConnector=_setSerConnector,msg=_eachItemToWrite)
        else:
            simpleLogger('Fail','Please make sure that you insert the current port number and the current speed !')

if __name__ == "__main__":
    
    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.port and args.speed:
        SerialManager().deploySerialMannger(
            portName=args.port,
            speed=args.speed,
            read=args.read,
            write=args.write,
            modeQuiet=args.mode_quiet,
            modeOutput=args.mode_output,
            modeSearchFullMatch=args.mode_search_full_match,
            modeSearchPartionMatch=args.mode_search_partion_match,
            sessionTimeout=args.session_timeout,
            breakWhenMatch=args.break_match_when,
            searchItem=args.search
            )
























