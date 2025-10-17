from dataclasses import dataclass


@dataclass
class OwnBaseException(Exception):
    error_message: str
    error_code: str

    def __str__(self):
        return f"{self.error_code} - {self.error_message}"
