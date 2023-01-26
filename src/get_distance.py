from index_xy import index_xy
from recognizing_rectangles import recogn_rect
import math

# this function finds the rectangle at a minumum distance from the index finger


def get_min_dist(image):

    # finds the coordinates of the finger
    ret1 = index_xy(image)
    if not ret1:
        return 50

    # print the 2D coordinates of the first finger
    x_fing, y_fing = ret1
    print(x_fing, y_fing)

    # finds the rectangles in the image
    ret2 = recogn_rect(image)
    X_CENTROIDS, Y_CENTROIDS, H, W = ret2

    if len(X_CENTROIDS) == 0:
        return 51

    print(X_CENTROIDS)
    print(Y_CENTROIDS)

    # computes all the distances
    DISTANCES = []
    for i in range(0, len(X_CENTROIDS)):
        d = math.sqrt((x_fing - X_CENTROIDS[i])
                      ** 2 + (y_fing - Y_CENTROIDS[i])**2)
        DISTANCES.append(d)

    # finds the position of the minimum distance
    posmin = DISTANCES.index(min(DISTANCES))
    x = X_CENTROIDS[posmin]
    y = Y_CENTROIDS[posmin]
    h = H[posmin]
    w = W[posmin]

    return x, y, h, w
