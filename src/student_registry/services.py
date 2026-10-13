"""Application services — orchestration layer."""

from collections.abc import Iterable

from student_registry.exceptions import NotFoundError, ValidationError
from student_registry.models import Group, Student
from student_registry.policies import GradePolicy
from student_registry.protocols import Exporter, Notifier
from student_registry.repositories import InMemoryRepository
from student_registry.value_objects import Grade


class StudentRegistryService:
    """Orchestrates use cases around students."""

    def __init__(
        self,
        repository: InMemoryRepository[Student],
        notifier: Notifier,
        exporter: Exporter,
        grade_policy: GradePolicy,
    ) -> None:
        # Dependency Injection через конструктор
        self._repo = repository
        self._notifier = notifier
        self._exporter = exporter
        self._policy = grade_policy

    # --- commands ---

    def register_student(self, student: Student) -> Student:
        adjusted = Student(
            student_id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            group=student.group,
            _average_grade=self._policy.apply(student.average_grade),
        )
        self._repo.add(adjusted)
        self._notifier.send(
            "registry@university",
            f"Registered: {adjusted.full_name}",
        )
        return adjusted

    def update_grade(self, student_id: int, new_grade: Grade) -> Student:
        student = self._repo.require(student_id)
        student.average_grade = self._policy.apply(new_grade)
        return student

    def remove_student(self, student_id: int) -> bool:
        return self._repo.remove(student_id)

    # --- queries ---

    def find_by_last_name(self, last_name: str) -> list[Student]:
        needle = last_name.strip().lower()
        return [
            s for s in self._repo.all()
            if s.last_name.lower() == needle
        ]

    def filter_by_group(self, group: str) -> list[Student]:
        return [s for s in self._repo.all() if s.group == group]

    def best_student(self) -> Student | None:
        students = self._repo.all()
        if not students:
            return None
        return max(students, key=lambda s: s.average_grade)

    def average_of_group(self, group: str) -> float:
        students = self.filter_by_group(group)
        if not students:
            return 0.0
        total = sum(s.average_grade.value for s in students)
        return total / len(students)

    def export_all(self) -> str:
        return self._exporter.export(self._repo.all())

    def build_group(self, name: str) -> Group:
        group = Group(name=name)
        for student in self.filter_by_group(name):
            group.add_student(student.student_id)
        return group