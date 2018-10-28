import serial
import sys
import os
import time, hashlib
from pyfingerprint.pyfingerprint import PyFingerprint


## Note: this script is meant to be run on a python2 compiler

#########################################################################
## Configure serial port settings. Run command $ dmesg to find correct
## ports for sensors. 
## Ex: FOR PULSE OX: cp210x converter now attached to ttyUSB1

## Configuration for the Fingerprinter
ttyF = '/dev/ttyUSB0'
ser = serial.Serial(ttyF,115200)

## Configuration for the Pulse Ox
ttyP = "/dev/ttyUSB1"
s = serial.Serial()
s.baudrate = 115200
s.bytesize = serial.EIGHTBITS
s.parity = serial.PARITY_NONE
s.stopbits = serial.STOPBITS_ONE
s.xonxoff = 1
s.timeout = 1
s.port = ttyP

###########################GLOBALS##############################################
dir = os.getcwd()
finger_path = dir + "/Fingerprinter/examples"
image_path = dir + "/Images"
options = ["e", "d", "v", "i", "c", "s", "x"]
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
##########################FUNCTIONS###############################################
def display_menu():
    print("\n\n________________________________________\n")
    print("Hello. Welcome to your security test.")
    print("Please select one of the following options:")
    print("E: Enroll a new finger.\nD: Delete old finger.")
    print("V: Validate an existing finger.")
    print("I: Get image of fingerprint at certain index.")
    print("C: Check Pulse Ox (SPO) and Heart Rate.")
    print("S: ---Run security test---")
    print("X: Exit")

## Enroll a Finger
def enroll():
    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)
        print('Remove finger...')
        time.sleep(2)
        print('Waiting for same finger again...')
        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)
        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
        ## Creates a template
        f.createTemplate()
        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

## Deletes a Finger
def delete():
    ## Tries to delete the template of the finger
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

## Validates a Finger
def validate():
    ## Tries to search the finger and calculate hash
    granted = False
    try:
        print('Waiting for finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        ## Searchs template
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]
        if ( positionNumber == -1 ):
            print('Invalid finger entry')
            granted = False
        else:
            granted = True
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
        return granted
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

## Gets an image of a finger
def image():
    ## Tries to read image and download it
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        print('Downloading image (this may take a couple of seconds)...')
        imageDestination =  image_path + '/fingerprint.bmp'
        f.downloadImage(imageDestination)
        print('The image was saved to "' + imageDestination + '".')
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

## For evaluating validity of spo2 and pulse rate
def evaluate_ranges(temp_spo2, temp_pulse):
    passed = False;
    ## if the pulse ox is in the range 94-100
    ## and if the heart rate is within the range 55-115
    if (temp_spo2 > 93 and temp_spo2 < 100) and (temp_pulse > 54 and temp_pulse < 116):
            print("\n--------Your spo2 and pulse are within normal ranges--------\n")
            passed = True
    else:
            print("\n--------Your spo2 and pulse are NOT within normal ranges--------\n")
            passed = False
    return passed

## Get HR and Pulse Ox
def spohr():
    ## Wait for finger to be placed on sensor
    s.close()
    s.open()
    enter = raw_input("Press enter when sensor is initialized\n\n")
    # Send data to recieve data
    try:
        s.write(b'\x7d\x81\xa1')
        # get the data, 9 bytes per reading
        d = s.read(9)
        pulse = ord(d[5]) & 0x7f
        spo2 = ord(d[6]) & 0x7f
        print("SPO2 = ", spo2, ", PULSE = ", pulse)
        test = evaluate_ranges(spo2, pulse)
        return test
    except:
        print("There was an error initializing. Is the sensor on?", sys.exc_info()[0])
#########################################################################
while True:
        display_menu()
        selection = raw_input('\nPlease enter an option: ')
        if (selection.lower() == options[0].lower()):
                ## Enroll finger
                enroll()
        elif (selection.lower() == options[1].lower()):
                ## Delete finger
                print("\nSelection: Delete finger\n\n")
                delete()
        elif (selection.lower() == options[2].lower()):
                ## Validate finger
                print("\nSelection: Validate finger\n\n")
                temp = validate()
        elif (selection.lower() == options[3].lower()):
                ## Get an Image
                print("\nSelection: Get image\n\n")
                image()
        elif (selection.lower == options[4].lower):
                ## Get pulse ox and heartrate
                print("\nSelection: SPO and HR\n\n")
                tmp = spohr()
        elif (selection.lower == options[5].lower):
                ## Run Security Test
                # Validate Finger First
                print("\nSelection: Run Security Test\n\n")
                access = validate()
                if access == True:
                    access_granted = spohr()
                    if access_granted == True:
                        print("\n\nCONGRATULATIONS -- ACCESS GRANTED\n\n")
                    else:
                        print("\n\nACCESS DENIED\n\n")
                else:
                   print("\n\nACCESS DENIED\n\n") 
                
        elif (selection.lower == options[6].lower):
                ##Exit
                print("\nGoodbye!\n")
                break
                        
        else:
                print("Invalid entry. Please try again.")
