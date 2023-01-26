import numpy as np
from difflib import SequenceMatcher

# this function compares the strings of the cells with a given one and finds the position of the most similar one


def compare_str(X_CENTROIDS_SORTED, Y_CENTROIDS_SORTED, H_SORTED, W_SORTED, STRINGS, string_to_find):
    # contains the x,y,h,w of every obtained rectangle and the relative string in it (5th element)
    DICT = []

    for i in range(len(X_CENTROIDS_SORTED)):
        couple = []  # contains the rectangle and the relative string (name)
        couple = np.append(
            couple, [X_CENTROIDS_SORTED[i], Y_CENTROIDS_SORTED[i], H_SORTED[i], W_SORTED[i]])
        couple = np.append(couple, STRINGS[i])
        DICT.append(couple)

    ratios = []
    for i in range(len(DICT)):
        ratios.append(SequenceMatcher(a=string_to_find, b=DICT[i][4]).ratio())
        print(DICT[i][4] + " :   " + str(ratios[i]) + "\n")

    max_ratio = max(ratios)
    pos_max_ratio = ratios.index(max_ratio)
    return pos_max_ratio
