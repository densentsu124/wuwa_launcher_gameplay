import cv2
import numpy as np
import mss
import mss.tools
import subprocess
import pygetwindow as gw
import time
import os
import threading
from elevate import elevate as elevated

class GameRunner:
# Ctrl+c to close, or close the windows
    
    def __init__(self):

        #Edit this for yourself
        self.game_folder = "C:/Games/Wuthering Waves"
        self.window_to_select = "Mozilla Firefox"
        self.resize = True

        # if you want to run wuwa on the launcher, make sure to run this script first before
        # opening the launcher after running the game.


        #Dont edit this.
        self.image_number = 0

    def get_window_bbox(self, window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            return {
                'left': window.left,
                'top': window.top,
                'width': window.width,
                'height': window.height
            }
        except IndexError:
            raise ValueError(f"Window with title '{window_title}' not found.")

    def get_input(self):
        while True:
            user_input = input("Enter command: ")
            self.image_number -= int(user_input)
            if self.image_number < 0:
                self.image_number = 0
            print(self.image_number)

    def delete_files_in_directory(self, directory_path):
        try:
            directory_path = directory_path.replace("/", "\\")
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                print(file_path)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files deleted successfully.")
        except OSError:
            print("Error occurred while deleting files.")

    def run(self):
        window_title = self.window_to_select
        bbox = self.get_window_bbox(window_title)
        self.game_folder = self.game_folder.replace("/", "\\")
        try:
            elevated()
            subprocess.check_call([f"{self.game_folder}/launcher.exe"])
            self.delete_files_in_directory(f"{self.game_folder}/kr_game_cache/animate_bg/9e62f695209fba078e3b01be9029ed74")

            with open("links.bat", "w") as links:
                for i in range(2, 451):
                    links.write(f'mklink "{self.game_folder}\kr_game_cache\\animate_bg\9e62f695209fba078e3b01be9029ed74\home_{i}.jpg" "{self.game_folder}\kr_game_cache\\animate_bg\9e62f695209fba078e3b01be9029ed74\home_1.jpg"\n')
            subprocess.run(["links.bat"], shell=True, check=True)
        except Exception:
            pass

        with mss.mss() as sct:
            monitor = {
                'left': bbox['left'],
                'top': bbox['top'],
                'width': bbox['width'],
                'height': bbox['height']
            }

            iterations_per_second = 21.216407
            interval = 1 / iterations_per_second  # Time per iteration in seconds
            while True:
                start_time = time.time()  # Record the start time of the iteration
                # Capture the screen area
                img = sct.grab(monitor)
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                if self.resize is True:
                    img = cv2.resize(img, (1280, 760))
                full_file = f"{self.game_folder}\kr_game_cache\\animate_bg\9e62f695209fba078e3b01be9029ed74\home_1.jpg"

                try:
                    print(full_file)
                    if os.path.isfile(full_file):
                        os.remove(full_file)
                    cv2.imwrite(full_file, img)
                except Exception:
                    pass
                # Break loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                self.image_number = self.image_number % 450
                self.image_number += 1
                end_time = time.time()
                elapsed_time = end_time - start_time

                sleep_time = max(0, interval - elapsed_time)
                time.sleep(sleep_time)

            # Release resources
            cv2.destroyAllWindows()

runner = GameRunner()
runner.run()