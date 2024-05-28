from fer import Video
import cv2
from fer import FER
import matplotlib.pyplot as plt
import os
import sys
import streamlit as st
import tempfile
import pandas as pd

def getEmotions(video_file_buffer):
    # Face detection
    detector = FER(mtcnn=True)
    # Write the video file buffer to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tffile:
        tffile.write(video_file_buffer.read())
        # Video predictions
        video = Video(tffile.name)

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

def load_excel(file_path):
    xl = pd.ExcelFile(file_path)
    return xl.sheet_names

st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_bar_plot(df, sheet_name):
    selected_sheet = df[sheet_name]
    selected_sheet.set_index(selected_sheet.columns[0], inplace=True)
    selected_sheet.plot(kind='bar')
    plt.xlabel(selected_sheet.columns[0])
    plt.ylabel('Values')
    plt.title(f'Bar Plot for {sheet_name}')
    st.pyplot()

def main():
    st.set_page_config(layout="wide")

    st.title('Integrated Framework For Multimodal Student Monitoring And Psychometric Analysis')
    
    col1, col2 = st.columns(2)

    with col1:
        st.header("Emotion Analysis")
        st.write('This is an app to return emotions of video')
        video_file_buffer = st.file_uploader("Upload a video", type=["mp4", "mov",'avi','asf', 'm4v' ])
        if video_file_buffer is not None:
            getEmotions(video_file_buffer)
        st.video(video_file_buffer)

    with col2:
        st.header("Psychometric test results")
        st.write('This is an app to return the Psychometric test results of the student.')        
        uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file, sheet_name=None)
            sheet_names = load_excel(uploaded_file)
            selected_sheet = st.selectbox("Select Sheet", sheet_names)
            plot_bar_plot(df, selected_sheet)

if __name__ == "__main__":
    main()
