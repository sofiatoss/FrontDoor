# this function sorts the rectangles of the doorbell
def centroid_sort(X_CENTROIDS, Y_CENTROIDS, H, W):

    X_SORTED = []
    Y_SORTED = []
    H_SORTED = []
    W_SORTED = []

    for i in range(4):

        # find the first value on the row
        sumcen = []
        for j in range(len(X_CENTROIDS)):
            sumcen.append(X_CENTROIDS[j]+Y_CENTROIDS[j])

        ind_uno = sumcen.index(min(sumcen))
        X_SORTED.append(X_CENTROIDS[ind_uno])
        Y_SORTED.append(Y_CENTROIDS[ind_uno])
        H_SORTED.append(H[ind_uno])
        W_SORTED.append(W[ind_uno])

        X_CENTROIDS.remove(X_CENTROIDS[ind_uno])
        Y_CENTROIDS.remove(Y_CENTROIDS[ind_uno])
        H.remove(H[ind_uno])
        W.remove(W[ind_uno])

        # find the second value on the row
        ind_sec = Y_CENTROIDS.index(min(Y_CENTROIDS))
        X_SORTED.append(X_CENTROIDS[ind_sec])
        Y_SORTED.append(Y_CENTROIDS[ind_sec])
        H_SORTED.append(H[ind_sec])
        W_SORTED.append(W[ind_sec])

        X_CENTROIDS.remove(X_CENTROIDS[ind_sec])
        Y_CENTROIDS.remove(Y_CENTROIDS[ind_sec])
        H.remove(H[ind_sec])
        W.remove(W[ind_sec])

    return X_SORTED, Y_SORTED, W_SORTED, H_SORTED
