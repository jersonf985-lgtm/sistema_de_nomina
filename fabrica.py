"""
Modulo: fabrica.py

Funciones de fabrica que ensamblan cada tipo de empleado con los
beneficios y deducciones que le corresponden segun las reglas de negocio.

Mantener esta decision aqui (y no dentro de Empleado) respeta la
responsabilidad unica: Empleado no necesita saber que beneficios existen
en el sistema, solo sabe usarlos a traves de la interfaz Beneficio/Deduccion.
"""

from datetime import date

from beneficios import BonoAlimentacion, BonoAntiguedad, BonoComisionExtra
from deducciones import DeduccionARL, DeduccionSeguridadSocial
from empleados import (
    EmpleadoAsalariado,
    EmpleadoPorComision,
    EmpleadoPorHoras,
    EmpleadoTemporal,
)


def crear_empleado_asalariado(
    id_empleado: str, nombre: str, fecha_ingreso: date, salario_mensual: float
) -> EmpleadoAsalariado:
    return EmpleadoAsalariado(
        id_empleado=id_empleado,
        nombre=nombre,
        fecha_ingreso=fecha_ingreso,
        salario_mensual=salario_mensual,
        beneficios=[BonoAntiguedad(), BonoAlimentacion()],
        deducciones=[DeduccionSeguridadSocial(), DeduccionARL()],
    )


def crear_empleado_por_horas(
    id_empleado: str,
    nombre: str,
    fecha_ingreso: date,
    tarifa_hora: float,
    horas_trabajadas: float,
    acepta_fondo_ahorro: bool = False,
) -> EmpleadoPorHoras:
    return EmpleadoPorHoras(
        id_empleado=id_empleado,
        nombre=nombre,
        fecha_ingreso=fecha_ingreso,
        tarifa_hora=tarifa_hora,
        horas_trabajadas=horas_trabajadas,
        acepta_fondo_ahorro=acepta_fondo_ahorro,
        beneficios=[],  # Regla de negocio: no reciben bonos
        deducciones=[DeduccionSeguridadSocial(), DeduccionARL()],
    )


def crear_empleado_por_comision(
    id_empleado: str,
    nombre: str,
    fecha_ingreso: date,
    salario_base: float,
    ventas: float,
    porcentaje_comision: float,
) -> EmpleadoPorComision:
    return EmpleadoPorComision(
        id_empleado=id_empleado,
        nombre=nombre,
        fecha_ingreso=fecha_ingreso,
        salario_base=salario_base,
        ventas=ventas,
        porcentaje_comision=porcentaje_comision,
        beneficios=[BonoComisionExtra(), BonoAlimentacion()],
        deducciones=[DeduccionSeguridadSocial(), DeduccionARL()],
    )


def crear_empleado_temporal(
    id_empleado: str,
    nombre: str,
    fecha_ingreso: date,
    salario_mensual: float,
    fecha_fin_contrato: date,
) -> EmpleadoTemporal:
    return EmpleadoTemporal(
        id_empleado=id_empleado,
        nombre=nombre,
        fecha_ingreso=fecha_ingreso,
        salario_mensual=salario_mensual,
        fecha_fin_contrato=fecha_fin_contrato,
        beneficios=[],  # Regla de negocio: sin bonos ni beneficios adicionales
        deducciones=[DeduccionSeguridadSocial(), DeduccionARL()],
    )
