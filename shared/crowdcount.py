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
parser.add_argument("--img_path", default="../../../examples/media/COCO_val2014_000000000241.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
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
imageToProcess = cv2.imread(args[0].img_path)
ratio = imageToProcess.shape[1] / float(imageToProcess.shape[0])
# net_height_mult = 69 #set this
net_height_mult = 60 #set this
net_height = net_height_mult * 16
net_width = net_height*ratio
net_width = int((net_width // 16 + 1) * 16)

params['net_resolution']='{:0}x{:0}'.format(net_width, net_height)
print("Net Resolution Set: ", params['net_resolution'])
# params['net_resolution']="-1x1072" # 16*51
params['scale_number'] = 1
params['scale_gap'] = 0.25
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

try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    # resize_factor = 1
    # imageToProcess = cv2.resize(imageToProcess,(int(imageToProcess.shape[1]/resize_factor), int(imageToProcess.shape[0]/resize_factor)))
    # print(imageToProcess.shape)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])

    # Display Image
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    print("Num of keypoints predicted: ", datum.poseKeypoints.shape)
    # print("Face keypoints: \n" + str(datum.faceKeypoints))
    # print(datum.faceKeypoints.shape)
    # print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    # print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

    frame_show = deepcopy(imageToProcess)

    draw_keypoints(frame_show, datum.poseKeypoints)

    cv2.namedWindow('Openpose',cv2.WINDOW_NORMAL)
    # cv2.imshow("Openpose", datum.cvOutputData)
    cv2.imshow('Openpose', frame_show)



    cv2.waitKey(0)
except Exception as e:
    print(e)
    sys.exit(-1)
