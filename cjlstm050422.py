import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt

FRAME_COUNT = 130
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
base_model.trainable = False
# Constants
  # Number of frames to extract from each video

def extract_frames(video_path, target_frames=FRAME_COUNT, frame_size=(224, 224)):
    print(f"Extracting frames from video: {video_path}")
    frames = []
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    skip_frames = max(1, total_frames // target_frames)
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to the specified size
        frame = cv2.resize(frame, frame_size)

        if frame_idx % skip_frames == 0:
            frames.append(frame)
            if len(frames) == target_frames:
                break

        frame_idx += 1

    cap.release()
    return frames

def preprocess_videos(folder_path_1, folder_path_2):
    videos = []
    labels = []  # 0 for failed, 1 for successful

    for folder_path in [folder_path_1, folder_path_2]:
        for label in ['Failed Lifts', 'Successful Lifts']:
            full_path = os.path.join(folder_path, label)
            print(f"Processing videos in {full_path}")

            video_files = os.listdir(full_path)
            video_files.sort()  # Sort the files to ensure matching across different views

            for video_file in video_files:
                if video_file.endswith(".mp4"):
                    video_path = os.path.join(full_path, video_file)
                    print(f"Processing file: {video_file}")
                    frames = extract_frames(video_path)
                    if len(frames) == FRAME_COUNT:  # Ensure each video has exactly FRAME_COUNT frames
                        videos.append(frames)
                        labels.append(1 if 'Successful' in label else 0)

    return np.array(videos), np.array(labels)



def create_model():
    # Load a pre-trained ResNet50 model for feature extraction
    base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    base_model.trainable = False

    model = Sequential([
        LSTM(256, input_shape=(FRAME_COUNT, base_model.output_shape[1])),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, videos, labels):
    # Feature extraction
    features = []
    for video in videos:
        video_features = base_model.predict(np.array(video))
        features.append(video_features)

    features = pad_sequences(features, maxlen=FRAME_COUNT)
    
    # Split the data into training and validation sets
    split_index = int(len(features) * 0.8)  # 80-20 split
    train_features, test_features = features[:split_index], features[split_index:]
    train_labels, test_labels = labels[:split_index], labels[split_index:]

    # Train the LSTM model
    history = model.fit(train_features, train_labels, validation_data=(test_features, test_labels), epochs=10, batch_size=8)
    model.save('cj_model0504(1).h5')
    return history

def plot_accuracy(history):
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(loc='upper left')
    plt.show()

# Load your dataset
folder_path_1 = "/Users/shruti/Downloads/Dataset Videos/Clean & Jerk/Frontal"
folder_path_2 = "/Users/shruti/Downloads/Dataset Videos/Clean & Jerk/Horizontal"
videos, labels = preprocess_videos(folder_path_1, folder_path_2)

model = create_model()
history = train_model(model, videos, labels)

# Plot the accuracy
plot_accuracy(history)

# For new video prediction, extract frames, predict with the base model, and then with the LSTM model
def predict_video(model, video_path):
    frames = extract_frames(video_path)
    features = base_model.predict(np.array(frames))
    features = pad_sequences([features], maxlen=FRAME_COUNT)
    prediction = model.predict(features)
    return 'Successful' if prediction >= 0.5 else 'Failed'
