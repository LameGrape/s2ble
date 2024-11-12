import keyboard
from pynput.keyboard import Controller, Key
from core import braille
import time

class Typer:
    def __init__(self, encoding: braille.Encoding):
        self.encoding = encoding
        self.heldKeys = set()
        self.suppress = set()
        self.suppressCount = 0

        self.controller = Controller()
        keyboard.hook(self.keyHook)
        keyboard.wait("esc")

    def toByte(self, string):
        binary = "".join(["1" if i in string else "0" for i in "qweruiop"])
        binary = int("".join([str(binary[int(i)]) for i in "32145607"])[::-1], 2)
        return binary
    
    def keyHook(self, key):
        # TODO: figure out why holding down a key backspaces way more than it should
        if key.event_type == "up" and key.name in self.suppress: self.suppress.remove(key.name)
        if key.event_type == "down":
            if key.name in "qwertyuiop":
                had = key.name in self.suppress
                if key.name not in self.suppress:
                    self.controller.tap(Key.backspace) # unga bunga key suppression
                if had: self.suppress.remove(key.name)
                else: self.suppress.add(key.name)
            if key.name == "t": self.controller.tap(Key.backspace)
            if key.name in "qweruiop":
                self.heldKeys.add(key.name)
            if key.name == "y": self.controller.tap(Key.enter)
            return
        
        if key.name == "space" or key.name in "qweruiop":
            if self.suppressCount > 0:
                self.suppressCount -= 1
                return
            if len(self.heldKeys) == 0: return
            if key.name != "space":
                self.suppressCount = len(self.heldKeys) - 1
            char = self.encoding.decodeByte(self.toByte("".join(self.heldKeys)))
            self.heldKeys = set()
            if len(char) == 0: return
            self.controller.type(char)