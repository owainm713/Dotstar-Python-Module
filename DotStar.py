"""DotStar, python module to use DotStar LEDs,
python version

created February 11, 2023
modified February 11, 2023"""

import time, spidev

class DotStar:
    
    def __init__(self, cs, numLEDs, brightness = 3, baudrate = 100000, auto_write = False):

        # set up SPI connection details
        self.spi=spidev.SpiDev()
        self.spi.open(0,cs)  # open spi port 0, device (CS) 1
        self.spi.max_speed_hz = baudrate #100000 #4000000

        # initialize list to hold individual LED colour & brightness details
        # initially set to all off and default brightness (as indicated by the -1)
        # (R, G, B, Brightness)        
        #self.dotList = [(0,0,0) for x in range(numLEDs)]
        self.dotList = [(0,0,0, -1) for x in range(numLEDs)]
        
        self.brightness = brightness
        self.auto_write = auto_write
        
        return
        
    def __setitem__(self, key, value):
        """__setitem__, function to set an indivdual or
        a range of LEDs values in the dotstar pixel list"""
        
        self.dotList[key] = value
        if self.auto_write == True:
            self.show()
            
        return
        
    def __getitem__(self, key):
        """__getitem__, function to get/return an indivdual or
        a range of LEDs values from the dotstar pixel list"""
        
        return self.dotList[key]
    
    def fill(self, colour, step = 1):
        """fill, function to set the dotstar pixel list
        to all the same colour"""       
        
        for i in range(0, len(self.dotList), step):
            self.dotList[i] = colour

        if self.auto_write == True:
            self.show()
            
        return 
    
    def show_v1(self, brightness = None):
        """show, function to write the pixel data to
        the LEDs to update/show the new values"""
        
        dataList = []
        numLEDs = len(self.dotList)
        
        if brightness == None:
            brightness = self.brightness
        brightness = 0xE0 | brightness
        
        # first part of LED frame consists of 3 1-bits and 5 brightness bits (i.e. 111bbbbb)
        for p in self.dotList:
            dataList.extend([brightness, p[2], p[1], p[0]])
        
        dataList[:0] = [0,0,0,0] # 32 bit 0 start frame
        if numLEDs < 64:
            dataList.extend([0x03, 0x00]) # end frame
        else:
            dataList.extend([0xFF, 0XFF, 0XFF, 0XFF]) # end frame

        dataTransfer = bytearray(dataList) # creates buffer object             
        self.spi.xfer2(dataTransfer)
        
        return
    
    def show(self, brightness = None):
        """show, function to write the pixel data to
        the LEDs to update/show the new values"""
        
        dataList = [] # list containing all formatted data to send to dotstar string
        numLEDs = len(self.dotList)        
        
        # first part of LED frame consists of 3 1-bits and 5 brightness bits (i.e. 111bbbbb)
        # go through each LED/pixel(p) and add the 4 bytes of data for each
        # to the dataList in the right order
        for p in self.dotList:
            if p[3] == -1:
                if brightness != None:
                    brightness = 0xE0 | brightness
                else:
                    brightness = 0xE0 | self.brightness
            else:
                brightness = 0xE0 | p[3]
                
            dataList.extend([brightness, p[2], p[1], p[0]])
        
        # add 4 byte/32 bit start frame to beginning of dataList
        dataList[:0] = [0,0,0,0] # 32 bit 0 start frame

        # add end frame to dataList, size dependent on number
        # of LEDs in string
        if numLEDs < 64:
            dataList.extend([0x03, 0x00]) # end frame
        else:
            dataList.extend([0xFF, 0XFF, 0XFF, 0XFF]) # end frame

        # write data out to dotstar string
        dataTransfer = bytearray(dataList) # creates buffer object             
        self.spi.xfer2(dataTransfer)
        
        return
        
if __name__ == "__main__":

    # initialize dotstar object
    dots = DotStar(cs = 1, numLEDs = 64)

    # delay between effects
    delay = 1
    mode = 2

    time.sleep(3)
    
    if mode == 1:
        dots[35] = (150, 150, 0)
        dots.show_v1()
        time.sleep(delay)
        dots.fill((0,150,0))
        dots.show_v1(brightness = 15)
        time.sleep(delay)
        dots[8:15] = [(0, 0, 150)] * 8
        dots.show_v1()
        time.sleep(delay)
        dots.fill((0,0,0))
        dots.show_v1()
        print('done')
    elif mode == 2:
        # set first 32 LED to green at minimal (1) brightness
        for i in range(0,32):
            dots[i] = (0, 150, 0, 1)

        # set next 32 LEDs to green at maximum (31) brightness
        for i in range(32,64):
            dots[i] = (0, 150, 0, 31)
        dots.show()
        time.sleep(delay*2)

        # set all LEDS to red at default brightness
        dots.fill((150,0,0,-1))
        dots.show()
        time.sleep(delay)
        
        # change default brightness to 15
        dots.brightness = 15
        
        # set LEDs 8-14 to blue at default brightness
        dots[8:15] = [(0, 0, 150, -1)] * 8    
        dots.show()
        time.sleep(delay)
        
        # change current brightness to 9 of 31
        dots.show(brightness = 9)
        time.sleep(delay)
        
        # print current colour & brightness value for
        # LED 31
        print(dots[31])

        # alternate method of turning LEDS off
        # but still maintaining last colour values
        #dots.show(brightness = 0)
        #time.sleep(delay)
        #dots.show()
        #time.sleep(delay)
        
        # turn off all LEDs        
        dots.fill((0,0,0,0))
        dots.show()
        print('done')
        
        
        
