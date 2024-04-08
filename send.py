import cv2
import mediapipe as mp
import os
import numpy as np
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()
filename=r'/Users/shruti/Downloads/Dataset Videos/Clean & Jerk/Frontal/Successful Lifts/CJ_FV_G_3.mp4'
success=0
for i in os.listdir('/Users/shruti/Downloads/Dataset Videos/Clean & Jerk/Frontal/Successful Lifts/'):
    vidcap = cv2.VideoCapture(str(filename))#files+'\\'+file)
    success,image = vidcap.read()
    print(success)
    count = 1
    # any button for next frame and to extract frame press q
    # change file path accordingly

def wireframe(i):
  with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    frame = i#cv2.imread(i)
            
            # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
        
            # Make detection
    results = pose.process(image)
        
            # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark
        #print(landmarks)
    except:
        print('error in landmarks')
            
            
            # Render detections
    mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_draw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_draw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
  
    return image


while success:      
    try:
        temp=None
        success,image = vidcap.read()
        temp=image
        if success==False: raise 'end'
        image=wireframe(image)
        image=cv2.resize(image,(800,800))
        cv2.imshow('test',image)
        key=cv2.waitKey(2)
        if key==ord('q'):
            image=cv2.resize(image,(800,800))
        #pimage=wireframe(image)
            cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVfirst%d.png" % count, image)
        # count+=1
            for i in range(3):
                success,temp=vidcap.read()
                temp=cv2.resize(temp,(800,800))
                #temp=wireframe(temp)
                cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVfirst%d.png" % count, temp)
                count+=1
        if key==ord('w'):
        #pimage=wireframe(image)
            image=cv2.resize(image,(800,800))
            cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVsecond%d.png" % count, pimage)
            count+=1
            for i in range(3):
                success,temp=vidcap.read()
            #temp=wireframe(temp)
                temp=cv2.resize(temp,(800,800))
                cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVsecond%d.png" % count, temp)
                count+=1
        if key==ord('e'):
        #pimage=wireframe(image)
            image=cv2.resize(image,(800,800))
            cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVthird%d.png" % count, pimage)
            count+=1
            for i in range(3):
                success,temp=vidcap.read()
            #temp=wireframe(temp)
                temp=cv2.resize(temp,(800,800))
                cv2.imwrite('/Users/shruti/Downloads/version1/frames'+"/SVthird%d.png" % count, temp)
                count+=1
        if key==27:
            cv2.destroyAllWindows()
        '''else:
        count+=1'''
        pimage=image
    except Exception as e:
        pass
    