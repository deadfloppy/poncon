# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
#
#  Copyright (c) 2020 deadfloppy
#  Most of this file is a rewritten pongoOS script
#  Full credit to checkra1n team


import usb
import usb.core
from sys import exit, argv


helpmsg = """poscon - a simple pseudoshell/command sender for pongoOS 
Usage: poscon [arguments] 
    or poscon

Arguments:
-h\t\tShow this message
-c [CMD]\tSend command and exit            
-s\t\tStart sending commands            
            """

class Console:
    def __init__(self,mode='s'):
        self.dev = None
        if self.findDevice() != 0:
            print("Aborting")
            exit(1)
        if mode=='s':
            self.openConsole()
            

    def findDevice(self):
        self.dev = usb.core.find(idVendor=0x05ac, idProduct=0x4141)
        if self.dev is None:
            print("Couldn\'t find the device")
            return 1
        
        try:
            self.dev.set_configuration()
        except:
            print("Couldn\'t set configuration")
            return 1
        
        print("Sending commands is available\n")
        return 0

    def openConsole(self):
        print("Type \'exit\' to stop")
        cmd = ""
        while True:
            cmd = input("console: ")
            if cmd == "":
                print("Cowardly refusing to send empty commands")
            elif cmd == "exit":
                break
            else:
                self._ctrltfr(cmd)
        print("Closing\n")
        exit(0)

    # A rewrite of the pyusb ctrl_transfer for simplicity
    def _ctrltfr(self,command):
        self.dev.ctrl_transfer(0x21, 4, 0, 0, 0)
        self.dev.ctrl_transfer(0x21, 3, 0, 0, command + "\n")


if "__main__" == __name__:
    # Parse arguments
    try:
        if argv[1] == '-h':
            print(helpmsg)
            exit(0)
        elif argv[1].startswith("-c"):
            console = Console(mode='c')
            console._ctrltfr(argv[2])
    except:
        console = Console()
