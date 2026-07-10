from dataclasses import dataclass

@dataclass
class Ok[T]:
    value: T

@dataclass
class Err:
    error: str

type Result[T] = Ok[T] | Err
