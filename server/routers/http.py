import cv2
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


def generate_frames():
    video = cv2.VideoCapture("/home/akashsonowal/video-streaming-platform/data/5220298-hd_1920_1080_25fps.mp4")
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )  # in multipart format
    video.release()


@router.get("/http")
def video():
    return StreamingResponse(
        generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )