import cv2
from random import randint 

color = (255,255,0)

font = cv2.FONT_HERSHEY_DUPLEX
fontScale = 5
fontColor = (255,255,0)
fontThickness = 5

def draw_keypoints(frame, people_kps, threshold=0.5):
    # print(frame.shape)
    # count = 0
    for kps in people_kps:
        ###
        # EUGENE ANG DID THIS
        # temp1 = randint(0,255)
        # temp2 = randint(0,255)
        # b_min = min(temp1, temp2)
        # b_max = max(temp1, temp2)
        # temp1 = randint(0,255)
        # temp2 = randint(0,255)
        # g_min = min(temp1, temp2)
        # g_max = max(temp1, temp2)
        # temp1 = randint(0,255)
        # temp2 = randint(0,255)
        # r_min = min(temp1, temp2)
        # r_max = max(temp1, temp2)
        # color = (randint(b_min,b_max), randint(g_min,g_max), randint(r_min,r_max))
        ###
        max_rgb = 200
        color = (randint(0,max_rgb), randint(0,max_rgb), randint(0,max_rgb))

        for kp in kps:
            x, y, prob = kp
            if prob < threshold:
                # print('continued')
                continue
            # count += 1
            # print(x,y)
            cv2.circle(frame, (x,y), 4, color, -1)

    # text_red = 'N P e s C u t d: {}'.format(len(people_kps))
    # text_white = ' D e p   o n e'
    text = 'NDPeeps Counted: {}'.format(len(people_kps))
    # text_red = ' '.join(text[::2])
    # print(text_red)
    # text_white = ' ' + ' '.join(text[1::2])
    # print(text_white)
    # cv2.putText(frame, text_red, (20,150), font, fontScale, (0,0,255), fontThickness)
    cv2.rectangle(frame, (20,25), (20+len(text)*92, 25+30*fontScale), (0,0,255), -1)
    cv2.putText(frame, text, (20,150), font, fontScale, (255,255,255), fontThickness)
    # cv2.putText(frame, text, (20,150), font, fontScale, fontColor, fontThickness)

