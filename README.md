Bicep Curl Counter
A Python application that uses MediaPipe and OpenCV to detect and count bicep curls from a video file in real-time. The system tracks human poses, calculates the elbow joint angle, counts repetitions, and displays the results on the video feed with a status box showing reps and arm stage (up/down). It also logs workout data to a file.
Features

Pose Detection: Identifies key landmarks (shoulder, elbow, wrist) using MediaPipe's Pose module.
Angle Calculation: Computes the elbow angle to detect curl phases (up: <30°, down: >160°).
Curl Counter: Tracks and counts bicep curls based on angle thresholds.
Visualization: Renders pose landmarks, joint angles, and a status box with rep count and stage.
Workout Logging: Saves curl timestamps to a workout_log.txt file.


Prerequisites

Python 3.7+
Libraries: mediapipe, opencv-python, numpy

Installation

Clone the repository:git clone https://github.com/raxor555/bicep-curl-counter.git
cd bicep-curl-counter


Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install mediapipe opencv-python numpy


Add a video file (e.g., workout.mp4) to the project directory.

Usage

Update the video_path variable in bicepcurl.py to point to your video file:video_path = "workout.mp4"


Run the script:python bicepcurl.py


The video feed will display with pose landmarks, elbow angle, rep count, and stage. Press q to exit.
Check workout_log.txt for a log of completed curls.

Project Structure
bicep-curl-counter/
│
├── bicepcurl.py  # Main script for curl counter
├── workout_log.txt              # Log file for workout data (auto-generated)
├── README.md                    # Project documentation
└── requirements.txt             # Dependency list

Requirements
mediapipe>=0.8.9
opencv-python>=4.5.5
numpy>=1.21.0

Future Improvements

Add support for tracking both left and right arms.
Implement form feedback (e.g., detect excessive shoulder movement).
Integrate with a GUI for configuration (e.g., select video file, adjust thresholds).
Support live webcam input alongside video files.
Export workout stats to a CSV or JSON file for analysis.

Contributing
Contributions are welcome! Please open an issue or submit a pull request with your ideas or improvements.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

MediaPipe for pose estimation.
OpenCV for video processing.


Created by [Rayyan]
