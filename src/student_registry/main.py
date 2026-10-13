"""Application entry point — demonstration of the OOP model."""

from student_registry.models import Student
from student_registry.policies import RoundedPolicy
from student_registry.repositories import InMemoryRepository
from student_registry.services import StudentRegistryService
from student_registry.value_objects import Grade


# --- concrete adapters for Protocol-based dependencies ---

class ConsoleNotifier:
    """Adapter implementing Notifier Protocol."""

    def send(self, recipient: str, message: str) -> None:
        print(f"[notify -> {recipient}] {message}")


class CsvExporter:
    """Adapter implementing Exporter Protocol."""

    def export(self, students) -> str:  # type: ignore[no-untyped-def]
        lines = ["student_id,name,group,grade"]
        for s in students:
            lines.append(
                f"{s.student_id},{s.full_name},{s.group},{s.average_grade}"
            )
        return "\n".join(lines)


def create_demo_students() -> list[Student]:
    return [
        Student(1, "Anna", "Koval", "PI-21", Grade(91.5)),
        Student(2, "Oleh", "Melnyk", "PI-21", Grade(84.0)),
        Student(3, "Iryna", "Bondar", "PI-22", Grade(95.2)),
        Student(4, "Andrii", "Shevchenko", "PI-21", Grade(88.7)),
        Student(5, "Maria", "Boyko", "PI-22", Grade(79.3)),
    ]


def main() -> None:
    # Dependency Injection: всі залежності передаються ззовні
    service = StudentRegistryService(
        repository=InMemoryRepository[Student](),
        notifier=ConsoleNotifier(),
        exporter=CsvExporter(),
        grade_policy=RoundedPolicy(),
    )

    print("=" * 65)
    print("LAB 04 — OOP domain model (Variant 1: Student registry)")
    print("=" * 65)

    # register students
    print("\n=== REGISTERING STUDENTS ===")
    for student in create_demo_students():
        service.register_student(student)

    # list all
    print("\n=== ALL STUDENTS ===")
    for student in service._repo.all():
        print(student)

    # find by last name
    print("\n=== SEARCH: 'Melnyk' ===")
    for student in service.find_by_last_name("Melnyk"):
        print(student)

    # filter by group
    print("\n=== GROUP PI-21 ===")
    for student in service.filter_by_group("PI-21"):
        print(student)

    # average per group
    print("\n=== AVERAGE GRADES ===")
    for group_name in ("PI-21", "PI-22"):
        avg = service.average_of_group(group_name)
        print(f"  {group_name}: {avg:.2f}")

    # best student
    best = service.best_student()
    if best is not None:
        print(f"\nBest student: {best.full_name} ({best.average_grade})")

    # update grade
    print("\n=== UPDATE GRADE (id=2) ===")
    updated = service.update_grade(2, Grade(92.7))
    print(f"Updated: {updated}")

    # Group aggregate
    group_obj = service.build_group("PI-21")
    print(f"\nGroup {group_obj.name}: {len(group_obj)} students")
    print(f"Contains id=1? {1 in group_obj}")

    # export
    print("\n=== CSV EXPORT ===")
    print(service.export_all())


if __name__ == "__main__":
    main()