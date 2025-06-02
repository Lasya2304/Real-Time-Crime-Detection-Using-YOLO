import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
import threading
import smtplib
import geocoder
from email.mime.text import MIMEText
from datetime import datetime
import os
import wave
import pyaudio
from moviepy.editor import VideoFileClip, AudioFileClip
import winsound
import time

# Load YOLO model
net = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
classes = ["Weapon"]
output_layer_names = net.getUnconnectedOutLayersNames()
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Global control variables
camera_on = False
video_writer = None
video_capture = None
stop_audio_event = None
audio_thread = None
video_filename = ""
audio_filename = ""
final_output = ""

# Audio recording function
def record_audio(audio_filename, stop_event):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk)

    frames = []

    while not stop_event.is_set():
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_buzzer(repeats=3, delay=0.5):
    for _ in range(repeats):
        winsound.Beep(1500, 700)
        time.sleep(delay)

# Weapon detection and recording
def detect_weapon():
    global camera_on, video_writer, video_capture, stop_audio_event, audio_thread
    global video_filename, audio_filename, final_output

    video_capture = cv2.VideoCapture(0)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    video_filename = f"weapon_detection_{timestamp}.mp4"
    audio_filename = f"audio_{timestamp}.wav"
    final_output = f"output_with_audio_{timestamp}.mp4"
    video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

    # Start audio recording
    stop_audio_event = threading.Event()
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, stop_audio_event))
    audio_thread.start()

    while camera_on:
        ret, img = video_capture.read()
        if not ret:
            break

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layer_names)

        class_ids, confidences, boxes = [], [], []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6:
                    center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                    w, h = int(detection[2] * width), int(detection[3] * height)
                    x, y = int(center_x - w / 2), int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indexes) > 0:
            play_buzzer()
            messagebox.showwarning("Alert", "Weapon Detected!")

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

        video_writer.write(img)
        cv2.imshow("Weapon Detection", img)

        if cv2.waitKey(1) == 27:  # ESC key
            break

    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()

    # Stop audio
    stop_audio_event.set()
    audio_thread.join()

    # Combine audio and video
    video_clip = VideoFileClip(video_filename)
    audio_clip = AudioFileClip(audio_filename)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_output, codec="libx264", audio_codec="aac")

# Start camera thread
def start_camera():
    global camera_on
    camera_on = True
    threading.Thread(target=detect_weapon).start()

# Stop camera
def stop_camera():
    global camera_on
    camera_on = False


import smtplib
from email.message import EmailMessage
import platform

# Use winsound for Windows, playsound or os for others
def beep_sound():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(1000, 1000) # frequency, duration
    else:
        import os
        os.system('say "Beep Alert"') # Mac alternative

def send_email():
    g = geocoder.ip('me')
    location = g.latlng
    print("location==>",location)
    map_loc="https://www.bing.com/maps?mepi=127%7EDirections%7EUnknown%7EDirection_Button&ty=0&rtp=pos.17.43777847290039_78.71621704101562__ACE+Engineering+College__e_%7E&mode=d&v=2&sV=1&cp=17.43779%7E78.716231&lvl=14.5"
    print(map_loc)
    msg = EmailMessage()
    msg['Subject'] = 'Alert: I am in Danger'
    msg['From'] = 'dskreddy97@gmail.com'
    msg['To'] = 'plasya234@gmail.com','klaxmiprasanna1423@gmail.com' ## 2mails pettandi meevi
    msg.set_content(f" I am in Danger, Location: {location} {map_loc} ")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('dskreddy97@gmail.com', 'tsjh nxkc qckr gwes')
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
# Send email with location

import threading

def play_buzzer_5_sec():
    # Use threading so it doesn't freeze the GUI
    def buzzer():
        duration = 5000  # milliseconds (5 seconds)
        frequency = 1000  # Hz (adjust for different tones)
        winsound.Beep(frequency, duration)

    threading.Thread(target=buzzer).start()
# GUI Setup

# GUI Setup
root = tk.Tk()
root.title("AI Powered Women Safety System with Predictive Crime Alerting")
root.geometry("300x300")

tk.Button(root, text="Camera ON", command=start_camera, width=25, bg="green").pack(pady=10)
tk.Button(root, text="Camera OFF", command=stop_camera, width=25, bg="red").pack(pady=10)
tk.Button(root, text="Send Email", command=send_email, width=25, bg="blue").pack(pady=10)
tk.Button(root, text="Play Buzzer (5 sec)", command=play_buzzer_5_sec, width=25, bg="orange").pack(pady=10)
tk.Button(root, text="Exit", command=root.quit, width=25).pack(pady=10)

root.mainloop()
