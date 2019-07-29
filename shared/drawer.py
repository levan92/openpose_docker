import cv2

color = (255,255,0)


def draw_keypoints(frame, people_kps, threshold=0.5):
    # print(frame.shape)
    # count = 0
    for kps in people_kps:
        for kp in kps:
            x, y, prob = kp
            if prob < threshold:
                # print('continued')
                continue
            # count += 1
            # print(x,y)
            cv2.circle(frame, (x,y), 2, color, -1)
