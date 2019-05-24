# Openpose on nvidia-docker

## Description
- Comes with 
    - CUDA 8.0
    - opencv 3.4.0 (python3)
    - caffe 1.0 (python3)
    - openpose (python3, latest version as of May 2019, with hand, body, face landmarks detection)
    - sublime text
    - packages needed to run with display
- Docker credentials: user:pwd

## Usage
Images available to pull:
- `sudo docker pull levan92/openpose_base:latest`
- `sudo docker pull levan92/openpose:init`

To build image from Dockerfile:

`sudo nvidia-docker build -t "levan92/openpose" .`

To run image with display:

`sudo nvidia-docker run -it --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" levan92/openpose`


## Additional info
cmake commands for openpose for future reference:
```
cmake -D PYTHON_EXECUTABLE=/usr/bin/python3 -D PYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.5m.so -D BUILD_PYTHON=ON -D Caffe_INCLUDE_DIRS="/opt/caffe/include;/opt/caffe/build/include/" -D Caffe_LIBS=/opt/caffe/build/lib/libcaffe.so -D BUILD_CAFFE=OFF ..
```
