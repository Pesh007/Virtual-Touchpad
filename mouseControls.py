import ctypes
from pathlib import Path


dll = ctypes.CDLL(str(Path(__file__).parent / "mouseControls.dll"))

def move_mouse(x: int, y: int):
    dll.MoveCursor.argtypes = (ctypes.c_int, ctypes.c_int)
    dll.MoveCursor.restype = None
    dll.MoveCursor(x, y)

def left_click():
    dll.LeftClick.argtypes = None
    dll.LeftClick.restype = None
    dll.LeftClick()


def vertical_scroll(amount: int):
    dll.ScrollVertical.argtypes = [ctypes.c_int]
    dll.ScrollVertical.restype = None
    dll.ScrollVertical(amount)    


def horizontal_scroll(amount: int):
    dll.ScrollHorizontal.argtypes = [ctypes.c_int]
    dll.ScrollHorizontal.restype = None
    dll.ScrollHorizontal(amount)
