"""Domain entities: Student, Group, AcademicRecord."""

from dataclasses import dataclass, field

from student_registry.exceptions import ValidationError
from student_registry.payloads import StudentPayload
from student_registry.value_objects import Grade


@dataclass
class Group:
    """Academic group — aggregate of students."""

    name: str
    _student_ids: list[int] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("Group name cannot be empty")

    def __len__(self) -> int:
        return len(self._student_ids)

    def __contains__(self, student_id: int) -> bool:
        return student_id in self._student_ids

    def add_student(self, student_id: int) -> None:
        if student_id in self._student_ids:
            return
        self._student_ids.append(student_id)

    def remove_student(self, student_id: int) -> None:
        if student_id in self._student_ids:
            self._student_ids.remove(student_id)

    @property
    def student_ids(self) -> tuple[int, ...]:
        return tuple(self._student_ids)


@dataclass
class Student:
    """Domain entity representing a student."""

    student_id: int
    first_name: str
    last_name: str
    group: str
    _average_grade: Grade

    def __post_init__(self) -> None:
        if not self.first_name.strip() or not self.last_name.strip():
            raise ValidationError("First and last name must not be empty")
        if not self.group.strip():
            raise ValidationError("Group must not be empty")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def average_grade(self) -> Grade:
        return self._average_grade

    @average_grade.setter
    def average_grade(self, value: Grade) -> None:
        self._average_grade = value

    def __repr__(self) -> str:
        return (
            f"Student(id={self.student_id}, "
            f"name={self.full_name!r}, "
            f"group={self.group!r}, "
            f"grade={self._average_grade})"
        )

    def __str__(self) -> str:
        return (
            f"{self.student_id:>4}  "
            f"{self.full_name:<25}"
            f"{self.group:<8}"
            f"{self._average_grade:>7.2f}"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id

    def __hash__(self) -> int:
        return hash(self.student_id)

    @classmethod
    def from_payload(cls, payload: StudentPayload) -> "Student":
        return cls(
            student_id=payload["student_id"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            group=payload["group"],
            _average_grade=Grade(payload["average_grade"]),
        )


@dataclass
class AcademicRecord:
    """Associates a student with a discipline and a grade."""

    student_id: int
    discipline: str
    grade: Grade

    def __post_init__(self) -> None:
        if not self.discipline.strip():
            raise ValidationError("Discipline must not be empty")