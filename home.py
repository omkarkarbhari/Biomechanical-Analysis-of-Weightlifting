from tkinter import *
import os
from tkinter import filedialog,ttk
import tkinter as tk
from tkinter import messagebox
import track
import Analysis
from barbeltrajectory import calculate_standard_deviation
import cv2
import importlib.util
import sys
import webbrowser
import os

from tensorflow.keras.models import load_model
from snatch_model import process_single_video_pair
from cjlstmtrial050422 import process_single_video_pair
filename1=''
filename2=''
lifting_type = ''  
lift_value=''
global std_deviation
curr=os.getcwd()
from dupereportnew import run_analysis_and_report
def set_lift_type(lift_type):
    global lifting_type
    global lift_value
    lifting_type = lift_type
    if lifting_type=='Snatch':
        lift_value=1
    else:
        lift_value=0
    print("Lift Type selected:", lifting_type)
    print("Lift Value:", lift_value)

def show_pdf(pdf_path):
    full_path = os.path.abspath(pdf_path)
    webbrowser.open(f'file://{full_path}')

def lift_type_selection():
    global window
    lift_type_window = Toplevel(window)
    lift_type_window.title("Select Lift Type")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = 150
    window_height = 100
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    lift_type_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    lift_type_window.config(background="#28282F")


    btn_clean_and_jerk = Button(lift_type_window, text="Clean and Jerk", command=lambda: [set_lift_type("Clean and Jerk"), lift_type_window.destroy()])
    btn_clean_and_jerk.pack(fill=X, pady=10)

    btn_snatch = Button(lift_type_window, text="Snatch", command=lambda: [set_lift_type("Snatch"), lift_type_window.destroy()])
    btn_snatch.pack(fill=X, pady=10)

def browseFiles():
    global filename1, filename2
    if lifting_type == '':
        messagebox.showerror("Error", "Please select the type of lift first.")
        return

num_captures = 0
prompt_label = None
analysisop=list()
def setname(file1,file2):
    global filename1,filename2
    filename1=file1
    filename2=file2
    return filename1,filename2
def browseFiles():
    global filename1,filename2
    filename1 = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File for Side View",
                                        filetypes = (('video files ','.mp4'),
                                                    ("all files",
                                                        "*.*")
                                                        ))
    filename2 = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File Front View",
                                        filetypes = (('video files ','.mp4'),
                                                    ("all files",
                                                        "*.*")
                                                        ))
    print(filename1,filename2)
    filename1,filename2=setname(filename1,filename2)

def extract_and_display():
    global filename1, filename2, window, lift_value
    if filename1 == '' or filename2 == '':
        messagebox.showerror("Error", "Please select both video files first.")
        return

    cap1 = cv2.VideoCapture(filename1)
    cap2 = cv2.VideoCapture(filename2)

    frame_counter = 1
    capture_counter = 0

    prompts = {0: ["Initial", "Clean", "Recovery", "Jerk", "Recovery"], 1: ["Initial", "Snatch", "Recovery"]}
    current_prompts = prompts[lift_value]

    prompt_label = Label(window, text=current_prompts[0], font=("Helvetica", 16), bg="#28282F", fg="red")
    prompt_label.pack(side=TOP, fill=X)
    window.update()

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            prompt_label.destroy()
            break

        cv2.imshow("Side View", frame1)
        cv2.moveWindow("Side View", 10, 45)

        cv2.imshow("Front View", frame2)
        cv2.moveWindow("Front View", 800, 45)

        key = cv2.waitKey(0) & 0xFF  # Wait indefinitely for a key press

        if key == ord('c') and capture_counter < len(current_prompts):
            prompt_label.config(text=current_prompts[capture_counter])

            curr_dir = os.getcwd()
            frames_dir = os.path.join(curr_dir, 'frames')

            if not os.path.exists(frames_dir):
                os.makedirs(frames_dir)

            side_frame_path = os.path.join(frames_dir, f"Side_{frame_counter}.jpeg")
            front_frame_path = os.path.join(frames_dir, f"Front_{frame_counter}.jpeg")

            cv2.imwrite(side_frame_path, frame1)
            cv2.imwrite(front_frame_path, frame2)

            frame_counter += 1
            capture_counter += 1

        elif key == ord('n'):  # 'n' key to go to the next frame
            continue
        
        elif key == ord('q'):  # 'q' key to quit
            break

        window.update()

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


def analysis():
    global analysisop, filename1, filename2,outcome

    if lifting_type == 'Snatch':
        model_path = 'my_model0422(1).h5'
        trained_model = load_model(model_path)
        outcome = process_single_video_pair(trained_model, filename2, filename1)
        analysisop.append(outcome)  
        print(f"The lift is {outcome}.")
    else:
        model_path="cj_model0504(1).h5"
        trained_model=load_model(model_path)
        outcome = process_single_video_pair(trained_model,filename2,filename1)
        analysisop.append(outcome)
        print(f"The lift is {outcome}")

    print("Analysis Completed!")
    messagebox.showinfo('Analysis', f"Analysis Completed! The lift is {analysisop[-1]}.")
    
def barbell():
    global filename1,std_deviation
    actual_path = track.run(filename1)
    optimal_path = 'barbell1.jpeg'
    std_deviation = calculate_standard_deviation(actual_path, optimal_path)
    print(f'Standard Deviation: {std_deviation}')

    
def report():
    run_analysis_and_report(lifting_type,outcome, std_deviation)
    show_pdf('reportdupe.pdf')
    messagebox.showinfo("Report", "Report generated successfully!")

def play_video(video_path, window_position):
    cap = cv2.VideoCapture(video_path)
    cv2.namedWindow('User Manual', cv2.WINDOW_NORMAL)
    # Move the video window to the same position as the main window
    x, y = window_position
    cv2.moveWindow('Video', x, y)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    cap.release()
    cv2.destroyAllWindows()

def main_screen_setup():
    # Get the position of the main window
    geom = window.geometry()
    window_position = tuple(map(int, geom.split('+')[1:]))  # Extract x and y positions

    window.after(2000, lambda: play_video('usermanual.mp4', window_position))
    button_video = Button(buttons_frame, text="User Manual",
                          command=lambda: play_video('usermanual.mp4', window_position),
                          width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_video.pack(fill=X, pady=10)
if __name__ == '__main__':
    window = Tk()
    window.state('zoomed')
    window.title('Biomechanical Analysis of Weightlifting')
    window.geometry("780x600+350+50")
    window.config(background="#28282F")
    btn_color = '#28282F'
    btn_fg = 'black'

    buttons_frame = Frame(window, bg="#28282F", bd=0, relief=FLAT)
    buttons_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
   
    main_screen_setup()

    button_lift_type = Button(buttons_frame, text="Select Lift Type", command=lift_type_selection,
                              width=20, pady=10)
    button_lift_type.pack(fill=X, pady=10)

    button_explore = Button(buttons_frame, text="Browse Files", command=browseFiles,
                            width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_explore.pack(fill=X, pady=10)

    button_ex = Button(buttons_frame, text="Extract and Select Frames", command=extract_and_display,
                       width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_ex.pack(fill=X, pady=10)

    button_select = Button(buttons_frame, text="Barbell Trajection", command=barbell,
                           width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_select.pack(fill=X, pady=10)

    button_analysis = Button(buttons_frame, text="Analysis and Classification", command=analysis,
                             width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_analysis.pack(fill=X, pady=10)

    button_exit = Button(buttons_frame, text="Get Report", command=report,
                         width=20, bg=btn_color, fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_exit.pack(fill=X, pady=10)

    button_ex1 = Button(buttons_frame, text="Exit", command=window.quit,
                        width=20, bg='#d9534f', fg=btn_fg, pady=10, bd=4, relief=RAISED)
    button_ex1.pack(fill=X, pady=10)

    window.mainloop()
 
