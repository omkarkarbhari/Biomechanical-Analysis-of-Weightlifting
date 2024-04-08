from fpdf import FPDF
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox
import os
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    return round(angle, 2) 

def analysis(paths):
    angles = []
    # Assuming front and side images are in the correct order
    for i in range(0, len(paths), 2):
        front_file = paths[i]
        side_file = paths[i + 1]

        body_parts_angles = {}
        for file in [front_file, side_file]:
            if not os.path.exists(file):
                print(f"File not found: {file}")
                continue


            print(f"Processing image: {file}")
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                frame = cv2.imread(file)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = pose.process(image)
                if results.pose_landmarks:
                    print(f"Pose detected successfully in {file}")
                    landmarks = results.pose_landmarks.landmark
                    view_type = 'Front' if 'Front' in file else 'Side'
                    if view_type == 'Front':
                        body_parts_angles['Right Elbow'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                        )
                        body_parts_angles['Left Elbow'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                        )
                        body_parts_angles['Right Shoulder'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        )
                        body_parts_angles['Left Shoulder'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        )

                    if view_type ==  'Side':  # Side view
                        body_parts_angles['Right Hip'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        )
                        body_parts_angles['Left Hip'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        )
                        body_parts_angles['Right Knee'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        )
                        body_parts_angles['Left Knee'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        )
                        body_parts_angles['Right Ankle'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y],
                            [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                        )
                        body_parts_angles['Left Ankle'] = calculate_angle(
                            [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y],
                            [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                        )

        angles.append(body_parts_angles)

    return angles

def generate_report(angles, image_paths, lift_type, outcome, trajectory_images,std_dev):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", '',size=12)
    pdf.cell(200, 10, txt="Biomechanical Analysis of Weightlifting", ln=True, align='C')
    pdf.cell(200, 10, txt=f"{lift_type} - {outcome}", ln=True, align='C')

    optimal_angles_remarks = {
    "Clean and Jerk": {
        "Starting Position": {
            "Knee": {
                "range": (65, 130),
                "remark": "Increase hip and knee angles to avoid too deep a starting position, ensuring a powerful lift-off.",
                "recommendation": "Perform squat mobility exercises to increase flexibility and strength in the optimal knee angle range."
            }
        },
        "After First Pull": {
            "Hip": {
                "range": (75, 110),
                "remark": "Avoid dropping too low after the first pull; maintain a stronger position for efficient force transfer.",
                "recommendation": "Practice deadlifts and clean pulls to strengthen the posterior chain and improve hip drive."
            },
            "Knee": {
                "range": (110, 145),
                "remark": "Avoid dropping too low after the first pull; maintain a stronger position for efficient force transfer.",
                "recommendation": "Incorporate squats and lunges to improve leg strength and stability during the pull phase."
            }
        },
        "Second Pull": {
            "Knee": {
                "range": (150, 170),
                "remark": "Ensure full extension in the second pull to maximize power output.",
                "recommendation": "Perform snatch grip deadlifts to work on full hip and knee extension."
            },
            "Hip": {
                "range": (160, 180),
                "remark": "Ensure full extension in the second pull to maximize power output.",
                "recommendation": "Include hip thrusts and high pulls in your training to enhance hip extension power."
            }
        },
        "Rack Phase": {
            "Elbow": {
                "range": (20, 50),
                "remark": "Focus on achieving a stronger rack position with elbows higher to prepare for a successful jerk.",
                "recommendation": "Work on front rack mobility and strength exercises to improve elbow positioning."
            }
        },
        "Jerk Phase": {
            "Shoulder": {
                "range": (160, 180),
                "remark": "Drive the bar upwards with full arm extension for a solid lockout in the jerk.",
                "recommendation": "Practice overhead press and push press to enhance shoulder stability and strength."
            },
            "Elbow": {
                "range": (175, 180),
                "remark": "Drive the bar upwards with full arm extension for a solid lockout in the jerk.",
                "recommendation": "Strengthen triceps and improve lockout with exercises like skull crushers and tricep pushdowns."
            }
        },
        "Recovery/Final Position": {
            "Hip": {
                "range": (170, 180),
                "remark": "Improve control and stability in the recovery, ensuring upright posture and balanced foot positioning.",
                "recommendation": "Enhance core strength and balance with planks and single-leg exercises."
            },
            "Knee": {
                "range": (170, 180),
                "remark": "Improve control and stability in the recovery, ensuring upright posture and balanced foot positioning.",
                "recommendation": "Strengthen leg muscles and improve balance with exercises like Bulgarian split squats and stability ball squats."
            },
            "Ankle": {
                "range": (170, 180),
                "remark": "Improve control and stability in the recovery, ensuring upright posture and balanced foot positioning.",
                "recommendation": "Perform ankle mobility and stability exercises to improve foot positioning and balance."
            }
        }
    },
    "Snatch": {
        "Starting Position": {
            "Knee": {
                "range": (65, 110),
                "remark": "Adjust to a slightly more bent knee position for a stronger and more dynamic start.",
                "recommendation": "Work on knee strengthening drills to improve explosive power from the starting position."
            }
        },
        "After First Pull": {
            "Hip": {
                "range": (75, 110),
                "remark": "Aim for a higher hip position to maintain tension and facilitate a powerful second pull.",
                "recommendation": "Focus on hip mobility and posterior chain strengthening exercises like Romanian deadlifts."
            }
        },
        "Second Pull": {
            "Hip": {
                "range": (170, 180),
                "remark": "Emphasize full hip and knee extension to maximize force and elevation of the bar.",
                "recommendation": "Practice snatch deadlifts to enhance power development during the second pull."
            },
            "Knee": {
                "range": (150, 170),
                "remark": "Emphasize full hip and knee extension to maximize force and elevation of the bar.",
                "recommendation": "Incorporate plyometric exercises like box jumps to improve explosive leg power."
            }
        },
        "Catch Phase": {
            "Elbow": {
                "range": (170, 180),
                "remark": "Work on improving upper body strength and speed to achieve a solid lockout.",
                "recommendation": "Perform overhead stability exercises and snatch balances to improve lockout strength."
            }
        },
        "Recovery/Final Position": {
            "Hip": {
                "range": (170, 180),
                "remark": "Focus on developing strength and stability in the catch and recovery phases to maintain an upright position.",
                "recommendation": "Utilize core strengthening exercises and overhead squats to enhance stability during recovery."
            },
            "Knee": {
                "range": (170, 180),
                "remark": "Focus on developing strength and stability in the catch and recovery phases to maintain an upright position.",
                "recommendation": "Strengthen the quadriceps and hamstrings with leg press and hamstring curl exercises."
            },
            "Elbow": {
                "range": (170, 180),
                "remark": "Focus on developing strength and stability in the catch and recovery phases to maintain an upright position.",
                "recommendation": "Improve elbow stability with exercises like farmer's walks and wrist curls."
            }
        }
    }
}


    if lift_type == "Clean and Jerk":
        phase_names = ["Starting Position", "After First Pull", "Second Pull", "Rack Phase", "Jerk Phase", "Recovery/Final Position"]
    else:
        phase_names = ["Starting Position", "After First Pull", "Second Pull", "Catch Phase", "Recovery/Final Position"]

    # Image dimensions and positions
    image_width_half = (pdf.w - 20) / 2
    image_height = 70
    label_height = 5
    table_spacing = 10
    cell_height = 10
    table_column_width = 20

    for i, phase in enumerate(phase_names):
        pdf.set_font("Arial",'', size=10)
        pdf.cell(0, 10, txt=phase, ln=1, align='C')

        # Load images
        front_image = image_paths.get(f'Front_{i+1}.jpeg', '')
        side_image = image_paths.get(f'Side_{i+1}.jpeg', '')

        # Calculate positions
        x_front_image = 10
        x_side_image = x_front_image + image_width_half + 10
        y_image = pdf.get_y()

        # Insert images
        pdf.image(front_image, x=x_front_image, y=y_image, w=image_width_half, h=image_height)
        pdf.image(side_image, x=x_side_image, y=y_image, w=image_width_half, h=image_height)

        # Insert image labels
        pdf.set_y(y_image + image_height)
        pdf.set_x(x_front_image)
        pdf.cell(image_width_half, label_height, "Frontal View", border=1, ln=0, align='C')
        pdf.set_x(x_side_image)
        pdf.cell(image_width_half, label_height, "Side View", border=1, ln=1, align='C')

        y_table_start = pdf.get_y() + table_spacing

        if i < len(angles):
            phase_angles = angles[i]
            remarks = set()
            recommendations = set()
            

            # Prepare the table starting Y-coordinate after the image labels
            y_table_start = pdf.get_y() + label_height + 2  # Add a small margin

            # Upper Body Angles Table
            pdf.set_xy(x_front_image, y_table_start)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(table_column_width, cell_height, "Angle", border=1)
            pdf.cell(table_column_width, cell_height, "Left", border=1)
            pdf.cell(table_column_width, cell_height, "Right", border=1, ln=1)

            # Body part names and angles for Upper Body
            upper_body_parts = ["Shoulder", "Elbow"]
            for part in upper_body_parts:
                pdf.set_font("Arial",'', 12)
                pdf.set_x(x_front_image)
                pdf.cell(table_column_width, cell_height, part, border=1)
                pdf.cell(table_column_width, cell_height, f"{phase_angles.get(f'Left {part}', 'N/A')}" ,border=1)
                pdf.cell(table_column_width, cell_height, f"{phase_angles.get(f'Right {part}', 'N/A')}", border=1,ln=1)

            # Lower Body Angles Table
            pdf.set_xy(x_side_image, y_table_start)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(table_column_width, cell_height, "Angle", border=1)
            pdf.cell(table_column_width, cell_height, "Left", border=1)
            pdf.cell(table_column_width, cell_height, "Right", border=1, ln=1)

            # Body part names and angles for Lower Body
            lower_body_parts = ["Hip", "Knee", "Ankle"]
            for part in lower_body_parts:
                pdf.set_font("Arial",'', 12)
                pdf.set_x(x_side_image)
                pdf.cell(table_column_width, cell_height, part, border=1)
                pdf.cell(table_column_width, cell_height, f"{phase_angles.get(f'Left {part}', 'N/A')}",border=1)
                pdf.cell(table_column_width, cell_height, f"{phase_angles.get(f'Right {part}', 'N/A')}", border=1,ln=1)

            for part, values in optimal_angles_remarks[lift_type][phase].items():
                min_angle, max_angle = values["range"]
                measured_angle = float(phase_angles.get(f'Left {part}', 0))  # Ensure measured_angle is a float

                if measured_angle < min_angle or measured_angle > max_angle:
                    remarks.add(values["remark"])
                    recommendations.add(values["recommendation"])
                # Convert angles to float for comparison
                min_angle = float(min_angle)
                max_angle = float(max_angle)
                
                measured_angle = phase_angles.get(f'Left {part}', 0)  # Assuming left side measurement for simplicity
                measured_angle = float(measured_angle)  # Ensure measured_angle is a float
                

            # Add remarks to the PDF
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 10, txt="Remarks for this phase:", ln=1)
            pdf.set_font("Arial", '', 10)
            if remarks:
                for remark in remarks:
                    pdf.multi_cell(0, 10, txt=remark)
            else:
                pdf.multi_cell(0, 10, txt="No significant deviations from optimal angles detected.")

            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 10, txt="Recommendations:", ln=1)
            pdf.set_font("Arial", '', 10)
            if recommendations:
                for recommendation in recommendations:
                    pdf.multi_cell(0, 10, txt=recommendation)
            else:
                pdf.multi_cell(0, 10, txt="N/A")

            pdf.ln(5)

            # After both tables are drawn, update Y-coordinate to the end of the taller table
            end_y_upper = pdf.get_y()
            pdf.set_xy(x_side_image, y_table_start)
            pdf.ln(table_column_width * len(lower_body_parts) * cell_height)
            end_y_lower = pdf.get_y()

            # Use the taller of the two tables to set the starting Y-coordinate for the next image/table set
            pdf.set_y(max(end_y_upper, end_y_lower) + 2)  # Add a small margin

            

    # Barbell trajectory images
    pdf.set_font("Arial", "",size=10)
    pdf.add_page()
    pdf.cell(200, 10, txt="Barbell Trajectory", ln=1, align='C')

    # Assuming the images are not larger than half the page width minus a small margin
    image_width_half = (pdf.w - 20) / 2  # Calculate the width for half the page
    image_height = 70  # Adjust the height of your images accordingly
    label_height = 5  # Height for the labels

    # Define your barbell trajectory images
    your_trajectory_image = trajectory_images['your_trajectory']
    optimal_trajectory_image = trajectory_images['optimal_trajectory']

    # Calculate positions
    x_left_image = 10
    x_right_image = x_left_image + image_width_half + 10
    y_image = pdf.get_y()

    # Draw the images
    pdf.image(your_trajectory_image, x=x_left_image, y=y_image, w=image_width_half, h=image_height)
    pdf.image(optimal_trajectory_image, x=x_right_image, y=y_image, w=image_width_half, h=image_height)

    # Draw the labels below the images
    pdf.set_y(y_image + image_height)
    pdf.set_x(x_left_image)
    pdf.cell(image_width_half, label_height, "Your Trajectory", border=1, ln=0, align='C')
    pdf.set_x(x_right_image)
    pdf.cell(image_width_half, label_height, "Optimal Trajectory", border=1, ln=1, align='C')
    pdf.ln(10)

    # Standard deviation
    pdf.cell(200, 10, txt=f"Standard Deviation -- {std_dev}", ln=1, align='C')  # Last value as an example

    # pdf.ln(10)  # Add a line break for space before the line
    # pdf.cell(0, 0, '', 'T', 1)  # This will draw a line across the page
    # pdf.set_font("Arial", 'B', 12)  # Set font to bold for the "Remarks" title
    # pdf.cell(200, 10, txt="Remarks", ln=1, align='C')  # Add the "Remarks" title
    # pdf.set_font("Arial", '', 10)  # Set font back to normal for the content of the remarks
    # pdf.multi_cell(0, 10, txt=remarks)

    report_file = 'reportdupe.pdf'
    pdf.output(report_file)
    print(f"Report generated successfully and stored at: {os.path.abspath(report_file)}")

def run_analysis_and_report(lift_type,outcome, std_deviation):
    image_paths = {}
    num_phases = 5 if lift_type == "Snatch" else 6

    for i in range(num_phases):
        image_paths[f'Front_{i+1}.jpeg'] = f'frames/Front_{i+1}.jpeg'
        image_paths[f'Side_{i+1}.jpeg'] = f'frames/Side_{i+1}.jpeg'
    print("Starting analysis...")
    angles = analysis(list(image_paths.values()))

    trajectory_images = {
        'your_trajectory': 'barbellyour.jpeg',
        'optimal_trajectory': 'barbell1.jpg'
    }

    print("Generating report...")
    generate_report(angles, image_paths, lift_type, outcome, trajectory_images,std_deviation)

    print("Report generation completed.")

#run_analysis_and_report()