import cv2

# this function, given an image, returns the coordinates of each rectangle inside with a certain dimension


def recogn_rect(image):

    # find the dimension of the image
    h_im, w_im, _ = image.shape
    print('width: ', w_im)
    print('height:', h_im)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # adaptive threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    # find the contours inside the image
    cnts, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # minimum dimension of the rectangle to find
    area_treshold_MIN = 1000

    X_CENTROIDS = []
    Y_CENTROIDS = []
    H = []
    W = []

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
        if len(approx) == 4:
            if w/h > 2 and w/h < 3 and cv2.contourArea(c) > area_treshold_MIN:
                cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
                xpw = x + w
                yph = y + h

                # computation of centroid's coordinate
                X_CENTR = (x+xpw)/2
                Y_CENTR = (y+yph)/2
                X_CENTROIDS.append(X_CENTR)
                Y_CENTROIDS.append(Y_CENTR)
                H.append(h)
                W.append(w)

    return X_CENTROIDS, Y_CENTROIDS, H, W
