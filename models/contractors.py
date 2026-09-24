"""Контрагенты: класс Contractor и функции обработки коллекции."""

from __future__ import annotations


class Contractor:
    """Контрагент организации."""

    def __init__(self, contractor_id: int, name: str, inn: str) -> None:
        """Создать контрагента."""
        self.id = contractor_id
        self.name = name
        self.inn = inn

    def __str__(self) -> str:
        """Строковое представление контрагента."""
        return f"{self.name} (ИНН {self.inn})"

    @classmethod
    def from_data(cls, data: dict) -> "Contractor":
        """Создать контрагента из словаря."""
        return cls(
            contractor_id=data["id"],
            name=data["name"],
            inn=data["inn"],
        )

    def to_data(self) -> dict:
        """Преобразовать контрагента в словарь для JSON."""
        return {"id": self.id, "name": self.name, "inn": self.inn}


def add_contractor(
    contractors: list[Contractor],
    name: str,
    inn: str,
) -> Contractor:
    """Создать контрагента и добавить его в коллекцию."""
    new_id = max((c.id for c in contractors), default=0) + 1
    contractor = Contractor(new_id, name, inn)
    contractors.append(contractor)
    return contractor


def find_contractor(
    contractors: list[Contractor],
    query: str,
) -> list[Contractor]:
    """Найти контрагентов по подстроке в названии."""
    query_lower = query.lower()
    return [c for c in contractors if query_lower in c.name.lower()]


def find_contractor_by_id(
    contractors: list[Contractor],
    contractor_id: int,
) -> Contractor | None:
    """Найти контрагента по id."""
    for contractor in contractors:
        if contractor.id == contractor_id:
            return contractor
    return None


def show_contractors(contractors: list[Contractor]) -> None:
    """Вывести список контрагентов."""
    if not contractors:
        print("Список контрагентов пуст.")
        return
    print("\n=== Контрагенты ===")
    for contractor in contractors:
        print(f"[{contractor.id}] {contractor}")