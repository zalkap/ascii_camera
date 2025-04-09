import curses

from PIL import Image
import cv2


CHARS_MAP = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """


def set_screen():
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.nodelay(False)
    return screen


def set_camera(device_number, image_size):
    camera = cv2.VideoCapture(device_number)
    x, y = image_size
    camera.set(3, x)
    camera.set(4, y)
    return camera


if __name__ == "__main__":
    chars_map_len = len(CHARS_MAP)
    scr = set_screen()
    cam = set_camera(0, (160, 120))
    while True:
        ret, cam_grab = cam.read()
        if ret:
            img_cam = Image.fromarray(cv2.cvtColor(cam_grab, cv2.COLOR_RGB2GRAY))
            scr_y, scr_x = scr.getmaxyx()
            scr_img = img_cam.resize((scr_x, scr_y)).transpose(Image.FLIP_LEFT_RIGHT)
            img_w, img_h = scr_img.size

            img_str = "".join(CHARS_MAP[int((p * chars_map_len) / 256)] for p in scr_img.getdata())
            [scr.addstr(y, 0, img_str[y * img_w:((y * img_w) + img_w)]) for y in range(img_h - 1)]
            scr.refresh()
