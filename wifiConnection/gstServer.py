import cv2
vc = cv2.VideoCapture()
# 192.168.34.162

vc.open("tcpclientsrc host=192.168.34.162 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false")
# vc.open("tcpclientsrc host=192.168.34.162 port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! appsink sync=false")
# vc.open("tcpclientsrc host=192.168.35.166 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false")
while True:
    try:
        a,b = vc.read()
        if a:
          cv2.imshow('0',b)
          junk = cv2.waitKey(10)
    except Exception as e:
        pass



# gst-launch-1.0 -v tcpclientsrc host=192.168.34.162 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false