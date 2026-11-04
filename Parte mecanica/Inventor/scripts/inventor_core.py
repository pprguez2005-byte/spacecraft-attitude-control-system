"""
================================================================================
MÓDULO NÚCLEO DE AUTOMATIZACIÓN DE AUTODESK INVENTOR 2027 (adsk.inventor)
Proyecto: Sistema Embebido de Control de Posición - TFG
Directorio: Parte mecanica/Inventor/scripts/inventor_core.py
================================================================================
Proporciona conexión centralizada, gestión de unidades (mm <-> cm interno),
creación de geometrías transitorias y utilidades de modelado.
================================================================================
"""

import sys
import os
import math

# Asegurar acceso al paquete nativo PythonBindings de Autodesk Inventor 2027
INVENTOR_BINDINGS = r"C:\Program Files\Autodesk\Inventor 2027\Bin\PythonBindings"
if INVENTOR_BINDINGS not in sys.path:
    sys.path.insert(0, INVENTOR_BINDINGS)

import adsk.inventor as inv


class InventorManager:
    """Administrador centralizado de la sesión de Autodesk Inventor."""
    _instance = None
    _app = None

    @classmethod
    def get_app(cls) -> inv.Application:
        """Obtiene la aplicación activa de Inventor o la inicializa."""
        if cls._app is None:
            print("[InventorManager] Inicializando conexión con Autodesk Inventor 2027...")
            try:
                # Intentar conectar a la instancia en ejecución
                cls._app = inv.connect()
                print(f"[InventorManager] Conectado exitosamente. Versión: {cls._app.SoftwareVersion.DisplayVersion}")
            except Exception:
                # Si no está en el ROT, lanzar la aplicación
                print("[InventorManager] Lanzando instancia de Inventor...")
                cls._app = inv.launch()
                print(f"[InventorManager] Lanzamiento completado. Versión: {cls._app.SoftwareVersion.DisplayVersion}")
            
            # Asegurar visibilidad para el diseñador
            try:
                cls._app.Visible = True
            except Exception:
                pass
        return cls._app


def mm(val_mm: float) -> float:
    """Convierte milímetros a centímetros (unidad interna de longitud de Inventor API)."""
    return float(val_mm) / 10.0


def pt2d(app: inv.Application, x_mm: float, y_mm: float):
    """Crea un objeto Point2d con coordenadas en milímetros."""
    return app.TransientGeometry.CreatePoint2d(mm(x_mm), mm(y_mm))


def pt3d(app: inv.Application, x_mm: float, y_mm: float, z_mm: float):
    """Crea un objeto Point con coordenadas en milímetros."""
    return app.TransientGeometry.CreatePoint(mm(x_mm), mm(y_mm), mm(z_mm))


def vec3d(app: inv.Application, x: float, y: float, z: float):
    """Crea un Vector 3D unitario o direccional."""
    return app.TransientGeometry.CreateVector(float(x), float(y), float(z))


def matrix_transform(app: inv.Application, x_mm=0.0, y_mm=0.0, z_mm=0.0, 
                     rot_x_deg=0.0, rot_y_deg=0.0, rot_z_deg=0.0):
    """
    Crea una matriz 4x4 de posicionamiento para componentes en ensamblajes (.iam).
    Aplica rotaciones en X, Y, Z (en grados) y traslación en milímetros.
    """
    tg = app.TransientGeometry
    mat = tg.CreateMatrix()
    
    # Rotación en X
    if abs(rot_x_deg) > 1e-4:
        mx = tg.CreateMatrix()
        mx.SetToRotation(math.radians(rot_x_deg), tg.CreateVector(1, 0, 0), tg.CreatePoint(0, 0, 0))
        mat.TransformBy(mx)
        
    # Rotación en Y
    if abs(rot_y_deg) > 1e-4:
        my = tg.CreateMatrix()
        my.SetToRotation(math.radians(rot_y_deg), tg.CreateVector(0, 1, 0), tg.CreatePoint(0, 0, 0))
        mat.TransformBy(my)
        
    # Rotación en Z
    if abs(rot_z_deg) > 1e-4:
        mz = tg.CreateMatrix()
        mz.SetToRotation(math.radians(rot_z_deg), tg.CreateVector(0, 0, 1), tg.CreatePoint(0, 0, 0))
        mat.TransformBy(mz)
        
    # Traslación final
    mat.SetTranslation(tg.CreateVector(mm(x_mm), mm(y_mm), mm(z_mm)), False)
    return mat
