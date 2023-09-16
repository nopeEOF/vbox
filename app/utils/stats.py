from dataclasses import dataclass


@dataclass
class UsersUsage:
    email: str
    upload: float
    download: float
