import os
from build123d import *

# ==============================================================================
# Generador Oficial STEP 1:1 del Bastidor Real Medido en Taller
# Basado estrictamente en las 8 fotografías y croquis dimensional
# Perfilería de aluminio extruido 20x20 mm y escuadras triangulares de 90°
#
# Dimensiones reales de taller:
# - Altura columnas: 500 mm
# - Luz interior entre columnas: 500 mm
# - Ancho exterior total: 540 mm (20 + 500 + 20 mm)
# - Perfiles: Ranurado V-Slot / T-Slot 20x20 mm
# ==============================================================================

def create_2020_profile(length):
    """Crea un perfil de aluminio extruido 2020 con núcleo de 5mm y 4 ranuras estándar"""
    with BuildPart() as p:
        with BuildSketch() as s:
            Rectangle(20, 20)
            # Taladro central de 5 mm de diámetro (radio 2.5 mm)
            Circle(radius=2.5, mode=Mode.SUBTRACT)
            # Ranuras exteriores de 6 mm de ancho x 5.5 mm de profundidad
            with Locations((0, 10), (0, -10)):
                Rectangle(6, 11, mode=Mode.SUBTRACT)
            with Locations((10, 0), (-10, 0)):
                Rectangle(11, 6, mode=Mode.SUBTRACT)
        extrude(amount=length)
    return p.part

def create_corner_bracket():
    """Crea una escuadra triangular de fundición de aluminio de 90° (20x20x18 mm)"""
    with BuildPart() as b:
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 0), (20, 0))
                Line((20, 0), (0, 20))
                Line((0, 20), (0, 0))
            make_face()
        extrude(amount=18)
    return b.part

def build_real_frame():
    parts = []

    # Centrado en el origen (X = 0 es el centro del marco):
    # Luz interior: de X = -250 mm a X = +250 mm (500 mm)
    # Exterior: de X = -270 mm a X = +270 mm (540 mm)

    # 1. Columna Izquierda (Longitud 500 mm en Z, de Z = 0 a 500 mm)
    col_izq = Pos(-260, 0, 250) * Box(20, 20, 500) # O con sección 2020 detallada
    col_izq_det = Pos(-260, -10, 0) * create_2020_profile(500)
    parts.append(col_izq_det)

    # 2. Columna Derecha (Longitud 500 mm en Z, de Z = 0 a 500 mm)
    col_der_det = Pos(260, -10, 0) * create_2020_profile(500)
    parts.append(col_der_det)

    # 3. Travesaño Superior (Longitud 500 mm en X, de X = -250 a +250 mm)
    # Montado con su cara superior a Z = 480 mm
    trav_sup = Pos(-250, -10, 480) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_sup)

    # 4. Travesaño Inferior (Longitud 500 mm en X, de X = -250 a +250 mm)
    # Montado con su cara inferior a Z = 20 mm
    trav_inf = Pos(-250, -10, 20) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_inf)

    # 5. Las 4 Escuadras Triangulares de 90° (fundición de aluminio)
    # Escuadra Superior Izquierda (sobre el travesaño en X = -250 mm, Z = 480 mm)
    esc_sup_izq = Pos(-250, -9, 480) * create_corner_bracket()
    parts.append(esc_sup_izq)

    # Escuadra Superior Derecha (sobre el travesaño en X = +250 mm, Z = 480 mm)
    esc_sup_der = Pos(250, -9, 480) * (Rotation(0, -90, 0) * (Rotation(0, 0, 180) * create_corner_bracket()))
    parts.append(esc_sup_der)

    # Escuadra Inferior Izquierda (bajo el travesaño en X = -250 mm, Z = 20 mm)
    esc_inf_izq = Pos(-250, -9, 20) * (Rotation(0, 90, 0) * (Rotation(0, 0, 180) * create_corner_bracket()))
    parts.append(esc_inf_izq)

    # Escuadra Inferior Derecha (bajo el travesaño en X = +250 mm, Z = 20 mm)
    esc_inf_der = Pos(250, -9, 20) * (Rotation(0, 180, 0) * create_corner_bracket())
    parts.append(esc_inf_der)

    ensamblaje = Compound(children=parts)
    return ensamblaje

if __name__ == "__main__":
    out_step_1 = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Marco_Real_2020_TFG.step"
    out_step_2 = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Banco_Mecatronico_TFG.step"
    print("Construyendo modelo 1:1 EXACTO del marco de las fotos...")
    modelo = build_real_frame()
    export_step(modelo, out_step_1)
    export_step(modelo, out_step_2)
    print("Exportacion STEP completada con exito:")
    print(f" -> {out_step_1}")
    print(f" -> {out_step_2}")
