"""
================================================================================
SCRIPT MAESTRO INTEGRAL DE AUTODESK INVENTOR 2027
Proyecto: Banco Mecatrónico TFG - Microgravedad Simulada
Directorio: Parte mecanica/Inventor/scripts/ejecutar_todo_inventor.py
================================================================================
Ejecuta la secuencia completa de diseño mecatrónico en Autodesk Inventor:
1. Creación y activación del proyecto oficial (Banco_Mecatronico_TFG.ipj).
2. Generación de las 11 piezas paramétricas (.ipt) en 'piezas/'.
3. Generación de los 4 subensamblajes y el ensamblaje maestro (.iam) en 'ensamblajes/'.
================================================================================
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from generar_proyecto_ipj import crear_y_activar_proyecto
from generar_piezas_ipt import crear_todas_las_piezas
from generar_cubo_con_cintas import construir_cubo_con_cintas


def ejecutar_flujo_completo():
    print("================================================================================")
    print("🚀 INICIANDO CONSTRUCCIÓN INTEGRAL CAD EN AUTODESK INVENTOR 2027")
    print("================================================================================")

    # Paso 1: Configurar Proyecto IPJ
    print("\n--- PASO 1: CONFIGURACIÓN DEL PROYECTO IPJ ---")
    crear_y_activar_proyecto()

    # Paso 2: Generar Catálogo de Piezas IPT
    print("\n--- PASO 2: GENERACIÓN DE PIEZAS PARAMÉTRICAS IPT ---")
    crear_todas_las_piezas()

    # Paso 3: Generar Cubo 50x54 cm con Cintas y 4 Perfiles Apoyados
    print("\n--- PASO 3: ENSAMBLAJE DEL CUBO CON CINTAS Y 4 PERFILES ---")
    construir_cubo_con_cintas()

    print("\n================================================================================")
    print("🎉 MODELADO MECATRÓNICO EN AUTODESK INVENTOR COMPLETADO CON ÉXITO")
    print("================================================================================")


if __name__ == "__main__":
    ejecutar_flujo_completo()
