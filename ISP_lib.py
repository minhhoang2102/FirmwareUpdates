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

#=====================================================
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