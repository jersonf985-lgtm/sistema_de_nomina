"""
Modulo: test_nomina.py
 
Pruebas unitarias del sistema de nomina (metodologia TDD).
Ejecutar con: python -m unittest test_nomina -v
"""
 
import unittest
from datetime import date, timedelta
 
from beneficios import BonoAlimentacion, BonoAntiguedad, BonoComisionExtra
from deducciones import DeduccionARL, DeduccionSeguridadSocial
from empleados import (
    EmpleadoAsalariado,
    EmpleadoPorComision,
    EmpleadoPorHoras,
    EmpleadoTemporal,
)
 
HACE_7_ANIOS = date.today() - timedelta(days=365 * 7)
HACE_2_ANIOS = date.today() - timedelta(days=365 * 2)
 
 
class TestEmpleadoAsalariado(unittest.TestCase):
    def test_salario_bruto_es_el_salario_mensual(self):
        empleado = EmpleadoAsalariado(
            id_empleado="E1", nombre="Ana", fecha_ingreso=HACE_2_ANIOS, salario_mensual=2_000_000
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 2_000_000)
 
    def test_recibe_bono_antiguedad_con_mas_de_5_anios(self):
        empleado = EmpleadoAsalariado(
            id_empleado="E2",
            nombre="Luis",
            fecha_ingreso=HACE_7_ANIOS,
            salario_mensual=2_000_000,
            beneficios=[BonoAntiguedad()],
        )
        self.assertAlmostEqual(empleado.calcular_total_beneficios(), 200_000)
 
    def test_no_recibe_bono_antiguedad_con_menos_de_5_anios(self):
        empleado = EmpleadoAsalariado(
            id_empleado="E3",
            nombre="Marta",
            fecha_ingreso=HACE_2_ANIOS,
            salario_mensual=2_000_000,
            beneficios=[BonoAntiguedad()],
        )
        self.assertEqual(empleado.calcular_total_beneficios(), 0)
 
    def test_salario_mensual_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            EmpleadoAsalariado(
                id_empleado="E4", nombre="Pedro", fecha_ingreso=HACE_2_ANIOS, salario_mensual=-100
            )
 
 
class TestEmpleadoPorHoras(unittest.TestCase):
    def test_sin_horas_extra(self):
        empleado = EmpleadoPorHoras(
            id_empleado="H1",
            nombre="Sara",
            fecha_ingreso=HACE_2_ANIOS,
            tarifa_hora=10_000,
            horas_trabajadas=40,
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 400_000)
 
    def test_con_horas_extra_recarga_1_5(self):
        empleado = EmpleadoPorHoras(
            id_empleado="H2",
            nombre="Ivan",
            fecha_ingreso=HACE_2_ANIOS,
            tarifa_hora=10_000,
            horas_trabajadas=48,
        )
        esperado = (40 * 10_000) + (8 * 10_000 * 1.5)
        self.assertEqual(empleado.calcular_salario_bruto(), esperado)
 
    def test_horas_negativas_lanza_error(self):
        with self.assertRaises(ValueError):
            EmpleadoPorHoras(
                id_empleado="H3",
                nombre="Eva",
                fecha_ingreso=HACE_2_ANIOS,
                tarifa_hora=10_000,
                horas_trabajadas=-5,
            )
 
    def test_no_recibe_bonos(self):
        empleado = EmpleadoPorHoras(
            id_empleado="H4",
            nombre="Tomas",
            fecha_ingreso=HACE_7_ANIOS,
            tarifa_hora=10_000,
            horas_trabajadas=40,
        )
        self.assertEqual(empleado.calcular_total_beneficios(), 0)
 
    def test_fondo_ahorro_si_acepta_y_mas_de_1_anio(self):
        empleado = EmpleadoPorHoras(
            id_empleado="H5",
            nombre="Nora",
            fecha_ingreso=HACE_2_ANIOS,
            tarifa_hora=10_000,
            horas_trabajadas=40,
            acepta_fondo_ahorro=True,
        )
        self.assertGreater(empleado.calcular_aporte_fondo_ahorro(), 0)
 
    def test_fondo_ahorro_no_aplica_si_no_acepta(self):
        empleado = EmpleadoPorHoras(
            id_empleado="H6",
            nombre="Iris",
            fecha_ingreso=HACE_2_ANIOS,
            tarifa_hora=10_000,
            horas_trabajadas=40,
            acepta_fondo_ahorro=False,
        )
        self.assertEqual(empleado.calcular_aporte_fondo_ahorro(), 0)
 
 
class TestEmpleadoPorComision(unittest.TestCase):
    def test_salario_bruto_base_mas_comision(self):
        empleado = EmpleadoPorComision(
            id_empleado="C1",
            nombre="Diego",
            fecha_ingreso=HACE_2_ANIOS,
            salario_base=1_000_000,
            ventas=5_000_000,
            porcentaje_comision=0.10,
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 1_500_000)
 
    def test_bono_extra_si_ventas_superan_20_millones(self):
        empleado = EmpleadoPorComision(
            id_empleado="C2",
            nombre="Lucia",
            fecha_ingreso=HACE_2_ANIOS,
            salario_base=1_000_000,
            ventas=25_000_000,
            porcentaje_comision=0.10,
            beneficios=[BonoComisionExtra()],
        )
        self.assertEqual(empleado.calcular_total_beneficios(), 750_000)
 
    def test_sin_bono_extra_si_ventas_no_superan_el_umbral(self):
        empleado = EmpleadoPorComision(
            id_empleado="C3",
            nombre="Mario",
            fecha_ingreso=HACE_2_ANIOS,
            salario_base=1_000_000,
            ventas=15_000_000,
            porcentaje_comision=0.10,
            beneficios=[BonoComisionExtra()],
        )
        self.assertEqual(empleado.calcular_total_beneficios(), 0)
 
    def test_ventas_negativas_lanza_error(self):
        with self.assertRaises(ValueError):
            EmpleadoPorComision(
                id_empleado="C4",
                nombre="Rosa",
                fecha_ingreso=HACE_2_ANIOS,
                salario_base=1_000_000,
                ventas=-1,
                porcentaje_comision=0.10,
            )
 
 
class TestEmpleadoTemporal(unittest.TestCase):
    def test_salario_bruto_fijo_sin_beneficios(self):
        empleado = EmpleadoTemporal(
            id_empleado="T1",
            nombre="Julio",
            fecha_ingreso=HACE_2_ANIOS,
            salario_mensual=1_800_000,
            fecha_fin_contrato=date.today() + timedelta(days=180),
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 1_800_000)
        self.assertEqual(empleado.calcular_total_beneficios(), 0)
 
 
class TestDeducciones(unittest.TestCase):
    def test_seguridad_social_es_4_por_ciento(self):
        deduccion = DeduccionSeguridadSocial()
        self.assertEqual(deduccion.calcular(None, 1_000_000), 40_000)
 
    def test_arl_valor_por_defecto_es_2_por_ciento(self):
        deduccion = DeduccionARL()
        self.assertEqual(deduccion.calcular(None, 1_000_000), 20_000)
 
    def test_arl_usa_porcentaje_configurable(self):
        deduccion = DeduccionARL(porcentaje=0.01)
        self.assertEqual(deduccion.calcular(None, 1_000_000), 10_000)
 
    def test_arl_porcentaje_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            DeduccionARL(porcentaje=-0.01)
 
 
class TestSalarioNeto(unittest.TestCase):
    def test_neto_combina_bruto_beneficios_y_deducciones(self):
        empleado = EmpleadoAsalariado(
            id_empleado="N1",
            nombre="Vero",
            fecha_ingreso=HACE_7_ANIOS,
            salario_mensual=2_000_000,
            beneficios=[BonoAntiguedad(), BonoAlimentacion()],
            deducciones=[DeduccionSeguridadSocial()],
        )
        bruto = 2_000_000
        beneficios = (0.10 * bruto) + 1_000_000
        deducciones = 0.04 * bruto
        esperado = bruto + beneficios - deducciones
        self.assertAlmostEqual(empleado.calcular_salario_neto(), esperado)
 
 
if __name__ == "__main__":
    unittest.main()
 
