# sistema_de_nomina
# Sistema de Nomina (POO + SOLID)

Actividad Unidad 3 - Ingenieria de Software (CIPA).
Sistema de nomina orientado a objetos para una empresa con distintos tipos
de empleados, cada uno con su propia forma de calcular salario, beneficios
y deducciones.

## Estructura del proyecto

```
sistema_nomina/
├── empleados.py     # Empleado (abstracta) + EmpleadoAsalariado, PorHoras, PorComision, Temporal
├── beneficios.py     # Beneficio (interfaz) + BonoAntiguedad, BonoAlimentacion, BonoComisionExtra, FondoAhorro
├── deducciones.py    # Deduccion (interfaz) + DeduccionSeguridadSocial, DeduccionARL
├── fabrica.py         # Funciones de fabrica: arman cada empleado con sus beneficios/deducciones
├── main.py            # Demo ejecutable
├── test_nomina.py      # 19 pruebas unitarias (unittest)
└── README.md
```

## Como ejecutar

```bash
# Demo con 4 empleados de ejemplo
python main.py

# Pruebas unitarias
python -m unittest test_nomina -v
```

Sin dependencias externas: solo usa la libreria estandar de Python.

## Aplicacion de principios SOLID

S (responsabilidad unica): `Empleado` solo orquesta el neto; cada
  subtipo solo calcula su propio bruto; cada beneficio/deduccion vive en
  su propia clase.
O (abierto/cerrado): agregar un tipo de empleado, un beneficio o una
  deduccion nueva no requiere tocar las clases existentes, solo crear una
  clase nueva y registrarla en `fabrica.py`.
-L (sustitucion de Liskov):cualquier subclase de `Empleado` puede
  usarse donde se espera un `Empleado` (por ejemplo en `imprimir_recibo`)
  sin romper el comportamiento.
-I (segregacion de interfaces):`Beneficio` y `Deduccion` son
  interfaces minimas de un solo metodo cada una.
-D (inversion de dependencias):`Empleado` depende de las
  abstracciones `Beneficio`/`Deduccion`, no de clases concretas; las
  listas se inyectan al construir cada empleado (`fabrica.py`).

## Decisiones y supuestos a confirmar con el profesor / CIPA

- El enunciado no especifica el porcentaje de ARL: se dejo configurable en
  `DeduccionARL` con un valor de referencia por defecto (0.522%, nivel de
  riesgo I). Ajustar si el profesor da un valor distinto.
- El fondo de ahorro (2%) se modela como informativo, separado del salario
  neto (`calcular_aporte_fondo_ahorro`), porque el enunciado no aclara si
  se descuenta del neto o es un aporte aparte de la empresa.

## Metodologia de desarrollo sugerida (Scrum ligero por sprints)

1.Sprint 1 - Analisis y diseno:modelado de clases, contratos SOLID,
   diagrama de clases (este sprint).
2.Sprint 2 - Implementacion con TDD:por cada regla de negocio se
   escribe primero la prueba unitaria y despues el codigo minimo que la
   hace pasar.
3.Sprint 3 - Integracion y refactorizacion:union de las piezas,
   revision de codigo limpio y cobertura de pruebas.
4.Sprint 4 - Documentacion y entrega:video explicando el diseno,
   commits descriptivos por sprint subidos a GitHub como evidencia del
   control de versiones.

## Sugerencia de commits para evidenciar control de version

```
git init
git add empleados.py beneficios.py deducciones.py
git commit -m "Sprint 1: diseño de clases con SOLID (Empleado, Beneficio, Deduccion)"
git add fabrica.py
git commit -m "Sprint 2: fabrica de empleados (inyeccion de dependencias)"
git add test_nomina.py
git commit -m "Sprint 2: pruebas unitarias (TDD) para reglas de negocio"
git add main.py README.md
git commit -m "Sprint 3-4: demo, documentacion y metodologia"
```
