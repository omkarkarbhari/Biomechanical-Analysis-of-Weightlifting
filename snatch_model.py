import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications import ResNet50

# Load the base ResNet50 model for feature extraction
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
base_model.trainable = False

FRAME_COUNT = 130
frame_size = (224, 224)

def load_trained_model(model_path):
    return load_model(model_path)

def extract_frames(video_path, target_frames=FRAME_COUNT, frame_size=frame_size):
    print(f"Extracting frames from video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < target_frames:
        print(f"Video {video_path} has only {total_frames} frames, which is less than the required {target_frames} frames.")
        cap.release()
        return None

    frames = []
    step = total_frames // target_frames

    for i in range(target_frames):
        frame_id = i * step
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        success, frame = cap.read()
        if not success:
            print(f"Failed to read frame {i} from {video_path}")
            break
        frame = cv2.resize(frame, frame_size)
        frames.append(frame)

    cap.release()
    return np.array(frames)

def preprocess_video(video_path):
    frames = extract_frames(video_path)
    if frames is None or len(frames) != FRAME_COUNT:
        print("Error: Video does not have the required number of frames.")
        return None
    return frames

def predict_outcome(model, video_frames):
    if video_frames is None:
        print("Error in video preprocessing.")
        return

    # Process frames through base_model to extract features
    features = base_model.predict(video_frames)
    features = np.expand_dims(features, axis=0)  # Add batch dimension
    features = pad_sequences(features, maxlen=FRAME_COUNT)
    prediction = model.predict(features)
    return np.mean(prediction)  # Get the average prediction if multiple frames

model_path = 'my_model0422(1).h5'
trained_model = load_trained_model(model_path)
def process_single_video_pair(model, frontal_video_path, horizontal_video_path):
    print(f"Processing {frontal_video_path} and {horizontal_video_path}")
    frontal_frames = preprocess_video(frontal_video_path)
    horizontal_frames = preprocess_video(horizontal_video_path)

    if frontal_frames is not None and horizontal_frames is not None:
        frontal_prediction = predict_outcome(model, frontal_frames)
        horizontal_prediction = predict_outcome(model, horizontal_frames)
        average_prediction = (frontal_prediction + horizontal_prediction) / 2
        outcome = 'Successful' if average_prediction >= 0.5 else 'Unsuccessful'
    else:
        outcome = 'Error in processing'

    print(f"{frontal_video_path} and {horizontal_video_path} are classified as {outcome}")
    return outcome

# frontal_video_path = 'C:/Users/Shubham/Desktop/Snatch/Frontal/Successful Lifts/S_FV_G_5.mp4'
# horizontal_video_path = 'C:/Users/Shubham/Desktop/Snatch/Horizontal/Successful Lifts/S_SV_G_5.mp4'

# process_single_video_pair(trained_model, frontal_video_path, horizontal_video_path)
