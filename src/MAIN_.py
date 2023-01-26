import cv2
from recognizing_rectangles import recogn_rect
import pytesseract
from gtts import gTTS
import os
from get_distance import get_min_dist
from difflib import SequenceMatcher
from ANALYSE_DOORBELL import analyse_doorbell
from FIND_INITIAL_RECT import find_init_rect


def main():

    # open the camera
    cap = cv2.VideoCapture(0)

    # variables to count or store features
    i = 0
    counter = 0
    flag = -1
    NOME = []
    z = 0
    r = 0
    fnf = 0

    # when the camera is open, an initial message is provided to the user
    initial_msg = "The program has started, I'm looking for the name to ring at"
    audio = gTTS(text=initial_msg, lang="en", slow=False)
    if os.path.exists("example0.mp3"):
        os.remove("example0.mp3")
    audio.save("example0.mp3")
    os.system("afplay example0.mp3")

    while (cap.isOpened()):
        ret, image = cap.read()
        i = i + 1
        if ((i % 5) == 0):
            counter = counter + 1

            # flag = -1: phase of recognition of the name on the paper
            if flag == -1:

                # the name in the rectangle is given. If it's not found, it returns 50
                ret = find_init_rect(image)
                if ret == 50:
                    continue
                else:
                    imgchar = ret

                # save names in a variable NOME
                NOME.append(imgchar)

                # checks whether the read name is the same for two consecutive times.
                if z >= 1:
                    if (NOME[z] == NOME[z - 1]) and len(imgchar) > 1:
                        print(imgchar)
                        string_to_find = imgchar
                        flag = 0
                        # the name is correct, a message is provided to the user
                        audio = gTTS(text='The name is' + imgchar +
                                     '. Now turn back and go to the door', lang="en", slow=False)
                        if os.path.exists("example2.mp3"):
                            os.remove("example2.mp3")
                        audio.save("example2.mp3")
                        os.system("afplay example2.mp3")
                z += 1

            # flag = 0: mapping of the doorbell
            if flag == 0:

                # rectangles in the image are recognized
                X_CENTROIDS, Y_CENTROIDS, H, W = recogn_rect(image)

                # if there are any repetitions, they are ignored
                if len(set(X_CENTROIDS)) != len(X_CENTROIDS) and len(set(Y_CENTROIDS)) != len(Y_CENTROIDS):
                    continue

                # if 8 rectangles are recognized, the doorbell is analysed
                if len(X_CENTROIDS) == 8:

                    # a message is provided when the doorbell is found for the first time
                    if r == 0:
                        doorbell_msg = "I've found the doorbell, remain in this position!"
                        audio = gTTS(text=doorbell_msg, lang="en", slow=False)
                        if os.path.exists("example1.mp3"):
                            os.remove("example1.mp3")
                        audio.save("example1.mp3")
                        os.system("afplay example1.mp3")
                        r += 1

                    # analysis of the doorbell: the position of the searched word is returned
                    db = analyse_doorbell(
                        string_to_find, image, X_CENTROIDS, Y_CENTROIDS, H, W)
                    if db == 50 or db == 51 or db == 52:
                        print(db)
                        continue
                    instruction, pos_max_ratio, stringa = db

                    print(string_to_find)
                    print(stringa)
                    print(pos_max_ratio)
                    print(X_CENTROIDS)
                    print(Y_CENTROIDS)

                    flag = 1

                else:
                    continue

            # flag = 1: the finger is detected and a message is provided when it is in the correct position
            if flag == 1:

                # the rectangles at the minimum distance from the finger is returned
                ret1 = get_min_dist(image)

                # after 5 times the finger isn't found, an advice is given to the user
                if ret1 == 50:
                    print('finger not found')
                    fnf += 1
                    if fnf == 5:
                        fnf_msg = "Finger not found, tilt your head down a little!"
                        audio = gTTS(text=fnf_msg, lang="en", slow=False)
                        if os.path.exists("example4.mp3"):
                            os.remove("example4.mp3")
                        audio.save("example4.mp3")
                        os.system("afplay example4.mp3")
                        fnf = 0
                    continue
                if ret1 == 51:
                    print('rectangle not found')
                    continue

                # given the rectangle, the image is cropped around it and the name inside is read
                x, y, h, w = ret1
                cropped_img = image
                cropped_img = cropped_img[int(
                    (y-h/2)):int((y+h/2)), int(x-w/2):int(x+w/2)]
                cropped_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                img2char_gray = pytesseract.image_to_string(cropped_gray)
                print(img2char_gray)

                # analysis of the similarity between the name read and the searched one
                rat = SequenceMatcher(
                    a=string_to_find, b=img2char_gray).ratio()
                if rat > 0.7:
                    # if the names are more or less the same, the user has arrived to the desired position
                    audio = gTTS(
                        text=string_to_find + '. Name found, now you can ring', lang="en", slow=False)
                    if os.path.exists("example2.mp3"):
                        os.remove("example2.mp3")
                    audio.save("example2.mp3")
                    os.system("afplay example2.mp3")
                    break


main()
