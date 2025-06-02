# Real-Time-Crime-Detection-Using-YOLO
This project utilizes deep learning and real-time object detection with the YOLOv3 model to identify weapons (like knives) from live video feeds. The system aims to enhance personal safety by generating instant alerts, recording evidence, and allowing users to send emergency emails with their current location.

📌 Features
- 🎯 Real-time Weapon Detection using YOLOv3
- 🔍 Visual + Audio Evidence Collection for real-time events
- 🎥 Live Webcam Feed Processing via OpenCV
- 🔊 Instant Alert System with buzzer and message popups
- 📬 Manual Email Alert with approximate live location
- 🖥️ Desktop GUI built with Tkinter for easy control


🧰 Tech Stack
- Python 3
- YOLOv3 (Custom-trained)
- OpenCV
- Tkinter (GUI)
- pyaudio / SoundDevice
- moviepy 
- Geocoder (IP-based location)

🚀 How It Works
1. Start Camera: Webcam feed starts and scans each frame in real time.
2. YOLO Detection: YOLOv3 checks frames for weapons (e.g., knives).
3. Alert System: If a weapon is detected:
  - A buzzer sounds
  - A warning message pops up
  - Video and audio recording starts
4. Email Alert: User can send an emergency email containing location details.
5. Media Merge: After stopping, audio and video are merged and saved locally.

📁 Project Structure
├── main.py               # Main GUI application
├── main2.py              # Alternative version with updated recording logic
├── weapon.py             # Web interaction module (optional)
├── yolov3_training_2000.weights   # Trained weights
├── yolov3_testing.cfg    # YOLO configuration
├── outputs/              # Recorded media (video/audio)
├── README.md             # Project documentation

⚙️ Setup Instructions
- Install Dependencies
pip install opencv-python
pip install numpy
pip install sounddevice
pip install soundfile
pip install geocoder
pip install moviepy
pip install pyaudio

🧪 Demo
-📌 Activate the webcam → Detect a weapon → Alert triggers → Video & audio are recorded → Send location-based emergency email!

📚 Future Enhancements
- 🧠 Add automatic email alerts (no manual trigger)
- ☁️ Integrate cloud backup and real-time dashboard
- 🔁 Train for multiple crime categories (fights, fire, etc.)
- 🎯 Upgrade to YOLOv5/YOLOv8 for improved detection
- 📱 Port the application to mobile/edge devices

🌟 Acknowledgements
- YOLO Object Detection (Darknet)
- OpenCV & Tkinter Documentation
- Geocoder Python Library
- moviePy 

📧 Contact
Lasya Palarapu
🔗 Email: plasya234@gmail.com
🔗 LinkedIn: https://www.linkedin.com/in/lasya-palarapu-8442b525a
🔗 GitHub : https://github.com/Lasya2304/Real-Time-Crime-Detection-Using-YOLO
