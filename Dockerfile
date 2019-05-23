FROM levan92/openpose_base
USER root
RUN apt update
RUN apt -y install sudo apt-transport-https 
RUN apt -y install libcanberra-gtk-module libcanberra-gtk3-module dbus-x11

# SUBLIME TEXT
RUN wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add - &&\
    echo "deb https://download.sublimetext.com/ apt/stable/" | tee /etc/apt/sources.list.d/sublime-text.list &&\
    apt update &&\
    apt -y install sublime-text

RUN apt -y autoremove

RUN useradd -m user && echo "user:pwd" | chpasswd && adduser user sudo
USER user



WORKDIR /home