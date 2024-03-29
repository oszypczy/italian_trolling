# Funny Script

This Python script automates a game on the website 'https://wordwall.net/it/resource/34415259/a1/paesi-e-nazionalit%C3%A0'. It uses image recognition and text extraction from images to interact with the game.

## Dependencies

The script uses the following Python libraries:

- `pyautogui` for automating mouse and keyboard actions
- `webbrowser` for opening the game in a web browser
- `time` for adding delays
- `pytesseract` for extracting text from images
- `PIL` (Pillow) for image processing
- `os` for file operations
- `pynput` for controlling the mouse

Make sure to install these dependencies using pip:

```bash
pip install pyautogui webbrowser time pytesseract pillow os pynput
```

## How to Run
To run the script, simply execute the funny_script.py file:

```bash
python funny_script.py
```

## How It Works
The script first opens the game in a web browser and starts the game. It then takes a screenshot of the game and uses image recognition to locate the tiles in the game. It extracts the text from each tile using pytesseract, and then uses pyautogui to move the tiles to the correct positions based on the extracted text.
