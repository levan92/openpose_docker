import os 
import sys
import cv2
import argparse 

OPENPOSE_DIR = os.path.abspath("../openpose")
OPENPOSE_PYTHON_DIR = os.path.abspath("../openpose/build/python")
sys.path.append(OPENPOSE_PYTHON_DIR)  # To find local version of the library

from openpose import pyopenpose as op

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("video", help="Video to be processed.")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = os.path.join(OPENPOSE_DIR,"models")
# params["face"] = True
# params["hand"] = False
# params['camera_resolution']="752x440" # Frisbee
# params['camera_resolution']="2400x1200" # golf_crowd
params['model_pose'] = "BODY_25"
# params['model_pose'] = "COCO" #18 keypoints
# params['model_pose'] = "MPI" # 15 keypoints
# params['model_pose'] = "MPI_4_layers" # 15 keypoints, less accurate but faster
# params['net_resolution']="-1x368" # default, best balance, 16*23

assert(os.path.exists(args[0].video)),'Video Path given does not exist!'
cap = cv2.VideoCapture(args[0].video)
frame_w = cap.get(3)
frame_h = cap.get(4)
vid_fps = cap.get(5)

basename = os.path.basename(args[0].video).split('.')[0]

fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
out_vid = cv2.VideoWriter(basename+'_cc.avi',fourcc, vid_fps, (int(frame_w), int(frame_h)))


ratio = frame_w / float(frame_h)
# net_height_mult = 69 #set this
# net_height_mult = 60 #set this
net_height_mult = 45 #set this
# net_height_mult = 23 #set this
net_height = net_height_mult * 16
net_width = net_height*ratio
net_width = int((net_width // 16 + 1) * 16)

params['net_resolution']='{:0}x{:0}'.format(net_width, net_height)
print("Net Resolution Set: ", params['net_resolution'])
# params['net_resolution']="-1x1072" # 16*51
params['scale_number'] = 1
params['scale_gap'] = 0.25
params['render_threshold'] = 0.4
# params['maximize_positives'] = False
# params['maximize_positives'] = True

# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1])-1: next_item = args[1][i+1]
    else: next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-','')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-','')
        if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

from drawer import draw_keypoints
from copy import deepcopy
import time
try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    cv2.namedWindow('Openpose',cv2.WINDOW_NORMAL)
    tot_dur = 0
    tot_dur_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # resize_factor = 1
        # imageToProcess = cv2.resize(imageToProcess,(int(imageToProcess.shape[1]/resize_factor), int(imageToProcess.shape[0]/resize_factor)))
        # print(imageToProcess.shape)
        datum.cvInputData = frame

        tic = time.time()
        opWrapper.emplaceAndPop([datum])
        toc = time.time()
        tot_dur += toc - tic
        tot_dur_count += 1

        # Display Image
        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        print("Num of keypoints predicted: ", datum.poseKeypoints.shape)
        # print("Face keypoints: \n" + str(datum.faceKeypoints))
        # print(datum.faceKeypoints.shape)
        # print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        # print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
        # frame_show = deepcopy(frame)
        # draw_keypoints(frame_show, datum.poseKeypoints)
        # cv2.imshow('Openpose', frame_show)

        openpose_frameshow = datum.cvOutputData
        # print('op frameshow:',openpose_frameshow.shape)

        cv2.imshow("Openpose", openpose_frameshow)
        # cv2.imwrite(os.path.basename(args[0].img_path).split('.')[0]+"_crowdcount.png", frame_show)
        out_vid.write(openpose_frameshow)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    print('Inference avrg duration: {}'.format(tot_dur/tot_dur_count))

except Exception as e:
    print(e)
    sys.exit(-1)
