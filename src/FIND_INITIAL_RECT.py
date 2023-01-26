import cv2
import pytesseract
from gtts import gTTS
import os


# this function, given the image, finds the rectangle with a certain area and proportion between w and h and returns the string written inside
def find_init_rect(image):

    # color to gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # adaptive threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    nb_rect = 0
    # Find rectangular contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            if cv2.contourArea(cnt) > 50000 and w/h > 1 and w/h < 2:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                nb_rect += 1
                X, Y, W, H = cv2.boundingRect(cnt)

    # only if it finds the correct rectangle:
    if nb_rect == 1:

        # the image is cropped around it
        print(nb_rect)
        cropped = gray
        cropped = cropped[Y:Y+H, X:X+W]

        # the name inside is read
        imgchar = pytesseract.image_to_string(cropped)
        print(imgchar)

        # correction of mistakes
        imgchar.replace('!', 'I')
        imgchar.replace('|', 'I')
        imgchar.replace("\\", 'I')
        imgchar.replace(" ", "")

        # if the name read is uppercase, it means it could be the correct one, so the person should keep in position
        if imgchar.isupper():
            audio = gTTS('Stay still', lang="en", slow=False)
            if os.path.exists("example1.mp3"):
                os.remove("example1.mp3")
            audio.save("example1.mp3")
            os.system("afplay example1.mp3")
        else:
            return 50
    else:
        return 50

    return imgchar
