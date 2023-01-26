import numpy as np
import cv2
import pytesseract
from gtts import gTTS
import os
from centroide_sort import centroid_sort
from difflib import SequenceMatcher
from compare_string import compare_str


# this function returns the location of the name to ring on the doorbell
def analyse_doorbell(string_to_find, image, X_CENTROIDS, Y_CENTROIDS, H, W):

    # sort the centroids from top left to down right
    X_CENTROIDS_SORTED, Y_CENTROIDS_SORTED, W_SORTED, H_SORTED = centroid_sort(
        X_CENTROIDS, Y_CENTROIDS, H, W)
    print(len(X_CENTROIDS_SORTED))

    STRINGS = []

    # all the names inside the rectangles are found and saved
    for i in range(len(X_CENTROIDS_SORTED)):
        cropped_img = image
        cropped_img = cropped_img[int((Y_CENTROIDS_SORTED[i]-H_SORTED[i]/2)):int((Y_CENTROIDS_SORTED[i]+H_SORTED[i]/2)),
                                  int(X_CENTROIDS_SORTED[i]-W_SORTED[i]/2):int(X_CENTROIDS_SORTED[i]+W_SORTED[i]/2)]
        cropped_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        img2char_gray = pytesseract.image_to_string(cropped_gray)
        print(img2char_gray.strip())
        STRINGS = np.append(STRINGS, img2char_gray)

    # correction of the names read
    STRINGS = [string.replace("!", "I") for string in STRINGS]
    for string in STRINGS:
        for j in string:
            if j.isalpha() == False and j != ' ':
                string.replace(j, '')
    if len(set(STRINGS)) != len(STRINGS):
        return 50
    for string in STRINGS:
        print(string)
        flag = False
        for j in string:
            if j.isalpha():
                flag = True
        if flag == False:
            return 51
    if len(STRINGS) == 0:
        return 50

    # compares the strings and finds the most similar one
    pos_max_ratio = compare_str(
        X_CENTROIDS_SORTED, Y_CENTROIDS_SORTED, H_SORTED, W_SORTED, STRINGS, string_to_find)

    if pos_max_ratio == 50:
        return 52
    else:
        print(pos_max_ratio)
        print(STRINGS[pos_max_ratio])

    # dictionary of the cells and instructions
        cell_descriptions = {
            0: 'First cell from the top left',
            2: 'Second cell from the top left',
            4: 'Third cell from the top left',
            6: 'Fourth cell from the top left',
            1: 'First cell from the top right',
            3: 'Second cell from the top right',
            5: 'Third cell from the top right',
            7: 'Fourth cell from the top right'
        }

        # if the string to find is the one recognized, a message of instruction is provided
        if SequenceMatcher(a=string_to_find, b=STRINGS[pos_max_ratio]).ratio() > 0.7:
            instruction = string_to_find + cell_descriptions[pos_max_ratio]
            print(instruction)

            audio = gTTS(instruction, lang="en", slow=False)
            if os.path.exists("example.mp3"):
                os.remove("example.mp3")
            audio.save("example.mp3")
            os.system("afplay example.mp3")

        else:
            return 52

        return instruction, pos_max_ratio, STRINGS[pos_max_ratio]
