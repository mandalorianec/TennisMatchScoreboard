from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestDTO:
    method: str
    query_params: dict[str, list[str]]
    body_params: Optional[dict] = None

