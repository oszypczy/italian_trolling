import pyautogui
import webbrowser
import time
import pytesseract
from PIL import ImageGrab
import math

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
    'America': ('americano/a', None),
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

v_max = 1000

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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
    # szukam póki nie znajdę (tutaj czas jeszcze nie ma znaczenia)
    while True:
        try:
            location = pyautogui.locateOnScreen(img, confidence=0.8)
            x, y = pyautogui.center(location)
            return x, y
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)


"""
Ogólnie tutaj czasem nie znajduje niektóych narodowości
I to jest dziwne bo to jest zwykle 1-3 rekordy ale co uruchomienie są różne
"""
def find_text_position(img, text_to_find):
    data = pytesseract.image_to_data(img, lang='ita+eng', output_type=pytesseract.Output.DICT, config='--psm 3')
    position = None
    for i in range(len(data['text'])):
        if data['text'][i].lower() == text_to_find.lower():
            x = data['left'][i]
            y = data['top'][i]
            position = (x + 50, y - 60)     # przesunięcie bo chodzi o lokację ramki wyżej
    return position

def get_tile_content(coordinates):
    bottom_left = (coordinates[0] - 90, coordinates[1] + 30)    # tutaj przesunięcie w dół i w lewo relatywnie do środka kafelka
    top_right = (coordinates[0] + 90, coordinates[1] - 30)      # tutaj przesunięcie w górę i w prawo relatywnie do środka kafelka
    width = top_right[0] - bottom_left[0]
    height = bottom_left[1] - top_right[1]
    screenshot = pyautogui.screenshot(region=(bottom_left[0], top_right[1], width, height))
    screenshot.save("tile.png")                                 # zapisanie kafelka do sprawdzenia czy dobrze tekst jest widoczny             
    text = pytesseract.image_to_string(screenshot)
    text = text.strip()
    return text

def move_tile(tile_coordinates):
    country = get_tile_content(tile_coordinates)
    pyautogui.moveTo(tile_coordinates)                                      # przesunięcie kursora na środek kafelka który biorę                 
    if country and country in anwsers.keys() and anwsers[country][1]:       # jeśli kraj jest w słowniku i ma przypisaną pozycję
        """
        Nie da się niestety dragować z zerowym czasem bo on wtedy puszcza wcześniej te kafelki
        Chyba że może innej biblioteki uzyć ale idk od czego to wsm zależy
        Jak się da za duży v_max to widac że on je upuszcza wcześniej :(
        """
        distance = calculate_distance(tile_coordinates, anwsers[country][1])
        mouse_duration = distance / v_max
        pyautogui.dragTo(anwsers[country][1], duration=mouse_duration)
        """
        Musi być tutaj sleep bo to GUI działa tak że jak trafisz to te kafelki się tak śmiesznie 
        gibają i nie można dobrze screena zrobić tego jednego kafelka kolejnego którego trzeba przeczytać co tam jest napisane
        """            
        time.sleep(0.4)
        return True
    return False

def main():
    url = 'https://wordwall.net/it/resource/34415259/a1/paesi-e-nazionalit%C3%A0'
    start_image = 'start.png'
    full_screen_image = 'full_screen.png'
    pause = 'pause.png'
    first_tile = (144, 126)

    pyautogui.FAILSAFE = False
    webbrowser.open(url)

    start_game(start_image)

    make_fullscreen(full_screen_image)

    time.sleep(1)
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")

    pause_game(pause)

    for key, value in anwsers.items():
        anwsers[key] = (value[0], find_text_position(screenshot, value[0]))

    for key, value in anwsers.items():
        print(f'{key}: {value}')
    
    pyautogui.click()

    # tuaj ma znaczenie czas bo wtedy timer się zaczyna
    for _ in range(len(anwsers)):
        outcome = move_tile(first_tile)
        if not outcome:
            first_tile = (first_tile[0] + 234, first_tile[1])
        

    pyautogui.FAILSAFE = True


if __name__ == '__main__':
    main()
