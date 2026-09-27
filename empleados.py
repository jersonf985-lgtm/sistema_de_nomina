"""
Modulo: empleados.py

Contiene la jerarquia de clases de empleados del sistema de nomina.

- Responsabilidad unica (SRP): cada subtipo de empleado solo sabe calcular
  su propio salario bruto. La orquestacion del salario neto (bruto +
  beneficios - deducciones) vive en la clase base Empleado.
- Abierto/cerrado (OCP): para agregar un nuevo tipo de empleado basta con
  crear una subclase nueva; no hace falta modificar Empleado ni las demas.
- Inversion de dependencias (DIP): Empleado no conoce clases concretas de
  beneficios o deducciones, solo las abstracciones Beneficio y Deduccion,
  que se inyectan desde afuera (ver fabrica.py).
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from beneficios import Beneficio, FondoAhorro
from deducciones import Deduccion


class Empleado(ABC):
    """Clase base abstracta para todos los tipos de empleado."""

    def __init__(
        self,
        id_empleado: str,
        nombre: str,
        fecha_ingreso: date,
        beneficios: Optional[List[Beneficio]] = None,
        deducciones: Optional[List[Deduccion]] = None,
    ) -> None:
        if not id_empleado:
            raise ValueError("El id del empleado no puede estar vacio")
        if not nombre:
            raise ValueError("El nombre del empleado no puede estar vacio")

        self.id_empleado = id_empleado
        self.nombre = nombre
        self.fecha_ingreso = fecha_ingreso
        self.beneficios: List[Beneficio] = beneficios or []
        self.deducciones: List[Deduccion] = deducciones or []

    @property
    def antiguedad_anios(self) -> float:
        """Anios completos (aproximados) que el empleado lleva en la empresa."""
        dias = (date.today() - self.fecha_ingreso).days
        return dias / 365.25

    @abstractmethod
    def calcular_salario_bruto(self) -> float:
        """Cada subtipo de empleado define su propia formula de salario bruto."""
        raise NotImplementedError

    def calcular_total_beneficios(self) -> float:
        return sum(beneficio.calcular(self) for beneficio in self.beneficios)

    def calcular_total_deducciones(self, salario_bruto: float) -> float:
        return sum(
            deduccion.calcular(self, salario_bruto) for deduccion in self.deducciones
        )

    def calcular_salario_neto(self) -> float:
        """
        Orquesta el calculo del salario neto: neto = bruto + beneficios - deducciones.
        Valida la regla de negocio de que el salario neto nunca sea negativo.
        """
        bruto = self.calcular_salario_bruto()
        total_beneficios = self.calcular_total_beneficios()
        total_deducciones = self.calcular_total_deducciones(bruto)

        neto = bruto + total_beneficios - total_deducciones
        if neto < 0:
            raise ValueError(
                f"El salario neto de {self.nombre} no puede ser negativo (dio {neto:.2f})"
            )
        return neto

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id_empleado!r}, nombre={self.nombre!r})"


class EmpleadoAsalariado(Empleado):
    """Empleado con salario fijo mensual."""

    def __init__(self, salario_mensual: float, **kwargs) -> None:
        super().__init__(**kwargs)
        if salario_mensual < 0:
            raise ValueError("El salario mensual no puede ser negativo")
        self.salario_mensual = salario_mensual

    def calcular_salario_bruto(self) -> float:
        return self.salario_mensual


class EmpleadoPorHoras(Empleado):
    """
    Empleado que cobra por horas trabajadas, con recargo en horas extra.
    No recibe bonos (regla de negocio). Puede tener acceso a un fondo de
    ahorro si acepta y lleva mas de 1 anio en la empresa.
    """

    HORAS_JORNADA_NORMAL = 40
    RECARGO_HORA_EXTRA = 1.5

    def __init__(
        self,
        tarifa_hora: float,
        horas_trabajadas: float,
        acepta_fondo_ahorro: bool = False,
        fondo_ahorro: Optional[FondoAhorro] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        if tarifa_hora < 0:
            raise ValueError("La tarifa por hora no puede ser negativa")
        if horas_trabajadas < 0:
            raise ValueError("Las horas trabajadas no pueden ser negativas")
        self.tarifa_hora = tarifa_hora
        self.horas_trabajadas = horas_trabajadas
        self.acepta_fondo_ahorro = acepta_fondo_ahorro
        # Inyeccion de dependencias con valor por defecto (DIP).
        self._fondo_ahorro = fondo_ahorro or FondoAhorro()

    def calcular_salario_bruto(self) -> float:
        if self.horas_trabajadas <= self.HORAS_JORNADA_NORMAL:
            return self.horas_trabajadas * self.tarifa_hora

        horas_normales = self.HORAS_JORNADA_NORMAL
        horas_extra = self.horas_trabajadas - self.HORAS_JORNADA_NORMAL
        return (horas_normales * self.tarifa_hora) + (
            horas_extra * self.tarifa_hora * self.RECARGO_HORA_EXTRA
        )

    def calcular_aporte_fondo_ahorro(self) -> float:
        """
        Aporte informativo al fondo de ahorro. Se reporta por separado y
        NO forma parte de calcular_salario_neto, ya que el enunciado no
        aclara si ese 2% se descuenta del neto o es un aporte aparte de
        la empresa (confirmar con el profesor o el CIPA).
        """
        return self._fondo_ahorro.calcular(self)


class EmpleadoPorComision(Empleado):
    """Empleado con salario base mas comision sobre ventas."""

    def __init__(
        self,
        salario_base: float,
        ventas: float,
        porcentaje_comision: float,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        if salario_base < 0:
            raise ValueError("El salario base no puede ser negativo")
        if ventas < 0:
            raise ValueError("Las ventas no pueden ser menores a $0")
        if porcentaje_comision < 0:
            raise ValueError("El porcentaje de comision no puede ser negativo")
        self.salario_base = salario_base
        self.ventas = ventas
        self.porcentaje_comision = porcentaje_comision

    def calcular_salario_bruto(self) -> float:
        return self.salario_base + (self.ventas * self.porcentaje_comision)


class EmpleadoTemporal(Empleado):
    """Empleado con salario fijo y contrato por tiempo definido, sin bonos ni beneficios."""

    def __init__(self, salario_mensual: float, fecha_fin_contrato: date, **kwargs) -> None:
        super().__init__(**kwargs)
        if salario_mensual < 0:
            raise ValueError("El salario mensual no puede ser negativo")
        self.salario_mensual = salario_mensual
        self.fecha_fin_contrato = fecha_fin_contrato

    def calcular_salario_bruto(self) -> float:
        return self.salario_mensual
