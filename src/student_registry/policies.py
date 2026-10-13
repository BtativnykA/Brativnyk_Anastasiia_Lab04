"""Grade policies — ABC + concrete subclasses (inheritance)."""

from abc import ABC, abstractmethod

from student_registry.models import Student
from student_registry.value_objects import Grade


class GradePolicy(ABC):
    """Abstract policy that maps a raw grade to a rounded grade."""

    @abstractmethod
    def apply(self, grade: Grade) -> Grade: ...


class PassThroughPolicy(GradePolicy):
    """No modification."""

    def apply(self, grade: Grade) -> Grade:
        return grade


class RoundedPolicy(GradePolicy):
    """Round to the nearest integer (as float)."""

    def apply(self, grade: Grade) -> Grade:
        return Grade(round(grade.value))


class PassingPolicy(GradePolicy):
    """Fail anything below a minimum threshold."""

    def __init__(self, minimum: float = 60.0) -> None:
        if not 0.0 <= minimum <= 100.0:
            raise ValueError("Minimum must be in [0, 100]")
        self._minimum = minimum

    @property
    def minimum(self) -> float:
        return self._minimum

    def apply(self, grade: Grade) -> Grade:
        return grade if grade.value >= self._minimum else Grade(0.0)