from machine import UART, Pin
import machine
import utime

#indicate program started visually
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# print(uart0)

def sendCMD_waitResp(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd + '\r\n')
    return waitResp(uart, timeout)
    
def waitResp(uart=uart0, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms() - prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("Response:")
    try:
        print(resp.decode())
        return resp.decode()
    except UnicodeError:
        print(resp)
        
# Wait and show response without return
def sendCMD_waitAndShow(cmd, uart=uart0):
    print("CMD: " + cmd)
    uart.write(cmd + '\r\n')
    while True:
        print(uart.readline())

#--------------Commands for File System--------------#
def SelectDir(path):
    sendCMD_waitResp('AT+FSCD=')
    #list file: 0 ; list dir: 1
def ListDirFile(wtype):
    sendCMD_waitResp('AT+FSLS=' + wtype)
def TransFileCMD(filepath, location, size):
    return sendCMD_waitResp('AT+CFTRANTX=' + '\"' + filepath + '\",' + location + ',' + size)
def TransFileCMD_Full(filepath):
    return sendCMD_waitResp('AT+CFTRANTX=' + '\"' + filepath + '\"')
def FileInfo(filename):
    return sendCMD_waitResp('AT+FSATTRI=' + filename)
def FileSize(filename):
    rx_str = FileInfo(filename)
    list_str = rx_str.splitlines()
    return list_str[2][9:14]
#----------------------------------------------------#

#--------------Commands for FTPS--------------#
def StartFTP():
    sendCMD_waitResp('AT+CFTPSSTART')
def StopFTP():
    sendCMD_waitResp('AT+CFTPSSTOP')
def LoginFTPServer(host, port, username, password, server_type):
    sendCMD_waitResp('AT+CFTPSLOGIN='+'\"'+host+'\",'+port+',\"'+username+'\",'+'\"'+password+'\",'+server_type)
def LogoutFTPServer():
    sendCMD_waitResp('AT+CFTPSLOGOUT')
def ChangeDir(dir_name):
    sendCMD_waitResp('AT+CFTPSCWD='+'\"'+dir_name+'\"')
def GetCurrentDir():
    sendCMD_waitResp('AT+CFTPSPWD')
def ListItems(dir_name):
    sendCMD_waitResp('AT+CFTPSLIST='+'\"'+dir_name+'\"')
def downloadFromFTP(filename):
    #dir_in: 1-F:/ 2-D:/ 3-E:/
    print('Downloading file from FTP...')
    sendCMD_waitResp('AT+CFTPSGETFILE='+'\"'+filename+'\"')
def uploadToFTP(filename, dir_in):
	print('Uploading file from FTP...')
	send_at('AT+CFTPSPUTFILE='+'\"'+filename+'\"')
#--------------------------------------------#

#--------------Commands for GPS--------------#
def StartGPS():
    sendCMD_waitResp('AT+CGPS=1')
def StopGPS():
    sendCMD_waitResp('AT+CGPS=0')
def GetGPSinfo():
    sendCMD_waitResp('AT+CGPSINFO')
def StrtGPSauto(auto):
    sendCMD_waitResp('AT+CGPS=' + auto)
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

def downloadFirmware(filename):
    #FTP Server
    ChangeDir('Firmware_Updates')
    downloadFromFTP(filename)
    
    #File Transfer
    return GetRxHexStr('F:/' + filename)
sendCMD_waitResp('AT')
#----------------------------main----------------------------#
# StopFTP()
# LoginFTPServer('ftp.drivehq.com', '21', 'mh1911200', '98027435610', '0')
# f = GetRxHexStr('F:/Blinkfast.ino.hex')
# print(f)
# print('size:', len(f))
# print('hexstr[-4:-2]:', RxString[-4:-2])
# GetRxHexStr(hexstr)


