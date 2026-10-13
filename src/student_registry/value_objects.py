"""Immutable value objects."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grade:
    """Immutable numeric grade with validation."""

    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 100.0:
            raise ValueError(
                f"Grade must be in [0, 100], got {self.value}"
            )

    def __add__(self, other: "Grade") -> "Grade":
        return Grade((self.value + other.value) / 2)

    def __lt__(self, other: "Grade") -> bool:
        return self.value < other.value

    def __str__(self) -> str:
        return f"{self.value:.2f}"

    def __format__(self, format_spec: str) -> str:
        """Delegate format spec to the underlying float.

        Enables f-strings like f"{grade:.2f}" or f"{grade:>7}".
        """
        return format(self.value, format_spec)