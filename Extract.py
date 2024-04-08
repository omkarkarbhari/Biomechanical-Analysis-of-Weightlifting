
import mediapipe as mp
import cv2
import numpy as np
import testing
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()


def run1(filename):
  vidcap = cv2.VideoCapture(str(filename))#files+'\\'+file)
  success,image = vidcap.read()
  print(success)
  count = 1
    # any button for next frame and to extract frame press q
    # change file path accordingly

  while success:      
    try:
      temp=None
      success,image = vidcap.read()
      temp=image
      if success==False: raise 'end'
      image=cv2.resize(image,(800,800))
      cv2.imshow('test',image)
      key=cv2.waitKey(0)
      if key==ord('q'):
        image=cv2.resize(image,(800,800))
        #pimage=wireframe(image)
        cv2.imwrite('.\\frames'+"\\SVfirst%d.png" % count, image)
        # count+=1
        for i in range(3):
          success,temp=vidcap.read()
          temp=cv2.resize(temp,(800,800))
          #temp=wireframe(temp)
          cv2.imwrite('.\\frames'+"\\SVfirst%d.png" % count, temp)
          count+=1
      if key==ord('w'):
        #pimage=wireframe(image)
        image=cv2.resize(image,(800,800))
        cv2.imwrite('.\\frames'+"\\SVsecond%d.png" % count, pimage)
        count+=1
        for i in range(3):
          success,temp=vidcap.read()
          #temp=wireframe(temp)
          temp=cv2.resize(temp,(800,800))
          cv2.imwrite('.\\frames'+"\\SVsecond%d.png" % count, temp)
          count+=1
      if key==ord('e'):
        #pimage=wireframe(image)
        image=cv2.resize(image,(800,800))
        cv2.imwrite('.\\frames'+"\\SVthird%d.png" % count, pimage)
        count+=1
        for i in range(3):
          success,temp=vidcap.read()
          #temp=wireframe(temp)
          temp=cv2.resize(temp,(800,800))
          cv2.imwrite('.\\frames'+"\\SVthird%d.png" % count, temp)
          count+=1
      if key==27:
        cv2.destroyAllWindows
      '''else:
        count+=1'''
      pimage=image
    except Exception as e:
      pass

def run2(filename):
  vidcap = cv2.VideoCapture(str(filename))#files+'\\'+file)
  success,image = vidcap.read()
  print(success)
  count = 1
    # any button for next frame and to extract frame press q
    # change file path accordingly

  while success:      
    try:
      temp=None
      success,image = vidcap.read()
      temp=image
      if success==False: raise 'end'
      image=cv2.resize(image,(800,800))
      cv2.imshow('test',image)
      key=cv2.waitKey(0)
      if key==ord('q'):
        image=cv2.resize(image,(800,800))
        cv2.imwrite('.\\frames'+"\\FVfirst%d.png" % count, pimage)
        count+=1
        for i in range(3):
          success,temp=vidcap.read()
          temp=cv2.resize(temp,(800,800))
          cv2.imwrite('.\\frames'+"\\FVfirst%d.png" % count, temp)
          count+=1
      
      if key==27:
        cv2.destroyAllWindows()
      '''else:
        count+=1'''
      pimage=image
    except Exception as e:
      pass

      #print('Read a new frame: ', success)
def run3():
  testing.run()



