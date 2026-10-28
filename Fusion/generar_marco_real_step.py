#!/usr/bin/env python3
"""
================================================================================
GENERADOR MAESTRO 1:1 CAD DEL MARCO REAL DE TALLER (STEP + OBJ + STL)
Proyecto: Banco Mecatrónico TFG - Simulación Satelital
Autor: Antigravity AI Pair Programmer
Fecha: 28-10-2026
================================================================================
Fiel reconstrucción física basada en las fotografías macro y croquis de taller:
1. Perfilería de aluminio extruido 2020 Slot 6 (T-Slot estándar europeo):
   - Sección transversal de 20x20 mm con chaflanes exteriores a 45° (1.0 mm)
   - Bocas exteriores planas de 6.2 mm de luz (sin rebajes triangulares exteriores erróneos)
   - Labios de 1.8 mm de espesor con transición interior biselada a 45°
   - Bolsillo interior de 11.0 mm de ancho x 4.2 mm de profundidad
   - Núcleo tubular central con taladro circular de 4.2 mm (roscable M5)
   - 4 nervios diagonales a 45° de 1.8 mm de espesor
2. Escuadras de 90° de fundición de aluminio (20x20x20 mm):
   - Montadas en el exterior de las esquinas (en los peldaños de 20 mm)
   - Dos nervios triangulares laterales de 3.0 mm de espesor
   - Bolsillo central vaciado de 14.0 mm de ancho
   - Dos taladros pasantes de 5.5 mm para tornillería M5
3. Tornillería M5 con arandela (ISO 7380 / DIN 125):
   - Cabeza alomada de 9.2 mm de diámetro x 2.6 mm con arandela plana de 10.0 mm
   - Posiciones de tornillos modeladas según el prototipo físico real de taller,
     reflejando fielmente las escuadras con tornillos instalados y los taladros
     vacíos donde falta el tornillo en los travesaños horizontales.
================================================================================
"""

import os
import sys
from build123d import *

# ------------------------------------------------------------------------------
# 1. Definición de la Sección Transversal Real 2020
# ------------------------------------------------------------------------------
def create_true_2020_sketch():
    """Genera el sketch 2D exacto del perfil 2020 T-Slot normalizado"""
    with BuildSketch() as s:
        # Cuadrado envolvente 20x20 mm
        Rectangle(20.0, 20.0)
        # Chaflanes a 45° en las cuatro esquinas exteriores (como se aprecia en la macro)
        chamfer(s.vertices(), length=1.0)
        
        # 4 ranuras T-slot simétricas
        for angle in [0, 90, 180, 270]:
            with Locations(Rotation(0, 0, angle)):
                # Boca de entrada exterior: 6.2 mm de ancho x 2.0 mm (de y = 8.1 a 10.1)
                with Locations((0, 9.1)):
                    Rectangle(6.2, 2.0, mode=Mode.SUBTRACT)
                # Cavidad interior ensanchada: 11.0 mm de ancho x 4.2 mm de profundidad
                with Locations((0, 6.1)):
                    Rectangle(11.0, 4.2, mode=Mode.SUBTRACT)
                # Biseles interiores de los labios a 45°
                with Locations((-3.1, 8.2)):
                    Triangle(a=1.2, b=1.2, C=90, rotation=180, mode=Mode.SUBTRACT)
                with Locations((3.1, 8.2)):
                    Triangle(a=1.2, b=1.2, C=90, rotation=270, mode=Mode.SUBTRACT)

        # Taladro circular del núcleo central de 4.2 mm de diámetro (M5)
        Circle(radius=2.1, mode=Mode.SUBTRACT)

    return s.sketch

def create_2020_profile_extrusion(length):
    """Extruye el perfil 2020 a lo largo del eje Z"""
    with BuildPart() as p:
        insert(create_true_2020_sketch())
        extrude(amount=length)
    return p.part

# ------------------------------------------------------------------------------
# 2. Escuadra de Fundición de Aluminio de 90° (20x20x20 mm)
# ------------------------------------------------------------------------------
def create_die_cast_bracket():
    """
    Escuadra de fundición de aluminio 20x20x20 mm:
    - Base en Z=0 (X de 0 a 20 mm, Y de -10 a +10 mm, espesor 3 mm)
    - Pared trasera en X=0 (Z de 0 a 20 mm, Y de -10 a +10 mm, espesor 3 mm)
    - Dos nervios laterales triangulares de 3 mm de espesor (Y de -10 a -7 y de 7 a 10)
    - Vaciado central de 14 mm de ancho (Y de -7 a +7 mm)
    - Taladro de 5.5 mm en la base horizontal (en X = 9.5 mm, Y = 0)
    - Taladro de 5.5 mm en la pared vertical (en Z = 9.5 mm, Y = 0)
    """
    with BuildPart() as b:
        # Prisma triangular macizo base (20x20x20 mm, centrado en Y de -10 a +10)
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 0), (20, 0))
                Line((20, 0), (0, 20))
                Line((0, 20), (0, 0))
            make_face()
        extrude(amount=10, both=True)

        # Vaciado del bolsillo central entre los nervios (ancho = 14 mm, de Y = -7 a +7)
        with BuildSketch(Plane.XZ) as s_pocket:
            with BuildLine() as lp:
                Line((3.0, 3.0), (17.0, 3.0))
                Line((17.0, 3.0), (3.0, 17.0))
                Line((3.0, 17.0), (3.0, 3.0))
            make_face()
        extrude(amount=7, both=True, mode=Mode.SUBTRACT)

        # Taladro pasante de 5.5 mm en la base horizontal (para tornillo M5)
        with Locations((9.5, 0, 0)):
            Cylinder(radius=2.75, height=10.0, mode=Mode.SUBTRACT)

        # Taladro pasante de 5.5 mm en la pared vertical (para tornillo M5)
        with Locations((0, 0, 9.5)):
            Rotation(0, 90, 0) * Cylinder(radius=2.75, height=10.0, mode=Mode.SUBTRACT)

    return b.part

# ------------------------------------------------------------------------------
# 3. Tornillo M5 con Arandela (Pan-Head ISO 7380 / DIN 7985)
# ------------------------------------------------------------------------------
def create_m5_screw_with_washer():
    """
    Crea el conjunto de tornillo M5 de cabeza alomada con arandela plana DIN 125:
    - Arandela: diámetro exterior 10.0 mm, espesor 1.0 mm
    - Cabeza alomada: diámetro 9.2 mm, altura 2.6 mm
    - Espárrago roscado: diámetro 4.9 mm, longitud 8.0 mm
    """
    with BuildPart() as p:
        # Arandela DIN 125
        Cylinder(radius=5.0, height=1.0)
        # Cabeza alomada mediante revolución
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 1.0), (4.6, 1.0))
                Line((4.6, 1.0), (4.6, 2.0))
                ThreePointArc((4.6, 2.0), (3.0, 3.5), (0, 3.5))
                Line((0, 3.5), (0, 1.0))
            make_face()
        revolve(axis=Axis.Z)
        # Espárrago roscado M5
        with Locations((0, 0, -4.0)):
            Cylinder(radius=2.45, height=8.0)
    return p.part

# ------------------------------------------------------------------------------
# 4. Construcción del Bastidor Completo
# ------------------------------------------------------------------------------
def build_real_frame():
    parts = []

    print("Construyendo perfiles 2020 con sección fotorrealista T-Slot...")
    # 1. Columna Izquierda (Longitud 500 mm en vertical Z)
    # Centrada en X = -260 mm (de X = -270 a -250 mm, Y de -10 a +10 mm)
    col_izq = Pos(-260, 0, 0) * create_2020_profile_extrusion(500)
    parts.append(col_izq)

    # 2. Columna Derecha (Longitud 500 mm en vertical Z)
    # Centrada en X = +260 mm (de X = +250 a 270 mm, Y de -10 a +10 mm)
    col_der = Pos(260, 0, 0) * create_2020_profile_extrusion(500)
    parts.append(col_der)

    # 3. Travesaño Superior (Longitud 500 mm en horizontal X)
    # Entre X = -250 mm y X = +250 mm (luz interior de 500 mm)
    # Centrado en Z = 470 mm (cara inferior a 460 mm, superior a 480 mm)
    trav_sup = Pos(-250, 0, 470) * (Rotation(0, 90, 0) * create_2020_profile_extrusion(500))
    parts.append(trav_sup)

    # 4. Travesaño Inferior (Longitud 500 mm en horizontal X)
    # Entre X = -250 mm y X = +250 mm
    # Centrado en Z = 30 mm (cara inferior a 20 mm, superior a 40 mm)
    trav_inf = Pos(-250, 0, 30) * (Rotation(0, 90, 0) * create_2020_profile_extrusion(500))
    parts.append(trav_inf)

    # --------------------------------------------------------------------------
    # 5. Escuadras de fundición de aluminio en las 4 esquinas exteriores
    # --------------------------------------------------------------------------
    bracket_base = create_die_cast_bracket()
    screw_base = create_m5_screw_with_washer()

    # Escuadra Superior Izquierda (TL):
    # Apoya en Z = 480 mm sobre el travesaño superior, adosada a la columna en X = -250 mm
    esc_sup_izq = Pos(-250, 0, 480) * bracket_base
    parts.append(esc_sup_izq)
    # Tornillo Columna TL:
    parts.append(Pos(-247, 0, 489.5) * (Rotation(0, -90, 0) * screw_base))
    # Tornillo Travesaño TL:
    parts.append(Pos(-240.5, 0, 483) * (Rotation(180, 0, 0) * screw_base))

    # Escuadra Superior Derecha (TR):
    # Apoya en Z = 480 mm sobre el travesaño, adosada a la columna en X = +250 mm
    esc_sup_der = Pos(250, 0, 480) * mirror(bracket_base, about=Plane.YZ)
    parts.append(esc_sup_der)
    # Tornillo Columna TR:
    parts.append(Pos(247, 0, 489.5) * (Rotation(0, 90, 0) * screw_base))
    # NOTA: En la escuadra TR, el tornillo horizontal del travesaño está FALTANTE
    # en el prototipo físico de taller (orificio de 5.5 mm libre).

    # Escuadra Inferior Izquierda (BL):
    # Apoya bajo el travesaño en Z = 20 mm, adosada a la columna en X = -250 mm
    esc_inf_izq = Pos(-250, 0, 20) * mirror(bracket_base, about=Plane.XY)
    parts.append(esc_inf_izq)
    # Tornillo Columna BL:
    parts.append(Pos(-247, 0, 10.5) * (Rotation(0, -90, 0) * screw_base))
    # NOTA: En la escuadra BL, el tornillo horizontal del travesaño está FALTANTE
    # en el prototipo físico de taller (orificio de 5.5 mm libre).

    # Escuadra Inferior Derecha (BR):
    # Apoya bajo el travesaño en Z = 20 mm, adosada a la columna en X = +250 mm
    esc_inf_der = Pos(250, 0, 20) * mirror(mirror(bracket_base, about=Plane.YZ), about=Plane.XY)
    parts.append(esc_inf_der)
    # Tornillo Columna BR:
    parts.append(Pos(247, 0, 10.5) * (Rotation(0, 90, 0) * screw_base))
    # Tornillo Travesaño BR:
    parts.append(Pos(240.5, 0, 17) * screw_base)

    ensamblaje = Compound(children=parts)
    print(f"Ensamblaje completado con {len(parts)} piezas sólidas independientes.")
    return ensamblaje

if __name__ == "__main__":
    base_dir = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion"
    if not os.path.exists(base_dir):
        base_dir = r"C:\Users\Usuario\Desktop\universidad\clase\TFG\DESARROLLO_TFG\Fusion"

    out_step_1 = os.path.join(base_dir, "Marco_Real_2020_TFG.step")
    out_step_2 = os.path.join(base_dir, "Banco_Mecatronico_TFG.step")
    out_obj_1  = os.path.join(base_dir, "Marco_Real_2020_TFG.obj")
    out_obj_2  = os.path.join(base_dir, "Banco_Mecatronico_TFG.obj")
    out_stl_1  = os.path.join(base_dir, "Marco_Real_2020_TFG.stl")

    print("Generando B-Rep sólido de alta precisión 1:1 del marco real...")
    modelo = build_real_frame()

    print(f"Exportando STEP -> {out_step_1}...")
    export_step(modelo, out_step_1)
    export_step(modelo, out_step_2)

    print(f"Exportando OBJ -> {out_obj_1}...")
    export_obj(modelo, out_obj_1)
    export_obj(modelo, out_obj_2)

    print(f"Exportando STL -> {out_stl_1}...")
    export_stl(modelo, out_stl_1)

    print("¡Todos los modelos 1:1 han sido generados y exportados exitosamente!")
