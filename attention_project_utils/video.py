import cv2


class Video:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.width, self.height = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(self.width, self.height)
        self.frames = Video.load_frames(self, video_path)
        self.frame_count = len(self.frames)

    def frame(self, frame_number):
        if frame_number < 0:
            return self.frames[0]
        if frame_number >= self.frame_count:
            return self.frames[self.frame_count - 1]
        return self.frames[frame_number]

    def load_frames(self, video_path):
        frames = []
        while self.cap.isOpened():
            grabbed, frame = self.cap.read()
            if not grabbed:
                return frames
            frames.append(frame)
        return frames
