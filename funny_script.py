import pyautogui
import webbrowser
import time
import pytesseract
from PIL import ImageGrab
import os
from pynput.mouse import Button, Controller

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

anwsers = {
    'Italia': ('italiano/a', None),
    'Canada': ('canadese', None),
    'Germania': ('tedesco/a', None),
    'Olanda': ('olandese', None),
    'Austria': ('austriaco/a', None),
    'Giappone': ('giapponese', None),
    'Grecia': ('greco/a', None),
    'India': ('indiano/a', None),
    "gli Stati Uniti (d'America)": ('americano/a', None),
    'Portogallo': ('portoghese', None),
    'Svizzera': ('svizzero/a', None),
    'Spagna': ('spagnolo/a', None),
    'Messico': ('messicano/a', None),
    'Svezia': ('svedese', None),
    'Cina': ('cinese', None),
    'Argentina': ('argentino/a', None),
    'Francia': ('francese', None),
    'Polonia': ('polacco/a', None),
    'Irlanda': ('irlandese', None),
    'Corea': ('coreano/a', None),
    'Croazia': ('croato/a', None),
    'Russia': ('russo/a', None),
    'Inghilterra': ('inglese', None),
}

def start_game(start_image):
    x, y = locate_img(start_image)
    pyautogui.click(x, y)

def make_fullscreen(full_screen_image):
    x, y = locate_img(full_screen_image)
    pyautogui.click(x, y)

def pause_game(pause_image):
    x, y = locate_img(pause_image)
    pyautogui.click(x, y)

def locate_img(img):
    while True:
        try:
            location = pyautogui.locateOnScreen(img, confidence=0.7)
            x, y = pyautogui.center(location)
            return x, y
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)

def find_text_position(img, text_to_find, x_offset, y_offset):
    rectangles = [
        ((40, 470), (1900, 560)),
        ((40, 685), (1900, 775)),
        ((40, 890), (1660, 980))
    ]
    for left_upper, right_lower in rectangles:
        cropped_img = img.crop((*left_upper, *right_lower))
        data = pytesseract.image_to_data(cropped_img, lang='ita', output_type=pytesseract.Output.DICT, config='--psm 4')
        for i in range(len(data['text'])):
            if data['text'][i].lower() == text_to_find.lower():
                x = data['left'][i] + left_upper[0]
                y = data['top'][i] + left_upper[1]
                position = (x + x_offset, y - y_offset)
                return position
    return None

def get_tile_content(coordinates, x_offset, y_offset):
    bottom_left = (coordinates[0] - x_offset, coordinates[1] + y_offset)    # tutaj przesunięcie w dół i w lewo relatywnie do środka kafelka
    top_right = (coordinates[0] + x_offset, coordinates[1] - y_offset)      # tutaj przesunięcie w górę i w prawo relatywnie do środka kafelka
    width = top_right[0] - bottom_left[0]
    height = bottom_left[1] - top_right[1]
    screenshot = pyautogui.screenshot(region=(bottom_left[0], top_right[1], width, height))
    file_count = len(os.listdir("tiles"))
    new_filename = f"tile_{file_count}.png"
    screenshot.save(os.path.join("tiles", new_filename))       # zapisanie kafelka do sprawdzenia czy dobrze tekst jest widoczny             
    text = pytesseract.image_to_string(screenshot)
    text = text.strip()
    text = text.replace('\n', ' ')
    text = text.split(' ')
    return text

def find_key(input):
    for key, value in anwsers.items():
        for word in input:
            if word.lower() in key.lower() and value[1]:
                return key

def move_tile(tile_coordinates, x_offset, y_offset):
    key = None
    country = get_tile_content(tile_coordinates, x_offset, y_offset)
    print(f"Przeczytano: {country}")
    pyautogui.moveTo(tile_coordinates)
    curr_x, curr_y = pyautogui.position()
    mouse = Controller()                                                                  # przesunięcie kursora na środek kafelka który biorę                 
    if country and len(country) == 1 and country[0] in anwsers.keys() and anwsers[country[0]][1]:       # jeśli kraj jest w słowniku i ma przypisaną pozycję
        key = country[0]
    elif country and len(country) > 1:
        key = find_key(country)
    if key:
        target_x, target_y = anwsers[key][1]
        mouse.press(Button.left)
        time.sleep(0.05)
        mouse.move(target_x - curr_x, target_y - curr_y)  
        time.sleep(0.05)
        mouse.release(Button.left)  
        time.sleep(0.2)
        return True
    return False

def main():
    url = 'https://wordwall.net/it/resource/34415259/a1/paesi-e-nazionalit%C3%A0'
    start_image = 'start.png'
    full_screen_image = 'full_screen.png'
    full_screen_mode = True

    if full_screen_mode:
        first_tile = (144, 128)
        next_tile = 230
        x_tile_offset = 100
        y_tile_offset = 30
        x_frame_offset = 60
        y_frame_offset = 70
        pause = 'big_pause.png'
    else:
        first_tile = (325, 270)
        next_tile = 150
        x_tile_offset = 55
        y_tile_offset = 15
        x_frame_offset = 50
        y_frame_offset = 60
        pause = 'small_pause.png'

    for file in os.listdir("tiles"):
        os.remove(os.path.join("tiles", file))

    pyautogui.FAILSAFE = False
    webbrowser.open(url)

    start_game(start_image)

    if full_screen_mode:
        make_fullscreen(full_screen_image)

    time.sleep(2)
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    
    pause_game(pause)

    for key, value in anwsers.items():
        anwsers[key] = (value[0], find_text_position(screenshot, value[0], x_frame_offset, y_frame_offset))
        pyautogui.moveTo(anwsers[key][1])

    for key, value in anwsers.items():
        if value[1] is None:
            print(f"Nie udało się znaleźć: {key}")
    
    pyautogui.click()
    time.sleep(0.5)

    # tuaj ma znaczenie czas bo wtedy timer się zaczyna
    for _ in range(len(anwsers)):
        outcome = move_tile(first_tile, x_tile_offset, y_tile_offset)
        if not outcome:
            # skipujemy te których nie znamy lokaliacji albo się chujowo przeczytały
            first_tile = (first_tile[0] + next_tile, first_tile[1])

    pyautogui.FAILSAFE = True


if __name__ == '__main__':
    main()
