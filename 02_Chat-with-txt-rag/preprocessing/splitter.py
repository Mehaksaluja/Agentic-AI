from config import Config

class TextSplitter:
    def __init__(
        self,
        chunk_size=Config.CHUNK_SIZE,
        overlap=Config.CHUNK_OVERLAP
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks