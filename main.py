from machine import UART, I2C, Pin, SPI
from ssd1306 import SSD1306_I2C
from urtc import DS1307
from AVR_CMD import Command, AVR_model, AVR_signature
import framebuf
import time, utime

from SIM7600E import *
from DataPackage import *
from encoder import *
import DataProcess as DP

# Blinks = '945C000C946E000C946E000C946E00946E000C946E000C946E000C946E00946E000C946E000C946E000C946E00946E000C946E000C946E000C946E009413010C946E000C946E000C946E00946E000C946E000C946E000C946E00946E000C946E0000000000240027000000000000250028002B00040404040404040202020202020303030303030204081020408001020408102001020810200000000800020100000304070000000000000011241FBECFEFD8E0BFCDBF21E0A0E0B1E001C01D92A93007E1F70E945D010C94CC010C940000EAF0E02491E2E9F0E09491EEE7F0E091EE23C9F0222339F0233001F1A8F43019F1223029F1F0E0EE0FFF1FEE584FA591B4912FB7F894EC91811126C0959E239C932FBF08952730A9F02830F0243049F7209180002F7D03C02091002F7720938000DFCF24B52F7724BDCF24B52F7DFBCF2091B0002F77209300D2CF2091B0002F7DF9CF9E2BDACFB7F8948091050190910601A091070191080126B5A89B05C02F3F19F001961DB11D3FBFBA2FA92F982F8827BC0101620F711D811D911D42E0660F771F1F991F4A95D1F708958F929F92AF9292CF92DF92EF92FF920E94B8004B010188EEC82E83E0D82EE12CF12C0E9400681979098A099B09683E7340810505A8F321E0C21AD108E108F10888EE0E83E0981EA11CB11CC114D104E1040429F7FF90EF90DF90CF90BF90AF90908F9008951F920F920FB60F921124933F938F939F93AF93BF9380910101910201A0910301B091040130910001E0230F2D3758F50196A11DB11D2093018093010190930201A0930301B093018091050190910601A0910701B091010196A11DB11D8093050190930601930701B0930801BF91AF919F918F91912F910F900FBE0F901F90189526E80F0296A11DB11DD2CF789484B58260BD84B5816084BD85B5826085BD85B56085BD80916E00816080936E00109200809181008260809381008091810060809381008091800081608093800091B10084608093B1008091B000816093B00080917A00846080937A00809100826080937A0080917A00816080930080917A00806880937A001092C100E9F0E02491EEE7F0E08491882399F0E0880F991FFC01E859FF4FA591B49101EE58FF4F859194918FB7F894EC912BEC938FBFC0E0D0E081E00E94700094DD0080E00E9470000E94DD002097F30E940000F1CFF894FFCFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# Blink_fast  = '0C945C000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C9412010C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E0000000000240027002A0000000000250028002B0004040404040404040202020202020303030303030102040810204080010204081020010204081020000000080002010000030407000000000000000011241FBECFEFD8E0DEBFCDBF21E0A0E0B1E001C01D92A930B207E1F70E945C010C94CB010C940000E1EBF0E02491EDE9F0E09491E9E8F0E0E491EE23C9F0222339F0233001F1A8F4213019F1223029F1F0E0EE0FFF1FEE58FF4FA591B4912FB7F894EC91811126C090959E239C932FBF08952730A9F02830C9F0243049F7209180002F7D03C0209180002F7720938000DFCF24B52F7724BDDBCF24B52F7DFBCF2091B0002F772093B000D2CF2091B0002F7DF9CF9E2BDACF3FB7F8948091050190910601A0910701B091080126B5A89B05C02F3F19F00196A11DB11D3FBFBA2FA92F982F8827BC01CD01620F711D811D911D42E0660F771F881F991F4A95D1F708958F929F92AF92BF92CF92DF92EF92FF920E94B8004B015C0184E6C82ED12CE12CF12C0E94B800681979098A099B09683E734081059105A8F321E0C21AD108E108F10888EE880E83E0981EA11CB11CC114D104E104F10429F7FF90EF90DF90CF90BF90AF909F908F9008951F920F920FB60F9211242F933F938F939F93AF93BF938091010190910201A0910301B09104013091000123E0230F2D3758F50196A11DB11D209300018093010190930201A0930301B09304018091050190910601A0910701B09108010196A11DB11D8093050190930601A0930701B0930801BF91AF919F918F913F912F910F900FBE0F901F90189526E8230F0296A11DB11DD2CF789484B5826084BD84B5816084BD85B5826085BD85B5816085BD80916E00816080936E00109281008091810082608093810080918100816080938100809180008160809380008091B10084608093B1008091B00081608093B00080917A00846080937A0080917A00826080937A0080917A00816080937A0080917A00806880937A001092C100EDE9F0E02491E9E8F0E08491882399F090E0880F991FFC01E859FF4FA591B491FC01EE58FF4F859194918FB7F894EC91E22BEC938FBFC0E0D0E081E00E9470000E94DD0080E00E9470000E94DD002097A1F30E940000F1CFF894FFCFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# Blink_chass = '0C945C000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C9413010C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E0000000000240027002A0000000000250028002B0004040404040404040202020202020303030303030102040810204080010204081020010204081020000000080002010000030407000000000000000011241FBECFEFD8E0DEBFCDBF21E0A0E0B1E001C01D92A930B207E1F70E945D010C94CC010C940000E1EBF0E02491EDE9F0E09491E9E8F0E0E491EE23C9F0222339F0233001F1A8F4213019F1223029F1F0E0EE0FFF1FEE58FF4FA591B4912FB7F894EC91811126C090959E239C932FBF08952730A9F02830C9F0243049F7209180002F7D03C0209180002F7720938000DFCF24B52F7724BDDBCF24B52F7DFBCF2091B0002F772093B000D2CF2091B0002F7DF9CF9E2BDACF3FB7F8948091050190910601A0910701B091080126B5A89B05C02F3F19F00196A11DB11D3FBFBA2FA92F982F8827BC01CD01620F711D811D911D42E0660F771F881F991F4A95D1F708958F929F92AF92BF92CF92DF92EF92FF920E94B8004B015C0188EEC82E83E0D82EE12CF12C0E94B800681979098A099B09683E734081059105A8F321E0C21AD108E108F10888EE880E83E0981EA11CB11CC114D104E104F10429F7FF90EF90DF90CF90BF90AF909F908F9008951F920F920FB60F9211242F933F938F939F93AF93BF938091010190910201A0910301B09104013091000123E0230F2D3758F50196A11DB11D209300018093010190930201A0930301B09304018091050190910601A0910701B09108010196A11DB11D8093050190930601A0930701B0930801BF91AF919F918F913F912F910F900FBE0F901F90189526E8230F0296A11DB11DD2CF789484B5826084BD84B5816084BD85B5826085BD85B5816085BD80916E00816080936E00109281008091810082608093810080918100816080938100809180008160809380008091B10084608093B1008091B00081608093B00080917A00846080937A0080917A00826080937A0080917A00816080937A0080917A00806880937A001092C100EDE9F0E02491E9E8F0E08491882399F090E0880F991FFC01E859FF4FA591B491FC01EE58FF4F859194918FB7F894EC91E22BEC938FBFC0E0D0E081E00E9470000E94DD0080E00E9470000E94DD002097A1F30E940000F1CFF894FFCFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# Blink_fast1 = '0C945C000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C9412010C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E000C946E0000000000240027002A0000000000250028002B0004040404040404040202020202020303030303030102040810204080010204081020010204081020000000080002010000030407000000000000000011241FBECFEFD8E0DEBFCDBF21E0A0E0B1E001C01D92A930B207E1F70E945C010C94CB010C940000E1EBF0E02491EDE9F0E09491E9E8F0E0E491EE23C9F0222339F0233001F1A8F4213019F1223029F1F0E0EE0FFF1FEE58FF4FA591B4912FB7F894EC91811126C090959E239C932FBF08952730A9F02830C9F0243049F7209180002F7D03C0209180002F7720938000DFCF24B52F7724BDDBCF24B52F7DFBCF2091B0002F772093B000D2CF2091B0002F7DF9CF9E2BDACF3FB7F8948091050190910601A0910701B091080126B5A89B05C02F3F19F00196A11DB11D3FBFBA2FA92F982F8827BC01CD01620F711D811D911D42E0660F771F881F991F4A95D1F708958F929F92AF92BF92CF92DF92EF92FF920E94B8004B015C0184E6C82ED12CE12CF12C0E94B800681979098A099B09683E734081059105A8F321E0C21AD108E108F10888EE880E83E0981EA11CB11CC114D104E104F10429F7FF90EF90DF90CF90BF90AF909F908F9008951F920F920FB60F9211242F933F938F939F93AF93BF938091010190910201A0910301B09104013091000123E0230F2D3758F50196A11DB11D209300018093010190930201A0930301B09304018091050190910601A0910701B09108010196A11DB11D8093050190930601A0930701B0930801BF91AF919F918F913F912F910F900FBE0F901F90189526E8230F0296A11DB11DD2CF789484B5826084BD84B5816084BD85B5826085BD85B5816085BD80916E00816080936E00109281008091810082608093810080918100816080938100809180008160809380008091B10084608093B1008091B00081608093B00080917A00846080937A0080917A00826080937A0080917A00816080937A0080917A00806880937A001092C100EDE9F0E02491E9E8F0E08491882399F090E0880F991FFC01E859FF4FA591B491FC01EE58FF4F859194918FB7F894EC91E22BEC938FBFC0E0D0E081E00E9470000E94DD0080E00E9470000E94DD002097A1F30E940000F1CFF894FFCFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# 
# text_message = 'Hello World!'

#==========================Set up===================================#
# OLED size
WIDTH = 128
HEIGHT = 64
# Set the update time (hour)
Update_time = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0)
# Set the position you what to update
BK_B1 = (10.771903, 106.658514) #HCMUT B1
HOME = (10.874118, 106.745708) #cafe khiet tam
UpdateLocation = HOME

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) # for module SIM7600E
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5)) # for ATmega328P
resetPin = Pin(3, Pin.OUT) # for reset pin of ATmega328P

i2c_oled = I2C(1, scl = Pin(27), sda = Pin(26), freq = 400000) # for oled
i2c_rtc = I2C(0, scl = Pin(17), sda = Pin(16), freq = 400000) # for rtc

rtc = DS1307(i2c_rtc)
display = SSD1306_I2C(128, 64, i2c_oled)


#___________________________________________________________________#

#==============================[ ISP command ]========================================#
def resetMCU():
	resetPin.value(0)
	time.sleep(0.05)
	resetPin.value(1)
	time.sleep(0.15)
	resetPin.value(0)
	time.sleep(0.05)
	resetPin.value(1)
	time.sleep(0.15)

def sendByte(lists):
    data = bytes(lists)
    uart1.write(data)
    print('Data sent')
    print(data)
    rxDataISP = bytes()
    rxDataISP = b''
    time.sleep(0.5)
    current_time = time.time()
    while uart1.any() > 0:
        rxDataISP += uart1.read(1)
    time.sleep(0.5)
    ret = list(rxDataISP)
    print('MCU Reply:')
    print(rxDataISP)
    return ret

def getSync():
	cmd = [0x30, 0x20]
	return sendByte(cmd)

def setProg():
    cmd = [0x42, 0x86, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x03, 0xff, 0xff, 0xff, 0xff, 0x00, 0x80, 0x04, 0x00, 0x00, 0x00, 0x80, 0x00, 0x20]
    return sendByte(cmd)

# set Device extend
def setProgEx():
    cmd = [0x45, 0x05, 0x04, 0xd7, 0xc2, 0x00, 0x20]
    return sendByte(cmd)

# Enter Program mode
def enterProgMode():
    cmd = [0x50, 0x20]
    return sendByte(cmd)

# Get signature
def getSignature():
    cmd = [0x75, 0x20]
    sign = sendByte(cmd)
    signature = sign[1:-1:1]
    for s in range(len(AVR_signature)):
        if AVR_signature[s] == signature:
            return 'model: {}'.format(AVR_model[s])
    return 'Unknown model (signature {}), please check again'.format(signature)

# Universal:
def universal():
    # head = [0x56, 0x30, 0x00, 0x00, 0x00, 0x20]
    head = [0x56]
    tail = [0x00, 0x20]
    cmd = [[0x30, 0x00, 0x00], [0x30, 0x00, 0x01], [0x30, 0x00, 0x02], [0xac, 0x80, 0x00]]
    log = []
    for i in cmd:
        cmd_config = head + i + tail
        ret = sendByte(cmd_config)
    return ret

# Leave Program mode
def exProgMode():
    cmd = [0x51, 0x20]
    return sendByte(cmd)


def IncreaseAddress(addr):
    addr[0] += 0x40
    if addr[0] >255:
        addr[0] = 0x00
        addr[1] += 0x01
    return addr

def loadAddress(addr):
    head = [0x55]
    tail = [0x20]
    load_addr = head + addr + tail
    return sendByte(load_addr)

def flashPage(data):
    head = [0x64, 0x00, 0x80,0x46]
    tail = [0x20]
    flash_page = head + data + tail
    return sendByte(flash_page)

# Read page on microchip
def readPage(count):
    read_addr = [0x00 ,0x00]
    cmd = [0x74, 0x00, 0x80, 0x46, 0x20]
    read_page =[]
    for i in range(count):
        loadAddress(read_addr)
        page_raw = sendByte(cmd)
        read_page.append(page_raw[1:-1:1])
        IncreaseAddress(read_addr)
    return read_page

def compare(page, block):
    log = []
    print('comparing')
    for i in range(len(page)):
        if page[i] != block[i]:
            log.append('Verification Error: page[{}] != block[{}] #####{} $$$ {}#####'.format(i,i,page[i],block[i]))
            for j in range(len(page[i])):
                if page[i][j] != block[i][j]:
                    log.append('First mismatch at byte {} :  {} != {} '.format(i*128+j, hex(page[i][j]), hex(block[i][j])))
                    break
            break
    print('End compare')
    return log

#===========================================================================
def start_Prog():
	resetMCU()
	print('get Sync')
	print(getSync())
	print('Set Prog')
	print(setProg())
	print('Set ProgEx')
	print(setProgEx())
	# print('Chip is being erased')
	# print(universal())
	print('Set Prog')
	print(setProg())
	print('Set ProgEx')
	print(setProgEx())
	print('Enter Programming session')
	print(enterProgMode())
	print('Get MCU signature: ')
	print(getSignature())
	# print('Chip is being erased')
	# print(universal())

def end_Prog():
	print('Exit Programming mode')
	print(exProgMode())
	print('Hard reset MCU')
	resetMCU()

def AVR_ISP(hex_data):
	addr = [0x00, 0x00]
	add_count = len(hex_data)
	print('Enter Programming mode:')
	start_Prog()
	for i in range(len(hex_data)):
		print('Flash page at address: {}  {}'.format(hex(addr[0]),hex(addr[1])))
		print(loadAddress(addr))
		flashPage(hex_data[i])
		IncreaseAddress(addr)
	Page = readPage(add_count)
	print(compare(Page, hex_data))
	end_Prog()


#==============================[ Connect ]========================================#
def connectFTP():
    StartFTP()
    LoginFTPServer('ftp.drivehq.com', '21', 'mh1911200', '98027435610', '0')
    utime.sleep(4)
    ChangeDir('Firmware_Updates')
    utime.sleep(2)
    ChangeDir('Firmware_Updates')
    utime.sleep(2)
def disconnectFTP():
    LogoutFTPServer()
    utime.sleep(2)
    StopFTP()
#=========================[ Check the version ]====================================#
def check_version():
    display.fill(0)
    display_status()
    display.text('Checking version',0,50)
    display.show()
    #Take current version index
    SelectDir('F:/')
    device_ver = ''
    ListDirFile('0')
    rx_device_ver_str = TransFileCMD_Full('F:/version.txt')
    rx_device_ver_list = rx_device_ver_str.split("\r\n")
    device_ver = rx_device_ver_list[2][17:len(rx_device_ver_list[2])]
    print('The version on this device now is: ' + device_ver)

    #Download version file
    SelectDir('F:/')
    DeleteFile('version.txt')
    ListDirFile('0')
    connectFTP()
    utime.sleep(1)
    downloadFromFTP('version.txt')
    utime.sleep(2)
    disconnectFTP()
    ListDirFile('0')

    #Send to RPi Pico
    # SelectDir('F:/')
    ftp_ver = ''
    rx_ftp_ver_str = TransFileCMD_Full('F:/version.txt')
    rx_ftp_ver_list = rx_ftp_ver_str.split("\r\n")
    ftp_ver = rx_ftp_ver_list[2][17:len(rx_ftp_ver_list[2])]
    print('The version on FTP server now is: ' + ftp_ver)
    if int(ftp_ver) > int (device_ver):
        display.fill(0)
        display_status()
        display.text('Need to update',0,50)
        display.show()
        print('You need to update the firmware of your device!')
        utime.sleep(1)
        return True
    else:
        print('The device is running with the newest firmware.')
        return False
#__________________________________________________________________________________#
# 
#=========================[ Download and pack the new firmware ]===================#
def TakeNewFirmware():
    display.fill(0)
    display.text('GetNewFirmware',0,50)
    display.show()
    display_status()
    SelectDir('F:/')
    DeleteFile('firmware.ino.hex')#Delete current file of firmware
    ListDirFile('0')
    connectFTP()
    downloadFromFTP('firmware.ino.hex')
    utime.sleep(2)
    disconnectFTP()
    ListDirFile('0')
    display.fill(0)
    display.text('Downloaded',0,50)
    display.show()
    display_status()
    print('New firmware is downloaded.')
    
    #Take file from 7600E and get all the string received
    rx_firmware_str =''
    rx_firmware_str = GetRxHexStr('F:/'+'firmware.ino.hex')

    #Create the Package
    f_package =''
    f_package = GetDataPackage(rx_firmware_str)
    print(f_package)
    
    return f_package

# new_firmware = ''
# if int(ftp_ver) > int (device_ver):
#     new_firmware = TakeNewFirmware()
# print('new firmware:',new_firmware)
#__________________________________________________________________________________#
# 
#=========================[ Check the status of the device ]=======================#
#Appropriate time to update:
def check_time():
    display.fill(0)
    display_status()
    print('checking time...')
    arr = rtc.datetime()
    hour = arr[4]
    minute = arr[5]
    if hour in Update_time:
        display.text('Time: OK',0,50)
        display.show()
        print('Time is OK')
        return True
    else:
        display.text('Time: not OK',0,50)
        display.show()
        print('It is not time to update')
        return False

#Speed
def check_speed():
    print('checking speed...')
    current_speed1 = GetSpeed()
    time.sleep(2)
    current_speed2 = GetSpeed()
    if current_speed1 > 0 and current_speed2 > 0:
        display.fill(0)
        display_status()
        display.text('Speed: not OK',0,50)
        display.show()
        print('The vehicle is running')
        return False
    else:
        display.fill(0)
        display_status()
        display.text('Speed: OK',0,50)
        display.show()
        print('The vehicle is stopped')
        return True
        
#Location
def check_location():
    display.fill(0)
    display_status()
    print('checking location...')
    response = GetGPSinfo()
    response_list = response.split("\r\n")
    if len(response_list[1]) == 19:
        return True
    else:
        y = ReadPosition(response) #Extract latitude and longitude
        lat = y[0]
        lon = y[1]
        dist = ReadDistance(UpdateLocation[0], UpdateLocation[1], lat, lon)
        if dist <= 1000:
            display.text('Location: OK',0,50)
            display.show()
            print('The vehicle is in update allowed area')
            return True
        else:
            display.text('Location: not OK',0,50)
            display.show()
            print('The vehicle is not in update allowed area')
            return False
    
def check_status():
    display.fill(0)
    display_status()
    display.text('Checking State',0,50)
    display.show()
    if check_location() == True and check_speed() == True and check_time() == True:
        utime.sleep(1)
        display.fill(0)
        display_status()
        display.text('State: OK',0,50)
        display.show()
        print('The status is ready to update')
        return True
    else:
        display.fill(0)
        display_status()
        display.text('State: not OK',0,50)
        display.show()
        print('The status is not ready to update')
        return False      
#__________________________________________________________________________________#

#=================================[ Flashing ]=====================================#
def flash_to_MCU(f_package):
    display.fill(0)
    display_status()
    display.text('Start Flashing',0,50)
    display.show()
    resetPin.value(1)
    time.sleep(5)
    print('Enter flashing operation...')
    pre_data = bytes()
    pre_data = b''
    data = DP.FormatData(f_package)
    AVR_ISP(data)
    display.fill(0)
    display_status()
    display.text('Finish Flashing',0,50)
    display.show()
    time.sleep(2)
#__________________________________________________________________________________#

#===========================[ Display the status ]=================================#
def display_status():
    # Date Time
    arr = rtc.datetime()
    RTC_time = str(arr[2]) + '-' + str(arr[1]) + '-' + str(arr[0]) + '  ' + str(arr[4]) + ':' + str(arr[5])
    display.text(RTC_time,0,0)
    # Position and distance
    response = GetGPSinfo()
    while len(response) < 19:
        print('Waiting 7600E')
        utime.sleep(3)
        response = GetGPSinfo()
    utime.sleep(2)
    response = GetGPSinfo()    
    response_list = response.split("\r\n")
    if len(response_list[1]) == 19:
        display.text('lat: not ready',0,10)
        display.text('lon: not ready',0,20)
    else:
        y = ReadPosition(response) #Extract latitude and longitude
        lat = y[0]
        lon = y[1]
        lat_str = 'lat:' + str(y[0])
        lon_str = 'lon:' + str(y[1])
    #     position = lat_str + ',' + lon_str
        display.text(lat_str,0,10)
        display.text(lon_str,0,20)
        dist = ReadDistance(UpdateLocation[0], UpdateLocation[1], lat, lon)
        dist_str = 'Dist: ' + str(dist/1000) +'km'
        display.text(dist_str,0,30)
    # Speed
    current_speed = 'RPM: ' + str(GetSpeed())
    display.text(current_speed,0,40)
    
    display.show()

#__________________________________________________________________________________#
    
#=================================[ Main ]=====================================#
while True:
    utime.sleep(2)
    resetPin.value(1)
    display.fill(0)
    display_status()
    display.text('Checking Version',0,50)
    display.show()
    print('Checking version on FTP server...')
    have_new_version = check_version()
    utime.sleep(1)
    if have_new_version == True:
        print('Downloading firmware from FTP server...')
        utime.sleep(1)
        f_package = TakeNewFirmware()
        utime.sleep(1)
        
        have_new_package = True
        
        while have_new_package == True:
            ready_update = check_status()
            if ready_update == True:
                flash_to_MCU(f_package)
                have_new_package = False
                utime.sleep(1)
                display_status()
            else:
                display.fill(0)
                display.text('WaitingToUpdate',0,50)
                display.show()
                display_status()
                utime.sleep(3)
    else:
        display.fill(0)
        display.text('RunningNewestVer',0,50)
        display.show()
        display_status()
        utime.sleep(30)

# while True:
#     
# display_status()
# check_time()
# check_speed()
# print(check_speed())
# print(check_location())
# check_status()
# time.sleep(5)
# resetPin.value(1)
# print(GetSpeed())

#______________________________________________________________________________#




