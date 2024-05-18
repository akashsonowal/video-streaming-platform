import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws")
async def ws_video(websocket: WebSocket):
    await websocket.accept() #handshake
    video = cv2.VideoCapture("/home/akashsonowal/video-streaming-platform/data/5220298-hd_1920_1080_25fps.mp4")

    try:
        while True:
            success, frame = video.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                await websocket.send_bytes(frame_bytes)

    except WebSocketDisconnect as e:
        print(e)
    finally:
        video.release()
        await websocket.close()