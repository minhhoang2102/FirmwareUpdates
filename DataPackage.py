import math
#This module is used to transform a "Data" package that will be flash into ATmega328P
#Input: a raw HEX string (example: file_hex = ''':100000000C945C000C946E000C946E000C946E00CA''')
#Output: a string including "Data" and added '0xFF' if it's necessary to make a perfect page when flashing (128 bytes)

#Make lists of "Record" without ':' and checksum
def ListData_noChecksum(list_raw):
    data = []
    for i in range(len(list_raw)):
        data.append(list_raw[i][1:-2])
    return data

#List "Record" of HEX file by '\n' and do not include '\n' in each part
def ListData(FileHex):
    return FileHex.splitlines()

#Extract "Data" strings of "Records" in lists
def extractData(start, stop, raw_data):
    data = []
    recent_addr = int(raw_data[0][3:7], 16)
    bytes_count = int(raw_data[0][1:3], 16)
    for i in range(len(raw_data)):
        a = raw_data[i]
        if a[8] == '0':
            current_addr = int(a[3:7], 16)
            if recent_addr == current_addr:
                fill_count = 0
            else:
                fill_count = current_addr - recent_addr - bytes_count
            #print('address {} to {} fill {} times'.format(recent_addr, current_addr, fill_count))
            data.append('FF'*fill_count)
            data.append(a[start:stop])
            recent_addr = current_addr
            bytes_count = int(a[1:3], 16)

    while ("" in data):
        data.remove("")
    return data

#Create package of "Data" before flash
def JoinHexPackage(ListedData):
    #Extract "Data" part for each "Record" of listed HEX file 
    ExData = extractData(9, -2, ListedData)
    
    #Join "Data" lists in a string
    DataStr = ''
    for i in range(len(ExData)):
        DataStr += ExData[i];
        
    #Calculate pages that needs to be flashed and insert '0xFF'
    SizeOfDataStr = int(len(DataStr)/2)
    #print('Size of Data: ', SizeOfDataStr, 'bytes')
    NumOfPage = math.ceil(SizeOfDataStr/128)
    #print('Numbers of Pages will be flashed: ', NumOfPage)
    NumOf0xFF = NumOfPage*128 - SizeOfDataStr
    #print('Numbers of 0xFF need to insert: ' + '128x' + str(NumOfPage) + ' - ' + str(SizeOfDataStr) + ' =', NumOf0xFF)
    F_str = ''
    for j in range(NumOf0xFF):
                    F_str += 'FF'
    DataStr += F_str
    return DataStr

#Get perfect package which is used to flash
def GetDataPackage(FileHex):
    ListsOfRecords = ListData(FileHex)
    #print(extractData(9, -2, ListsOfRecords))
    DataPackage = JoinHexPackage(ListsOfRecords)
    return DataPackage


