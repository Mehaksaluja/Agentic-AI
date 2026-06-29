from langchain_core.output_parsers import (
    StrOutputParser
)

class OutputParserFactory:
    @staticmethod
    def create():
        return StrOutputParser()