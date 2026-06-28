from pathlib import Path
from models.document import Document


class TextLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> Document:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"{self.file_path} does not exist."
            )

        text = self.file_path.read_text(
            encoding="utf-8"
        )

        return Document(
            page_content=text,
            metadata={
                "source": self.file_path.name
            }
        )