"""Unit conversion: plain functions with no MCP or I/O concerns."""

from typing import Final

# Each unit's factor to its quantity's base unit (metre for length, gram for mass).
_LENGTH: Final[dict[str, float]] = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "ft": 0.3048,
    "in": 0.0254,
    "mi": 1609.344,
}
_MASS: Final[dict[str, float]] = {
    "g": 1.0,
    "kg": 1000.0,
    "lb": 453.59237,
    "oz": 28.349523125,
}
_QUANTITIES: Final[dict[str, dict[str, float]]] = {"length": _LENGTH, "mass": _MASS}


class UnitError(ValueError):
    """Raised for an unknown unit, or for a conversion between different quantities."""


def supported_units() -> list[str]:
    """Return every unit name that :func:`convert` accepts, sorted."""
    return sorted(unit for table in _QUANTITIES.values() for unit in table)


def _lookup(unit: str) -> tuple[str, float]:
    """Return the quantity name and the base-unit factor for ``unit``."""
    for quantity, table in _QUANTITIES.items():
        if unit in table:
            return quantity, table[unit]
    raise UnitError(f"unknown unit {unit!r}; supported units: {', '.join(supported_units())}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Raises:
        UnitError: if either unit is unknown, or the units measure different quantities.
    """
    from_quantity, from_factor = _lookup(from_unit)
    to_quantity, to_factor = _lookup(to_unit)
    if from_quantity != to_quantity:
        raise UnitError(
            f"cannot convert {from_unit} ({from_quantity}) to {to_unit} ({to_quantity})"
        )
    return value * from_factor / to_factor
