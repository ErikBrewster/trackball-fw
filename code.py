import busio
import board
import fw
import time
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)
XSCALING = 0.1
YSCALING = -0.1
SAMPLE_PERIOD = 0.01

Product_ID = 0x00
Revision_ID = 0x01
Motion = 0x02
Delta_X_L = 0x03
Delta_X_H = 0x04
Delta_Y_L = 0x05
Delta_Y_H = 0x06
SQUAL = 0x07
Raw_Data_Sum = 0x08
Maximum_Raw_data = 0x09
Minimum_Raw_data = 0x0A
Shutter_Lower = 0x0B
Shutter_Upper = 0x0C
Control = 0x0D
Config1 = 0x0F
Config2 = 0x10
Angle_Tune = 0x11
Frame_Capture = 0x12
SROM_Enable = 0x13
Run_Downshift = 0x14
Rest1_Rate_Lower = 0x15
Rest1_Rate_Upper = 0x16
Rest1_Downshift = 0x17
Rest2_Rate_Lower = 0x18
Rest2_Rate_Upper = 0x19
Rest2_Downshift = 0x1A
Rest3_Rate_Lower = 0x1B
Rest3_Rate_Upper = 0x1C
Observation = 0x24
Data_Out_Lower = 0x25
Data_Out_Upper = 0x26
Raw_Data_Dump = 0x29
SROM_ID = 0x2A
Min_SQ_Run = 0x2B
Raw_Data_Threshold = 0x2C
Config5 = 0x2F
Power_Up_Reset = 0x3A
Shutdown = 0x3B
Inverse_Product_ID = 0x3F
LiftCutoff_Tune3 = 0x41
Angle_Snap = 0x42
LiftCutoff_Tune1 = 0x4A
Motion_Burst = 0x50
LiftCutoff_Tune_Timeout = 0x58
LiftCutoff_Tune_Min_Length = 0x5A
SROM_Load_Burst = 0x62
Lift_Config = 0x63
Raw_Data_Burst = 0x64
LiftCutoff_Tune2 = 0x65



def write(spi, addr, data):
    cs.value = False
    spi.write(bytes([addr | 0x80]))
    #time.sleep(500e-6)
    spi.write(bytes([data]))
    cs.value = True
    #print(f'w {hex(addr)} {hex(data)}')

def read(spi, addr):
    cs.value = False
    result = bytearray(1)
    spi.write(bytes([addr]))
    #time.sleep(100e-6)
    spi.readinto(result)
    cs.value = True
    #print(f'r {hex(addr)} {hex(result[0])}')
    return result

def twos(val_str, bytes):
    import sys
    val = int(val_str, 2)
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)                                                          
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

def readPointer(spi):
    cs.value = False
    write(spi, Motion, 0x01)
    read(spi, Motion)
    xl = read(spi, Delta_X_L)
    xh = read(spi, Delta_X_H)
    yl = read(spi, Delta_Y_L)
    yh = read(spi, Delta_Y_H)
    cs.value = True
    xlnew = ~(xl[0])
    if xlnew < -128:
        xlnew = xlnew + 256
    xhnew = ~(xh[0])
    if xhnew > -128:
        xhnew = xhnew + 256
    ylnew = ~(yl[0])
    if ylnew > 128:
        ylnew = ylnew - 256
    yhnew = ~(yh[0])
    if yhnew > 128:
        yhnew = yhnew - 256

    x = xl[0]+xh[0]*256
    if x > 32767:
        xconverted = x - 65536
    else:
        xconverted = x
    
    y = yl[0]+yh[0]*256
    if y > 32767:
        yconverted = y - 65536
    else:
        yconverted = y
    
    #print(f'{y:#020b} {x:#020b} {xconverted} {yconverted}')
    
    return xconverted, yconverted
    
def uploadFirmware(spi):
    print('Uploading FW')
    
    # Write 0 to Rest_En bit of Config2 register to disable Rest mode.
    write(spi, Config2, 0x0)
    # write 0x1d in SROM_enable reg for initializing
    write(spi, SROM_Enable, 0x1d)
    # wait for more than one frame period (assume 100 Hz)
    time.sleep(0.01)
    # write 0x18 to SROM_enable to start SROM download
    write(spi, SROM_Enable, 0x18)
    # write the SROM file (=firmware data)
    
    
    cs.value = False
    spi.write(bytes([SROM_Load_Burst | 0x80]))
    time.sleep(0.001)
    

    # send all bytes of the firmware
    for myByte in fw.PROGMEM1:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM2:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM3:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM4:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM5:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM6:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM7:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM8:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM9:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM10:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM11:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM12:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM13:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM14:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM15:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM16:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM17:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM18:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM19:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM20:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM21:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM22:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM23:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM24:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM25:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM26:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM27:    
        spi.write(bytes([myByte]))
    for myByte in fw.PROGMEM28:    
        spi.write(bytes([myByte]))


    cs.value = True
    
    # Read the SROM_ID register to verify the ID before any other register reads or writes.
    id = read(spi, Product_ID)

    # Write 0x00 to Config2 register for wired mouse or 0x20 for wireless mouse design.
    write(spi, Config2, 0x00)

    # set initial CPI resolution
    write(spi, Config1, 0x15)
    

def startup(spi):
    id = read(spi, Product_ID)
    
    write(spi, Power_Up_Reset, 0x5a) # force reset
    time.sleep(0.05)
    
    read(spi, Motion)
    read(spi, Delta_X_L)
    read(spi, Delta_X_H)
    read(spi, Delta_Y_L)
    read(spi, Delta_Y_H)
    uploadFirmware(spi)
    time.sleep(0.01)
    
    id = read(spi, Product_ID)
    
    revision = read(spi, Revision_ID)
    

cs = digitalio.DigitalInOut(board.GP17)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

spi = busio.SPI(clock=board.GP18, MISO=board.GP16, MOSI=board.GP19)

# try.lock locks the SPI bus so we can access the sensor
# for our sole use
while not spi.try_lock():
    pass

spi.configure(baudrate=5000000, phase=1, polarity=1)

startup(spi)

try:
    xSum = 0
    ySum = 0
    while True:
        x, y = readPointer(spi)
        xSum += x * XSCALING
        ySum += y * YSCALING
        xMove = round(xSum)
        yMove = round(ySum)
        #print(f'{x} {xSum} {xMove} {xSum - xMove}')
        xSum = xSum - xMove
        ySum = ySum - yMove
        mouse.move(x=int(xMove), y=int(yMove))
    
        time.sleep(SAMPLE_PERIOD)

finally:  # unlock the spi bus when ctrl-c'ing out of the loop
    spi.unlock()