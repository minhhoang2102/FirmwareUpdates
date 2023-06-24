from machine import UART, Pin
from math import radians, cos, sin, asin, sqrt
import math
import utime

#indicate program started visually
# led_onboard = machine.Pin(25, machine.Pin.OUT)
# led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
# utime.sleep(0.5)
# led_onboard.value(1)
# utime.sleep(1.0)
# led_onboard.value(0)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
# uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  # for ATmega328P
# print(uart0)

def sendCMD_waitResp(cmd, timeout):
    print("CMD: " + cmd)
    uart0.write(cmd + '\r\n')
#     return waitResp(timeout)
    prvMills = utime.ticks_ms()
    resp = b''
    while (utime.ticks_ms() - prvMills) < timeout:
        if uart0.any():
            resp = b''.join([resp, uart0.read(1)])
    print('Response:')
    try:
        print(resp.decode())
        return resp.decode()
    except UnicodeError:
        print(resp)
    
# def waitResp(timeout):
#     prvMills = utime.ticks_ms()
#     resp = b""
#     while (utime.ticks_ms() - prvMills) < timeout:
#         if uart0.any():
#             resp = b"".join([resp, uart0.read(1)])
#     print("Response:")
#     try:
#         print(resp.decode('utf-8'))
#         return resp.decode('utf-8')
#     except UnicodeError:
#         print(resp)
        
# Wait and show response without return
# def sendCMD_waitAndShow(cmd, uart=uart0):
#     print("CMD: " + cmd)
#     uart.write(cmd + '\r\n')
#     while True:
#         print(uart.readline())

#--------------Commands for File System--------------#
def SelectDir(path):
    sendCMD_waitResp('AT+FSCD='+path, 1000)
    #list file: 0 ; list dir: 1
def ListDirFile(wtype):
    sendCMD_waitResp('AT+FSLS=' + wtype, 1000)
def TransFileCMD(filepath, location, size):
    return sendCMD_waitResp('AT+CFTRANTX=' + '\"' + filepath + '\",' + location + ',' + size, 1000)
def TransFileCMD_Full(filepath):
    return sendCMD_waitResp('AT+CFTRANTX=' + '\"' + filepath + '\"', 5000)
def FileInfo(filename):
    return sendCMD_waitResp('AT+FSATTRI=' + filename, 1000)
def FileSize(filename):
    rx_str = FileInfo(filename)
    list_str = rx_str.splitlines()
    return list_str[2][9:14]
def DeleteFile(filename):
    sendCMD_waitResp('AT+FSDEL=' + filename, 1000)
#----------------------------------------------------#

#--------------Commands for FTPS--------------#
def StartFTP():
    sendCMD_waitResp('AT+CFTPSSTART', 1000)
def StopFTP():
    sendCMD_waitResp('AT+CFTPSSTOP', 1000)
def LoginFTPServer(host, port, username, password, server_type):
    sendCMD_waitResp('AT+CFTPSLOGIN='+'\"'+host+'\",'+port+',\"'+username+'\",'+'\"'+password+'\",'+server_type, 3000)
def LogoutFTPServer():
    sendCMD_waitResp('AT+CFTPSLOGOUT', 1000)
def ChangeDir(dir_name):
    sendCMD_waitResp('AT+CFTPSCWD='+'\"'+dir_name+'\"', 2000)
def GetCurrentDir():
    sendCMD_waitResp('AT+CFTPSPWD', 1000)
def ListItems(dir_name):
    sendCMD_waitResp('AT+CFTPSLIST='+'\"'+dir_name+'\"', 1000)
def downloadFromFTP(filename):
    #dir_in: 1-F:/ 2-D:/ 3-E:/
    print('Downloading file from FTP...')
    sendCMD_waitResp('AT+CFTPSGETFILE='+'\"'+filename+'\"', 3000)
def uploadToFTP(filename, dir_in):
	print('Uploading file from FTP...')
	send_at('AT+CFTPSPUTFILE='+'\"'+filename+'\"', 3000)
#--------------------------------------------#

#--------------Commands for GPS--------------#
def StartGPS():
    sendCMD_waitResp('AT+CGPS=1', 1000)
def StopGPS():
    sendCMD_waitResp('AT+CGPS=0', 1000)
def GetGPSinfo():
    return sendCMD_waitResp('AT+CGPSINFO', 1000)
def StrtGPSauto(auto):
    sendCMD_waitResp('AT+CGPS=' + auto, 1000)
    #Return lists of latitude and longitude    
def ReadPosition(RxStr):
    RxStr = RxStr.split("+CGPSINFO: ")
    
    #calculate position
    lat_raw = ''
    lon_raw = ''
    lat_raw = RxStr[1][0:11]
    lon_raw = RxStr[1][14:26]
    lat_raw1 = float(lat_raw[0:2])
    lat_raw2 = float(lat_raw[2:12])
    lon_raw1 = float(lon_raw[0:3])
    lon_raw2 = float(lon_raw[3:13])
    lat = lat_raw1 + lat_raw2/60
    lon = lon_raw1 + lon_raw2/60
#     print('lat: ', lat_raw)
#     print('lon: ', lon_raw)
    a = (lat, lon)
    return a

def ReadDistance(lat1, lon1, lat2, lon2):
    #convert degrees to radians
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6378100 #6378100 is the radius of the Earth
    return distance
#--------------------------------------------#
    
#____________________Transfer HEX file to Raspberry Pi Pico____________________#
#Extract HEX file with the input is the string reponsed from AT+CFTRANTX command
def ExtractRxHexStr(RxStr):
    #List recevived data from UART by the string "+CFTRANTX:"
    RxStr = RxStr.split("+CFTRANTX:")

    #Find and Join all strings that include hex file data
    HexFile1 = ''
    for str1 in RxStr:
        if str1[1:5] == 'DATA':
            HexFile1 += str1[10:len(str1)];
            
    #List the data string by '\n'
    HexFile1_List = HexFile1.splitlines()
    
    #Join all the data lists that do not include any '\n'
    HexFile2 = ''
    for str2 in HexFile1_List:
        if str2 != '':
            HexFile2 += str2;
            
    #Delete the '' in the first position of HexFile2
    HexFile2 = HexFile2[1:]
    
    #List the HexFile string by ':'
    HexFile2_List = HexFile2.split(':')
    
    #Reform the HexFile2_List by adding ':' and '\r\n' at the first and the last position of each string
    for i in range(len(HexFile2_List)):
        HexFile2_List[i] = ':' + HexFile2_List[i] + '\r\n';
        
    #Join all the parts to make a hex string of original form
    HexFile3 = ''.join(HexFile2_List)
    #print(HexFile3)
    #print('Size of HexFile3 is: ', len(HexFile3))
    return HexFile3

#Get HEX file from a file path and return the string of that file
def GetRxHexStr(filepath):
    #Send AT command and save the response in RxString
    SelectDir('F:/')
    RxString = TransFileCMD_Full(filepath)
    while RxString[-4:-2] != 'OK':
        RxString = ''
        RxString = TransFileCMD_Full(filepath)
    #Extract and transform a original HEX file and save to RawFile
    RawFile = ExtractRxHexStr(RxString)
    return RawFile
#______________________________________________________________________________#

# response = GetGPSinfo()
# res_list = response.split('\r\n')
# if len(res_list[1]) == 19:
#     print('waiting for GPS info...')
# print('gps info:', res_list[1])
# print('size of res:', len(res_list[1]))

    
# while True:
#     x = GetGPSinfo()
#     y = ReadPosition(x)
#     lat = y[0]
#     lon = y[1]
# #     print('latitude: ',ReadPosition(x))
#     dist = ReadDistance(DHBKgps[0], DHBKgps[1], lat, lon)
#     print('dist =', dist/1000)
#     utime.sleep(5)

# filename = 'Blink2sec.ino.hex'
# filename = 'Blink2sec.ino.hex'

#----------------------------main----------------------------#
# DeleteFile('version.txt')
# StartFTP()
# LoginFTPServer('ftp.drivehq.com', '21', 'mh1911200', '98027435610', '0')
# utime.sleep(3)
# ChangeDir('Firmware_Updates')
# utime.sleep(3)
# downloadFromFTP('version.txt')
# utime.sleep(2)
# LogoutFTPServer()
# utime.sleep(2)
# StopFTP()
# ListDirFile('0')


