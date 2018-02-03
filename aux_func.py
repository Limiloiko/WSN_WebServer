# -*- coding: utf-8 -*-
"""
Description:
    This script includes the basic initializations functions:
        
        * config_telegesis: Initialization of the Telegesis USB module.
    
    
    Also the functions to write and read from the USB port are here:
        
        * wait_for_message: Continue read the port until the expedted character 
        arrives.
        
        * write_to_telegesis: Write the data and waits for the 'OK' message 
        from the module.
        
    
    Recursive function is based on threading.Timer class used to execute code 
    repetedly over time.


NOTES:
    * CHANGE DEVICE VARIABLE TO YOUR CURRENTLY CONNECTED TELEGESIS MODULE


TODO:
    * Add exception handlers !


"""

__author__ = 'David Lima (limiloiko@gmail.com)'
__version__ = '1.0'
__all__ = ['port', 'device']

# Standard libraries
import serial                 # USB control
from threading import Timer   # Timer class

# App libraries
from app import db            # Database access
# Tables classes
from app.models import Temperatures, Humidities, Luminosities 


device = "/dev/ttyUSB0"                 # USB device THIS MAY CHANGE!!

port = serial.Serial(                   # USB handle
         device,                
         baudrate=19200,                # Baudrate
         parity=serial.PARITY_NONE, 
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.EIGHTBITS,
         writeTimeout=0,
         timeout=0.05,
         rtscts=False,
         dsrdtr=False,
         xonxoff=False)


def wait_for_message(port, ascii):
    """Wait for message function. Print the received information and blocks 
    the execution until information arrives.
        
    
    Args:
        port    (serial.Serial): USB handle 
        ascii             (str): Expected character to read
        
        
    Raises:
        
        
        
    """
    
    forward = True  
    
    # Exception caused from delay in ZigBee left current PAN
    if ascii not in 'L':
        while forward:
            line = port.readline()    
            
            # Expected message received
            if ascii in line :
                forward = False
                print line
                
    else:
        while forward:
            line = port.readline()
            print line
            
            if 'K' in line:
                forward = False
                print line
                
            # Error due to not be in a PAN
            elif 'E' in line: 
                forward = False
                print line
                
                



def write_to_telegesis(data):
    """Writes the data on the USB and waits OK answer.
    
    """
    
    port.write(data)
    wait_for_message(port, 'K')




def config_telegesis(port):
    """Initializes the Telegesis module, that will act like the coordinator of
    the PAN.
    
    Steps:
        * Left current PAN.
        * Configure Channel mask.
        * Configure SHORT PAN ID
        * Cconfigure Extended PAN ID.
        * Software Reset.
        * Create the PAN.
        
    """
   
    print "Configurating telegesis module...\r"
    
    # Left current PAN
    print "Left current PAN...\r"
    port.write("AT+DASSL\r")
    wait_for_message(port, 'L')
    
    # Channel mask:
    print "Channel Mask to 0x0008...\r"
    write_to_telegesis("ATS00=0008\r")
    
    # PAN short ID:
    print "PAN short ID to 1995...\r"
    write_to_telegesis("ATS02=1995\r")
    
    # PAN Extended ID:
    print "PAN extended ID to 123456789ABCDEF4...\r"
    write_to_telegesis("ATS03=123456789ABCDEF4\r")
  
    # Reset
    print "Software Reset...\r"
    write_to_telegesis("ATZ\r")
  
    # Create the PAN
    print "Create the PAN...\r"
    write_to_telegesis("AT+EN\r")
  
    
  
# Función que se ejecuta recursivamente, la que leera los datos del usb
def recursive():
    """Function that will execute repeadly code to see if we receive messages 
    from the slave node with measurements information. It chackes if valid 
    information is received and updates the Database with new data.
        
    """
    
    forward = True
    
    # Reat until valid information is received
    while forward:
        line = port.readline()
        
        # There is no information in the USB
        if len(line) == 0:
            forward = False
            
        else:
            # Unicast received
            if 'UCAST' in line:
                print line
                
            # Temperature mesaure
            if "t" in line:
                pos = line.find('t')+1          # Position of first value
                data = int(line[pos:pos+2])     # All mesaurement
                print data 
                temp = Temperatures(data=data)  # Database row
                db.session.add(temp)       # Add to currently Database session
                
            # Humiditie measure
            elif "h" in line:    
                pos = line.find('h')+1
                data = int(line[pos:-1])
                print data
                hum = Humidities(data=data)
                db.session.add(hum)
                
            # Luminosity measure
            elif "l" in line:
                pos = line.find('l')+1
                data = int(line[pos:-1])
                print data
                lum = Luminosities(data=data)
                db.session.add(lum)
                
            # Thrass information
            else:
                Timer(0.8, recursive).start()   # Restart timer
                return
            
            db.session.commit()                 # Commit changes in database
                
    Timer(0.8, recursive).start()               # Restart timer
 
    


# Initialize 
config_telegesis(port)
recursive()
    
    

