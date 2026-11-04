"""
================================================================================
GENERADOR DEL ARCHIVO DE PROYECTO AUTODESK INVENTOR (.ipj)
Proyecto: Sistema Embebido de Control de Posición - TFG
Directorio: Parte mecanica/Inventor/scripts/generar_proyecto_ipj.py
================================================================================
Crea y activa el proyecto oficial 'Banco_Mecatronico_TFG.ipj' en el directorio
'Parte mecanica/Inventor', asegurando la correcta resolución de rutas relativas,
piezas (.ipt) y ensamblajes (.iam).
================================================================================
"""

import os
import sys

# Agregar ruta del módulo núcleo
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from inventor_core import InventorManager, inv

PROJECT_NAME = "Banco_Mecatronico_TFG"
INVENTOR_ROOT = os.path.dirname(SCRIPT_DIR) # Parte mecanica/Inventor
IPJ_PATH = os.path.join(INVENTOR_ROOT, f"{PROJECT_NAME}.ipj")


def crear_y_activar_proyecto():
    app = InventorManager.get_app()
    pm = app.DesignProjectManager
    
    print(f"[Proyecto IPJ] Directorio de trabajo: {INVENTOR_ROOT}")
    print(f"[Proyecto IPJ] Ruta de archivo de proyecto: {IPJ_PATH}")

    # Verificar si el archivo .ipj ya existe en disco
    if os.path.exists(IPJ_PATH):
        print(f"[Proyecto IPJ] Archivo existente detectado. Cargando y activando...")
        try:
            prj = pm.DesignProjects.AddExisting(IPJ_PATH)
            prj.Activate()
            print(f"[Proyecto IPJ] Proyecto '{prj.Name}' activado correctamente.")
            return prj
        except Exception as e:
            print(f"[Proyecto IPJ] Nota al cargar existente: {e}")
            # Si ya está en la colección, buscarlo por nombre
            for i in range(1, pm.DesignProjects.Count + 1):
                p = pm.DesignProjects.Item(i)
                if p.FullFileName.lower() == IPJ_PATH.lower():
                    p.Activate()
                    print(f"[Proyecto IPJ] Proyecto '{p.Name}' encontrado y activado.")
                    return p

    # Crear proyecto nuevo
    try:
        print("[Proyecto IPJ] Creando nuevo proyecto SingleUser...")
        prj = pm.DesignProjects.Add(
            inv.MultiUserModeEnum.kSingleUserMode,
            PROJECT_NAME,
            INVENTOR_ROOT
        )
        prj.Activate()
        print(f"[Proyecto IPJ] Proyecto '{PROJECT_NAME}' creado y activado con éxito.")
        return prj
    except Exception as e:
        print(f"[Proyecto IPJ] Error al crear proyecto: {e}")
        return None


if __name__ == "__main__":
    crear_y_activar_proyecto()
