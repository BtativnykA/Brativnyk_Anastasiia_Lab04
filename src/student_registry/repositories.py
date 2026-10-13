"""Generic in-memory repository."""

from typing import Generic, Protocol, TypeVar

from student_registry.exceptions import DuplicateError, NotFoundError


class HasId(Protocol):
    """Anything with an integer `student_id`."""

    student_id: int


T = TypeVar("T", bound=HasId)


class InMemoryRepository(Generic[T]):
    """Generic in-memory repository keyed by `.student_id`."""

    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def add(self, item: T) -> None:
        if item.student_id in self._items:
            raise DuplicateError(
                f"Item with id={item.student_id} already exists"
            )
        self._items[item.student_id] = item

    def get(self, item_id: int) -> T | None:
        return self._items.get(item_id)

    def require(self, item_id: int) -> T:
        item = self._items.get(item_id)
        if item is None:
            raise NotFoundError(f"Item id={item_id} not found")
        return item

    def all(self) -> list[T]:
        return list(self._items.values())

    def remove(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self._items.values())

    def __contains__(self, item_id: int) -> bool:
        return item_id in self._items