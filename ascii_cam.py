import curses
import glob

from PIL import Image
import cv2


def set_screen() -> curses.window:
    """ Initializes curses screen/window. Returns curses.window object."""
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.nodelay(False)
    return screen


def set_camera(image_size: tuple[int | float, int | float] = (160, 120)) -> cv2.VideoCapture:
    """
    Opens first available video capturing device and sets its resolution based on image_size tuple.
    Returns cv2.VideoCapture object.
    """
    for dev_number, _ in enumerate(glob.glob("/dev/video?")):
        camera = cv2.VideoCapture(dev_number)
        if camera.isOpened():
            break
    width, height = image_size
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return camera


def image2ascii(image: Image, size: tuple[int | float, int | float], ascii_map: list | str) -> str:
    """Yields line by line of ascii picture of the given size"""
    ascii_map_len = len(ascii_map)
    img = image.resize(size)
    line_len, _ = size
    line = ""
    for idx, pixel in enumerate(img.getdata(), 1):
        line += ascii_map[int((pixel * ascii_map_len) / 256)]
        if idx % line_len == 0:
            yield line
            line = ""


ASCII_MAP = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`'. """  # noqa

if __name__ == "__main__":
    cam = set_camera()
    scr = set_screen()
    try:
        while True:
            ret, cam_grab = cam.read()
            if ret:
                img_cam = Image.fromarray(cv2.cvtColor(cam_grab, cv2.COLOR_RGB2GRAY))
                scr_y, scr_x = scr.getmaxyx()
                for y, line in enumerate(image2ascii(img_cam, (scr_x, scr_y - 1), ASCII_MAP)):
                    scr.addstr(y, 0, line[::-1])
                scr.refresh()
    except KeyboardInterrupt:
        curses.endwin()
