"""External payloads (TypedDict) — not domain entities."""

from typing import NotRequired, TypedDict


class StudentPayload(TypedDict):
    """Shape of a student record coming from CSV / JSON."""

    student_id: int
    first_name: str
    last_name: str
    group: str
    average_grade: float
    email: NotRequired[str]