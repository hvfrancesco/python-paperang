#!/usr/bin/env python3
import config
import hardware
import image_data
import logging
import os
import sys
import tempfile
import time
import traceback
from watchgod import watch
from pathlib import Path


class Paperang_Printer:
    def __init__(self):
        if hasattr(config, "macaddress"):
            self.printer_hardware = hardware.Paperang(config.macaddress)
        else:
            self.printer_hardware = hardware.Paperang()
    
    def print_sirius_image(self, path):
        if self.printer_hardware.connected:
            self.printer_hardware.sendImageToBt(image_data.sirius(path))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    mmj=Paperang_Printer()
    # `sirius-client` will write to this folder
    tmpdir = os.path.join(tempfile.gettempdir(), 'sirius-client')
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    logging.info("tmpdir = " + tmpdir)
    
    for changes in watch(tmpdir):
        while len(changes) > 0:
            change = changes.pop()
            file = change[1]
            print("Printing " + file)
            try:
                if mmj is None:
                    mmj = Paperang_Printer()
                mmj.print_sirius_image(file)
            except Exception as ex:
                print("There was a problem while printing: ", sys.exc_info()[1])
                logging.debug(traceback.format_exc())
                timeout = 15
                print("Trying again in ", timeout, " seconds...")
                time.sleep(timeout)
                print("attempting to reconnect to printer...")
                mmj = None
                changes.add(change)

