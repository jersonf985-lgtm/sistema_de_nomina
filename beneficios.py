"""
Modulo: beneficios.py

Define la interfaz Beneficio y sus implementaciones concretas.

- Segregacion de interfaces (ISP): Beneficio es una interfaz minima con un
  solo metodo; ninguna clase se ve obligada a implementar algo que no usa.
- Abierto/cerrado (OCP): agregar un beneficio nuevo no obliga a modificar
  Empleado ni los demas beneficios ya existentes.
"""

from abc import ABC, abstractmethod


class Beneficio(ABC):
    """Contrato que debe cumplir cualquier beneficio o bono."""

    @abstractmethod
    def calcular(self, empleado) -> float:
        """Devuelve el valor del beneficio para el empleado dado."""
        raise NotImplementedError


class BonoAntiguedad(Beneficio):
    """Bono del 10% del salario bruto para empleados con mas de 5 anios."""

    PORCENTAJE_BONO = 0.10
    ANIOS_MINIMOS = 5

    def calcular(self, empleado) -> float:
        if empleado.antiguedad_anios > self.ANIOS_MINIMOS:
            return empleado.calcular_salario_bruto() * self.PORCENTAJE_BONO
        return 0.0


class BonoAlimentacion(Beneficio):
    """Bono fijo mensual para empleados permanentes (asalariados y por comision)."""

    VALOR_MENSUAL = 1_000_000.0

    def calcular(self, empleado) -> float:
        return self.VALOR_MENSUAL


class BonoComisionExtra(Beneficio):
    """
    Bono adicional del 3% sobre las ventas cuando estas superan $20.000.000.
    Solo tiene efecto en empleados que tengan el atributo `ventas`
    (empleados por comision).
    """

    UMBRAL_VENTAS = 20_000_000.0
    PORCENTAJE_BONO = 0.03

    def calcular(self, empleado) -> float:
        ventas = getattr(empleado, "ventas", 0)
        if ventas > self.UMBRAL_VENTAS:
            return ventas * self.PORCENTAJE_BONO
        return 0.0


class FondoAhorro(Beneficio):
    """
    Aporte del 2% del salario a un fondo de ahorro, para empleados por
    horas con mas de 1 anio que hayan aceptado el acceso al fondo.

    Se usa de forma separada del calculo del salario neto (ver
    EmpleadoPorHoras.calcular_aporte_fondo_ahorro en empleados.py), porque
    el enunciado no aclara si ese 2% se descuenta del neto o es un aporte
    aparte de la empresa.
    """

    PORCENTAJE_APORTE = 0.02
    ANIOS_MINIMOS = 1

    def calcular(self, empleado) -> float:
        acepta = getattr(empleado, "acepta_fondo_ahorro", False)
        if acepta and empleado.antiguedad_anios > self.ANIOS_MINIMOS:
            return empleado.calcular_salario_bruto() * self.PORCENTAJE_APORTE
        return 0.0
