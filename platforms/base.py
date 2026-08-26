from abc import ABC, abstractmethod


class SocialMedia(ABC):
    def __init__(self, name: str, videoPath: str):
        super().__init__()
        self.name = name
        self.videoPath = videoPath

    @abstractmethod
    def post(message: str, videoPath: str) -> bool:
        ...