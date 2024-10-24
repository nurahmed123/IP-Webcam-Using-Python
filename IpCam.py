import cv2
from flask import Flask, Response

# Initialize Flask app
app = Flask(__name__)

# Initialize webcam (0 is usually the default webcam on Mac)
cap = cv2.VideoCapture(0)


def generate_frames():
    while True:
        # Capture frame-by-frame from the webcam
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format as multipart
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


# Route to serve the video stream
@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
