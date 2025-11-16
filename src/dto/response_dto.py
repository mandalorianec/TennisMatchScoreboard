from dataclasses import dataclass


@dataclass
class ResponseDto:
    status: str
    headers: list[tuple[str, str]]
    body: str
