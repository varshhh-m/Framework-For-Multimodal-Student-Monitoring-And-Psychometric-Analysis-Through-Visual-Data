from fer import Video
import cv2
from fer import FER
import matplotlib.pyplot as plt
import os
import sys
import streamlit as st
import tempfile

def getEmotions(vid ):
    # Face detection
    detector = FER(mtcnn=True)
    # Video predictions
    video = Video(vid)

    # Output list of dictionaries
    raw_data = video.analyze(detector, display=False)

    # Convert to pandas for analysis
    df = video.to_pandas(raw_data)
    df = video.get_first_face(df)
    df = video.get_emotions(df)

    # Plot emotions
    fig = df.plot(figsize=(20, 16), fontsize=26).get_figure()
    # Filename for plot
    fig.savefig('my_figure.png')

    most_common_emotion = df.sum().idxmax()
    print("Most common emotion in the video:", most_common_emotion)

    st.write("Emotion Distribution:")
    fig, ax = plt.subplots(figsize=(8, 8))
    emotion_counts = df.sum()
    total_frames = df.shape[0]
    emotion_percentages = (emotion_counts / total_frames) * 100
    ax.pie(emotion_percentages, labels=emotion_percentages.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Emotion Distribution in Video')
    ax.axis('equal')
    st.pyplot(fig)

    most_common_emotion = emotion_counts.idxmax()
    st.write("Most common emotion in the video:", most_common_emotion)
    
st.write('This is an app to return emotions of image')

video_file_buffer = st.sidebar.file_uploader("Upload a video", type=[ "mp4", "mov",'avi','asf', 'm4v' ])

#tffile = tempfile.NamedTemporaryFile(delete=False)

#tffile.write(video_file_buffer.read())
vid = cv2.VideoCapture(video_file_buffer.read())

    #values 
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(vid.get(cv2.CAP_PROP_FPS))
    #codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
codec = cv2.VideoWriter_fourcc('V','P','0','9')
out = cv2.VideoWriter('output1.webm', codec, fps, (width, height))


st.sidebar.text('Input Video')
#st.sidebar.video(tffile.name)


    
getEmotions(vid)


# Example usage:
# videofile = 'your_video_file.mp4'
# getEmotions(videofile)

    