"""
Modulo: deducciones.py
 
Define la interfaz Deduccion y sus implementaciones concretas.
Misma logica de diseno que beneficios.py: interfaz minima (ISP) y clases
cerradas a modificacion pero abiertas a extension (OCP).
"""
 
from abc import ABC, abstractmethod
 
 
class Deduccion(ABC):
    """Contrato que debe cumplir cualquier deduccion obligatoria."""
 
    @abstractmethod
    def calcular(self, empleado, salario_bruto: float) -> float:
        """Devuelve el valor a descontar del salario bruto del empleado."""
        raise NotImplementedError
 
 
class DeduccionSeguridadSocial(Deduccion):
    """Deduccion obligatoria del 4% del salario bruto (seguro social y pension)."""
 
    PORCENTAJE = 0.04
 
    def calcular(self, empleado, salario_bruto: float) -> float:
        return salario_bruto * self.PORCENTAJE
 
 
class DeduccionARL(Deduccion):
    """
    Deduccion por ARL (riesgos laborales).
 
    El enunciado de la actividad no daba el porcentaje exacto; se usa 2%
    como valor por defecto. Sigue siendo configurable por si otro escenario de prueba necesita otra tasa.
    """
 
    PORCENTAJE_POR_DEFECTO = 0.02
 
    def __init__(self, porcentaje: float = PORCENTAJE_POR_DEFECTO) -> None:
        if porcentaje < 0:
            raise ValueError("El porcentaje de ARL no puede ser negativo")
        self.porcentaje = porcentaje
 
    def calcular(self, empleado, salario_bruto: float) -> float:
        return salario_bruto * self.porcentaje
 
    def calcular(self, empleado, salario_bruto: float) -> float:
        return salario_bruto * self.porcentaje
