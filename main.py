import datetime
import sys
import re
import time
from argparse import ArgumentParser

import cv2
import mss
import pytesseract

from analytics import Analytics


def getData():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 118, "left": 1340, "width": 700, "height": 29}
        output = 'testi'
        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    img = cv2.imread('testi')

    config = ('-l eng --oem 1 --psm 3')

    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    text = pytesseract.image_to_string(img, config=config)

    # Check if we are somewhat reading at the right spot.
    if 'Accuracy' not in text:
        print('Cannot read keybr.')
        exit(1)
        
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[^0-9.\s]', '', text)
    text = re.sub(r'\s+', ' ', text) # handle multiple spaces
    text = re.sub(r'^\s+', '', text) # remove leading whitespace
    text = re.sub(r'\s+$', '', text) # remove trailing whitespace
    
    return text # remove space in front

def appendToFile(line):
    f = open("scores.txt", "a")
    f.write(line)
    f.close()

def readLastLine():
    with open('scores.txt', 'r') as f:
        last_line = f.readlines()[-1]
    return last_line

def runListener():
    while True:
        last = readLastLine()[20:].replace('\n', '') # remove time and linebreak
        new = last
        while last == new: 
            new = getData() # get new data
            time.sleep(1)

        if len(new) != 0:
            Analytics().feedback(new)
            appendToFile(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} {new}\n')

            # print(f'write {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} {new}')

if __name__ ==  '__main__':

    if len(sys.argv) == 1:
        print('-r\tview report\n-g\tgraph\n-l\tlistener mode')
        exit(0)

    match sys.argv[1]:
        case '-g':
            Analytics().graph()
        case '-l':
            runListener()
        case '-r':
            Analytics().report()
        case _:
            exit(0)

