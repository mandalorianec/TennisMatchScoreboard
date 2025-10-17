from dataclasses import dataclass


@dataclass
class ResponseDto:
    status: str
    headers: list[(str, str)]
    body: str
