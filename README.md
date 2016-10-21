# FaceLook
A robot that could track people' face and follow.

#### ENGR 2210 Principles of Engineering 							Fall 2016


## Final Project Preproposal

Team name: Js
Section: Earlier section (0900-1040)
#### Members: Zhecan Wang, Jee Hyun Kim, Jong Woo Nam, Joseph Lee, Soohwan Chae

Project Title: Facelook 

### Basic concept and functionality
Facelook is a robot that can detect a human face and follow the detected face with its eye, a camera mounted on a pan/tilt mechanism. It can also move in all directions and follow the face owner to always keep a specified distance from the owner, by detecting the changing face size of the owner.

### Minimal Viable Product 
Our MVP is a robot that can detect and follow people’s face (not specific) from a camera/ Android phone mounted on a pan/ tilt mechanism. A good reference could be found here (https://www.youtube.com/watch?v=70lT8aNARNU)

### Stretch Goal (Tentative)
Our stretch goal is to mount the pan and tilt mechanism to a robot, whether it be a 4 wheeled vehicle(https://www.youtube.com/watch?v=vwZULUiJTqA) or a BB-8 robot (https://www.youtube.com/watch?v=Yq8_cvpOnSA). We would also like to implement something like face to voice matching, so that it would chase the person calling out its name, acting like a pet eventually. 

Anticipated biggest challenges to project implementation
The biggest challenge is to allow the system to detect a specific person’s face. This involves a button to trigger the camera to take multiple photos of the specific person’s face. Then the model may have to preprocess the data and then use machine learning algorithm to train on it. We are not sure the minimum live data size in order to let the machine to be able to detect the person’s face and the computation efficiency of the model training could be expensive.

