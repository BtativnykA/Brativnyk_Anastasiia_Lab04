"""Abstractions: Protocol for duck-typed interfaces, ABC for hierarchies."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Protocol

from student_registry.models import Student


class Notifier(Protocol):
    """Structural interface for notifications (Protocol)."""

    def send(self, recipient: str, message: str) -> None:
        ...


class Exporter(Protocol):
    """Structural interface for exporters (Protocol)."""

    def export(self, students: Iterable[Student]) -> str:
        ...


class StudentRepository(ABC):
    """Abstract base class for repositories."""

    @abstractmethod
    def add(self, student: Student) -> None: ...

    @abstractmethod
    def get(self, student_id: int) -> Student | None: ...

    @abstractmethod
    def all(self) -> list[Student]: ...

    @abstractmethod
    def remove(self, student_id: int) -> bool: ...