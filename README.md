# Student Registry

Лабораторна робота №4 з курсу «Професійний Python».
Варіант №1 — «Система обліку студентів» (ООП + type hints).

## Description

Типізована об'єктна модель предметної області з використанням:
класів, композиції, наслідування, ABC, Protocol, dataclass,
properties, dunder methods, SOLID, Generic, TypeVar, TypedDict.

## Features

- domain entities: `Student`, `Group`, `AcademicRecord`;
- immutable value object: `Grade` (frozen dataclass);
- ABC: `StudentRepository`, `GradePolicy`;
- Protocol: `Notifier`, `Exporter`, `HasId`;
- Generic repository: `InMemoryRepository[Student]`;
- dependency injection через конструктор `StudentRegistryService`;
- TypeVar з bound + TypedDict payload;
- SOLID: SRP, OCP, DIP;
- type checking через mypy --strict.

## Requirements

Python 3.11+

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"