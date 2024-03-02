import cv2
import argparse
from utils import *
import mediapipe as mp
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise
import time

class ExerciseTracker:
    

    def __init__(self, args):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.exercise_types = ['pull-up', 'sit-up', 'push-up', 'squat', 'walk', 'jumping-jacks', 'lunges', 'leg-raises', 'burpees']
        self.current_index = self.exercise_types.index(args["exercise_type"])
        self.args = args

    def move_to_next_exercise(self):
        self.current_index = (self.current_index + 1) % len(self.exercise_types)
        return self.exercise_types[self.current_index]

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 480)

        with self.mp_pose.Pose(min_detection_confidence=0.5,
                            min_tracking_confidence=0.5) as pose:

            counter = 0
            status = True
            start_time = time.time()
            while cap.isOpened():
                ret, frame = cap.read()
                frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame.flags.writeable = False
                results = pose.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    counter, status = TypeOfExercise(landmarks).calculate_exercise(
                        self.args["exercise_type"], counter, status)
                except:
                    pass

                frame = score_table(self.args["exercise_type"], frame, counter, status)

                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                            thickness=2,
                                            circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(174, 139, 45),
                                            thickness=2,
                                            circle_radius=2),
                )

                cv2.imshow('Video', frame)
                if counter == 15:
                    cv2.destroyAllWindows()
                    time.sleep(15)
                    self.args["exercise_type"] = self.move_to_next_exercise()
                    cap = cv2.VideoCapture(0)
                    cap.set(3, 800)
                    cap.set(4, 480)
                    start_time = time.time()
                    counter = 0
                    status = True

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                if time.time() - start_time >= 120:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
    def run_in_background(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        return thread

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t",
                    "--exercise_type",
                    type=str,
                    help='Type of activity to do',
                    required=True)
    args = vars(ap.parse_args())

    tracker = ExerciseTracker(args)
    tracker.run()

'''import cv2
import mediapipe as mp
from flask import Flask, Response
import time
import argparse

app = Flask(__name__)

mp_pose = mp.solutions.pose

class ExerciseTracker:
    def __init__(self, exercise_type):
        self.exercise_type = exercise_type
        self.video_capture = None

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 480)

        with mp_pose.Pose(min_detection_confidence=0.5,
                          min_tracking_confidence=0.5) as pose:

            counter = 0
            status = True
            start_time = time.time()
            while cap.isOpened():
                ret, frame = cap.read()
                frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame.flags.writeable = False
                results = pose.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    counter, status = TypeOfExercise(landmarks).calculate_exercise(
                        self.args["exercise_type"], counter, status)
                except:
                    pass

                frame = score_table(self.args["exercise_type"], frame, counter, status)

                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                            thickness=2,
                                            circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(174, 139, 45),
                                            thickness=2,
                                            circle_radius=2),
                )

                cv2.imshow('Video', frame)
                if counter == 15:
                    cv2.destroyAllWindows()
                    time.sleep(15)
                    self.args["exercise_type"] = self.move_to_next_exercise()
                    cap = cv2.VideoCapture(0)
                    cap.set(3, 800)
                    cap.set(4, 480)
                    start_time = time.time()
                    counter = 0
                    status = True

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                if time.time() - start_time >= 120:
                    break
                cv2.putText(frame, f"Exercise: {self.exercise_type}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                if time.time() - start_time >= 120:
                    break

            cap.release()
            cv2.destroyAllWindows()

@app.route('/start-exercise/<exercise_type>')
def start_exercise(exercise_type):
    return Response(ExerciseTracker(exercise_type).run(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--exercise_type", type=str, help='Type of activity to do', required=True)
    args = parser.parse_args()

    app.run(host='localhost', port=5000, debug=True)
'''