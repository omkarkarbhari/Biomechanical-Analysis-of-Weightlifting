from tkinter import messagebox
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
# initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

# def csvwrite(alldata):
#     with open('frangledata2.csv','a',newline='') as file:
#         csvwriter = csv.writer(file)
#         csvwriter.writerow(alldata)
#         file.close()
    


def analysis(paths):

    #folderpath=r'C:\Users\Rutik\Desktop\pro25\Badlift2'
    #files=os.listdir(folderpath)
    flag=False
    ls=[]
    cont=0
    #print(file)

    for file in paths:
        #print(file)
        
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            frame = cv2.imread(file)
            #detectPose(frame, pose, display=True)   
                # Recolor image to RGB
            #print(frame)
            #cv2.imshow('check',frame)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
                # Make detection
            results = pose.process(image)
            #print(pose.process(image))
            #print(results.pose_landmarks)
                # Recolor back to BGR
            try:
                landmarks = results.pose_landmarks.landmark
                if(len(paths)==3):
                    
                    
                    print(cont)
                    print("\nKNEE")
                    print('RIGHT',end=' ')    
                    rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    print(int(calculate_angle(rhip,rknee,rankle)))
                    ls.append(int(calculate_angle(rhip,rknee,rankle)))


                    print('LEFT',end=' ')
                    lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    print(int(calculate_angle(lhip,lknee,lankle)))
                    ls.append(int(calculate_angle(lhip,lknee,lankle)))
                    print("\nANKLE")
                    print('RIGHT',end=' ')
                    rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    rfoot = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]


                    print(int(calculate_angle(rknee,rankle,rfoot)))
                    ls.append(int(calculate_angle(rknee,rankle,rfoot)))

                    print('LEFT',end=' ')
                    lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    lfoot = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

                    print(int(calculate_angle(lknee,lankle,lfoot)))
                    ls.append(int(calculate_angle(lknee,lankle,lfoot)))
                    print("\nHIP")
                    print('RIGHT',end=' ')
                    rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                    print(int(calculate_angle(rshoulder,rhip,rknee)))
                    ls.append(int(calculate_angle(rshoulder,rhip,rknee)))            



                    print('LEFT',end=' ')
                    lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    print(int(calculate_angle(lshoulder,lhip,lknee)))
                    ls.append(int(calculate_angle(lshoulder,lhip,lknee)))
                    print(ls)
                elif(len(paths)==1):

                    rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]




                    print(rhip,rshoulder,relbow)




                    ls.append(int(calculate_angle(rhip,rshoulder,relbow)))


                    print('LEFT SHOULDER')

                    # In[12]:



                    lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]


                    # In[6]:


                    print(lhip,lshoulder,lelbow)


                # In[7]:


                    ls.append(int(calculate_angle(lhip,lshoulder,lelbow)))

                    print('RIGHT ELBOW')

                    rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                    rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    

              

                    #print(rwrist,rshoulder,relbow)


         


                    ls.append(int(calculate_angle(rwrist,relbow,rshoulder)))


                    print('LEFT ELBOW')

                    lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    


                


                    

            


                    ls.append(int(calculate_angle(lwrist,lelbow,lshoulder)))

                    rindex = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
                    lindex = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]

        
                    temp=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
                    ls.append(int(calculate_angle(temp,lindex,rindex)))
                else:
                    print("Number of Paths Specified are not sufficient")
                
                

                
                #csvwrite(ls)
                print("\n\n")

                flag=False
            except:
                print("failed")
                flag=True
    return ls

def ReportGen(paths,anglis):
    if len(anglis)==23:
        from fpdf import FPDF
        #rk lk ra la rh lh rs ls re le d
        side0=paths[0]
        side1=paths[1]
        side2=paths[2]
        front=paths[3]
        barbell=paths[4]

        # save FPDF() class into a 
        # variable pdf
        pdf = FPDF()
        
        # Add a page
        pdf.add_page()
        
        # set style and size of font 
        # that you want in the pdf
        pdf.set_font("Arial", size = 15)
        
        # create a cell
        pdf.cell(200, 10, txt = "Biomechanical Analysis of Weightlifting", 
                ln = 1, align = 'C')
        
        # add another cell
        pdf.cell(200, 10, txt = "Side View Angles",
                ln = 2, align = 'C')


        sidedata0 = (
            (" ", "Left", "Right", "Difference"),
            ("Hip Angle", str(anglis[5]), str(anglis[4]), str(anglis[5]-anglis[4] if anglis[5]>anglis[4] else anglis[4]-anglis[5])),
            ("Knee Angle", str(anglis[1]), str(anglis[0]), str(anglis[1]-anglis[0] if anglis[1]>anglis[0] else anglis[0]-anglis[1])),
            ("Ankle Angle", str(anglis[3]), str(anglis[2]), str(anglis[3]-anglis[2] if anglis[3]>anglis[2] else anglis[2]-anglis[3])),
        )

        sidedata1 = (
            (" ", "Left", "Right", "Difference"),
            ("Hip Angle", str(anglis[11]), str(anglis[10]), str(anglis[11]-anglis[10] if anglis[11]>anglis[10] else anglis[10]-anglis[11])),
            ("Knee Angle", str(anglis[7]), str(anglis[6]), str(anglis[7]-anglis[6] if anglis[7]>anglis[6] else anglis[6]-anglis[7])),
            ("Ankle Angle", str(anglis[9]), str(anglis[8]), str(anglis[9]-anglis[8] if anglis[9]>anglis[8] else anglis[8]-anglis[9])),
    )
        sidedata2 = (
            (" ", "Left", "Right", "Difference"),
            ("Hip Angle", str(anglis[17]), str(anglis[16]), str(anglis[17]-anglis[16] if anglis[17]>anglis[16] else anglis[16]-anglis[17])),
            ("Knee Angle", str(anglis[13]), str(anglis[12]), str(anglis[13]-anglis[12] if anglis[13]>anglis[12] else anglis[12]-anglis[13])),
            ("Ankle Angle", str(anglis[15]), str(anglis[14]), str(anglis[15]-anglis[14] if anglis[15]>anglis[14] else anglis[14]-anglis[15])),
            )

        frontdata = (
            (" ", "Left", "Right", "Difference"),
            ("Shoulder Angle", str(anglis[19]), str(anglis[18]),str(anglis[19]-anglis[18] if anglis[19]>anglis[18] else anglis[18]-anglis[19])),
            ("Elbow Angle", str(anglis[21]), str(anglis[20]),str(anglis[21]-anglis[20] if anglis[21]>anglis[20] else anglis[20]-anglis[21])),
        )

        pdf.set_font("Arial",size=12)
        epw = pdf.w - 2*pdf.l_margin
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
        col_width = epw/4

        # pdf.set_font('Times','B',14.0) 
        # pdf.set_font('Times','',10.0) 
        pdf.ln(0.5)
        th = pdf.font_size
        # Here we add more padding by passing 2*th as height
        pdf.cell(200, 40, txt = " ",
                ln = 2, align = 'C')

        pdf.image(side0, x=20, y=40, w=50, h=50)
        pdf.image(side1, x=80, y=40, w=50, h=50)
        pdf.image(side2, x=140, y=40, w=50, h=50)
        pdf.cell(200, 10, txt = " ",
                ln = 2, align = 'C')
        pdf.cell(200, 10, txt = " ",
                ln = 2, align = 'C')
        pdf.cell(200, 10, txt = "Phase 1",
                ln = 2, align = 'C')

        for row in sidedata0:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        pdf.cell(200, 20, txt = " ",
                ln = 2, align = 'C')
        pdf.cell(200, 20, txt = "Phase 2",
                ln = 2, align = 'C')

        for row in sidedata1:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        pdf.cell(200, 20, txt = " ",
                ln = 2, align = 'C')
        pdf.cell(200, 20, txt = "Phase 3",
                ln = 2, align = 'C')

        for row in sidedata2:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 20, txt = "Front View Angles",
                ln = 1, align = 'C')
        pdf.set_font("Arial", size = 12)
        pdf.image(front, x=90, y=55, w=40, h=40)
        for row in frontdata:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 40, txt = "",
                ln = 1, align = 'C')
        pdf.cell(200, 30, txt = "Barbell Path",
                ln = 1, align = 'C')
        pdf.set_font("Arial", size = 12)
        pdf.image(barbell, x=50, y=155, w=120, h=100)
        data=[(" ","Deviation"),("Barbell Deviation",str(anglis[22]))]
        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1,align='C')
        
            pdf.ln(2*th)
        pdf.output('report.pdf','F')
        return 1
    else:
        root=tk.Tk()
        messagebox.showinfo('Error','Some error has occured')



def run(files):
    list1=files[1:]
    list2=files[0:1]
    ls1=analysis(list2)
    ls=analysis(list1)

    ls=list(map(int,ls))
    datain=ls+ls1
    res=list1+list2+['C:\\Users\\sohil\\Downloads\\version1\\barbell.jpg']
    print(datain)
    ReportGen(res,datain)
    return datain