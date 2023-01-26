import cv2
import mediapipe as mp

# this function returns the x and y coordinates of the y finger in an image. For further info refer to: https://mediapipe.dev/


def index_xy(image):

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.8,  # sopra 0.8 non va
            min_tracking_confidence=0.8) as hands:

        image = cv2.flip(image, 1)

        # converts the image to RGB and returns landmarks e handedness
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        if not results.multi_hand_landmarks:
            return
        for hand_landmarks in results.multi_hand_landmarks:
            my_marker = []
            for indice in range(21):
                denorm_x = hand_landmarks.landmark[indice].x * image.shape[1]
                denorm_y = hand_landmarks.landmark[indice].y * image.shape[0]
                denorm_z = hand_landmarks.landmark[indice].z * image.shape[1]
                xyz_marker = [denorm_x, denorm_y, denorm_z]
                my_marker.append(xyz_marker)

        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        x = image_width - hand_landmarks.landmark[8].x*image.shape[1]
        y = image_height - hand_landmarks.landmark[8].y*image.shape[0]
        INDEX_MARKER = [x, y]

    # It returns h_im-y because imshow puts the origin at the top of the image for y
    return x, image_height-y
