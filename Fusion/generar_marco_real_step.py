#!/usr/bin/env python3
"""
================================================================================
GENERADOR MAESTRO 1:1 CAD DEL MARCO REAL DE TALLER (STEP + OBJ + STL)
Proyecto: Banco Mecatrónico TFG - Simulación Satelital
Autor: Antigravity AI Pair Programmer
Fecha: 28-10-2026
================================================================================
Reconstrucción fotorrealista exacta 1:1 según las imágenes oficiales de catálogo:
1. Perfilería de aluminio 2020 (Captura de pantalla 2026-10-28 191135.png):
   - Sección transversal de 20x20 mm con las 4 esquinas redondeadas (R = 1.5 mm).
   - Bocas exteriores de 6.0 mm con labios de 1.8 mm.
   - Cavidades interiores ensanchadas trapezoidales entre nervios a 45°.
   - Núcleo central con taladro lobulado de 4 orejetas (cloverleaf) de M5.
2. Escuadras de unión de 90° (Captura de pantalla 2026-10-28 191203.png):
   - Bloque de 20x20x20 mm con 2 nervios laterales de 2.5 mm de espesor.
   - Perfil de nervio con escalones horizontales/verticales de 3.5 mm y pendiente a 45°.
   - Bolsillo central vaciado de 15 mm de anchura.
   - Colisos pasantes (ranuras ovaladas) de 5.3 x 9.5 mm en base y pared vertical.
3. Tornillería DIN 912 / ISO 4762 Allen M5 con arandela ancha:
   - Tornillo cilíndrico de cabeza Allen (diámetro 8.5 mm, altura 5.0 mm, hexágono de 4 mm).
   - Arandela ancha de diámetro 11.5 mm x 1.0 mm de espesor.
   - Reflejo fiel del prototipo físico: 4 tornillos en montantes verticales y
     orificios libres (coliso vacío sin tornillo) en las escuadras con tornillo faltante.
================================================================================
"""

import os
import sys
from build123d import *

# ------------------------------------------------------------------------------
# 1. Definición de la Sección Transversal Real 2020 de Catálogo
# ------------------------------------------------------------------------------
def create_catalog_2020_sketch():
    """Genera el sketch 2D exacto del perfil 2020 de catálogo"""
    with BuildSketch() as s:
        # Cuadrado 20x20 mm con esquinas exteriores redondeadas R = 1.5 mm
        Rectangle(20.0, 20.0)
        fillet(s.vertices(), radius=1.5)

        for angle in [0, 90, 180, 270]:
            with Locations(Rotation(0, 0, angle)):
                # Boca de 6.0 mm (de x = -3.0 a +3.0) con labio de 1.8 mm
                with Locations((0, 9.1)):
                    Rectangle(6.0, 1.8, mode=Mode.SUBTRACT)
                
                # Cavidad interior ensanchada trapezoidal (entre nervios a 45°)
                with BuildLine(mode=Mode.SUBTRACT) as bl:
                    Line((-2.8, 3.6), (2.8, 3.6))
                    Line((2.8, 3.6), (5.6, 8.2))
                    Line((5.6, 8.2), (-5.6, 8.2))
                    Line((-5.6, 8.2), (-2.8, 3.6))
                make_face(mode=Mode.SUBTRACT)

        # Taladro central lobulado M5 de 4 orejetas (cloverleaf)
        Circle(radius=2.1, mode=Mode.SUBTRACT)
        for angle in [0, 90, 180, 270]:
            with Locations(Rotation(0, 0, angle)):
                with Locations((0, 2.2)):
                    Circle(radius=0.9, mode=Mode.SUBTRACT)

    return s.sketch

def create_2020_profile_extrusion(length):
    """Extruye el perfil 2020 a lo largo del eje Z"""
    with BuildPart() as p:
        insert(create_catalog_2020_sketch())
        extrude(amount=length)
    return p.part

# ------------------------------------------------------------------------------
# 2. Escuadra de 90° con Nervios y Colisos (20x20x20 mm)
# ------------------------------------------------------------------------------
def create_catalog_bracket():
    """
    Escuadra de 90° con nervios laterales y colisos (ranuras ovaladas):
    - Dimensiones envolventes: 20x20x20 mm
    - 2 nervios laterales de 2.5 mm de espesor con escalón de 3.5 mm
    - Bolsillo central de 15 mm de ancho
    - Coliso pasante de 5.3 x 9.5 mm en la base horizontal
    - Coliso pasante de 5.3 x 9.5 mm en la pared vertical
    """
    with BuildPart() as b:
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 0), (20, 0))
                Line((20, 0), (20, 3.5))
                Line((20, 3.5), (16.5, 3.5))
                Line((16.5, 3.5), (3.5, 16.5))
                Line((3.5, 16.5), (3.5, 20))
                Line((3.5, 20), (0, 20))
                Line((0, 20), (0, 0))
            make_face()
        extrude(amount=10, both=True)

        with BuildSketch(Plane.XZ) as s_pocket:
            with BuildLine() as lp:
                Line((3.0, 3.0), (21.0, 3.0))
                Line((21.0, 3.0), (21.0, 21.0))
                Line((21.0, 21.0), (3.0, 21.0))
                Line((3.0, 21.0), (3.0, 3.0))
            make_face()
        extrude(amount=7.5, both=True, mode=Mode.SUBTRACT)

        # Coliso en base horizontal (ancho 5.3 mm, longitud 9.5 mm)
        with BuildSketch(Plane.XY) as s_slot_base:
            with Locations((10.5, 0)):
                SlotCenterToCenter(center_separation=4.0, height=5.3)
        extrude(amount=10.0, both=True, mode=Mode.SUBTRACT)

        # Coliso en pared vertical (ancho 5.3 mm, longitud 9.5 mm)
        with BuildSketch(Plane.YZ) as s_slot_vert:
            with Locations((0, 10.5)):
                SlotCenterToCenter(center_separation=4.0, height=5.3, rotation=90)
        extrude(amount=10.0, both=True, mode=Mode.SUBTRACT)

    return b.part

# ------------------------------------------------------------------------------
# 3. Tornillo Allen Cilíndrico DIN 912 M5 con Arandela Ancha
# ------------------------------------------------------------------------------
def create_din912_screw():
    """
    Tornillo DIN 912 M5 con arandela ancha DIN 9021:
    - Arandela: diámetro 11.5 mm, espesor 1.0 mm
    - Cabeza cilíndrica: diámetro 8.5 mm, altura 5.0 mm
    - Alojamiento hexagonal Allen de 4.0 mm
    - Espárrago roscado M5
    """
    with BuildPart() as p:
        # Arandela ancha DIN 9021
        Cylinder(radius=5.75, height=1.0)
        # Cabeza cilíndrica DIN 912 con hexágono interior Allen
        with Locations((0, 0, 1.0)):
            Cylinder(radius=4.25, height=5.0)
            with BuildSketch(Plane.XY) as s_hex:
                with Locations((0, 0)):
                    RegularPolygon(radius=2.3094, side_count=6)
            extrude(amount=3.0, both=False, mode=Mode.SUBTRACT)
        # Espárrago roscado M5
        with Locations((0, 0, -5.0)):
            Cylinder(radius=2.45, height=10.0)
    return p.part

# ------------------------------------------------------------------------------
# 4. Construcción del Bastidor Completo 1:1
# ------------------------------------------------------------------------------
def build_real_frame():
    parts = []

    print("Construyendo perfiles 2020 con sección de catálogo lobulada...")
    # Columnas verticales (2 unidades de 500 mm en Z)
    # Columna Izquierda: X centrada en -260 mm (de X=-270 a -250), Z de 0 a 500
    col_izq = Pos(-260, 0, 0) * create_2020_profile_extrusion(500)
    parts.append(col_izq)

    # Columna Derecha: X centrada en +260 mm (de X=250 a 270), Z de 0 a 500
    col_der = Pos(260, 0, 0) * create_2020_profile_extrusion(500)
    parts.append(col_der)

    # Travesaños horizontales (2 unidades de 500 mm en X, de X=-250 a +250)
    # Travesaño Superior: Z centrado en 470 mm (de Z=460 a 480)
    trav_sup = Pos(-250, 0, 470) * (Rotation(0, 90, 0) * create_2020_profile_extrusion(500))
    parts.append(trav_sup)

    # Travesaño Inferior: Z centrado en 30 mm (de Z=20 a 40)
    trav_inf = Pos(-250, 0, 30) * (Rotation(0, 90, 0) * create_2020_profile_extrusion(500))
    parts.append(trav_inf)

    # Escuadras con colisos en las 4 esquinas exteriores
    bracket_base = create_catalog_bracket()
    screw_base = create_din912_screw()

    # 1. Escuadra Superior Izquierda (TL):
    # Apoya en Z = 480 mm sobre el travesaño, pared vertical en X = -250 mm
    esc_sup_izq = Pos(-250, 0, 480) * bracket_base
    parts.append(esc_sup_izq)
    # Tornillo Columna TL:
    parts.append(Pos(-247, 0, 490.5) * (Rotation(0, -90, 0) * screw_base))
    # Tornillo Travesaño TL:
    parts.append(Pos(-239.5, 0, 483) * (Rotation(180, 0, 0) * screw_base))

    # 2. Escuadra Superior Derecha (TR):
    # Apoya en Z = 480 mm sobre el travesaño, pared vertical en X = +250 mm
    esc_sup_der = Pos(250, 0, 480) * mirror(bracket_base, about=Plane.YZ)
    parts.append(esc_sup_der)
    # Tornillo Columna TR:
    parts.append(Pos(247, 0, 490.5) * (Rotation(0, 90, 0) * screw_base))
    # NOTA: En la escuadra TR, el tornillo horizontal del travesaño está FALTANTE
    # en el prototipo físico de taller (coliso de 5.3 x 9.5 mm abierto y libre).

    # 3. Escuadra Inferior Izquierda (BL):
    # Apoya bajo el travesaño en Z = 20 mm, pared vertical en X = -250 mm
    esc_inf_izq = Pos(-250, 0, 20) * mirror(bracket_base, about=Plane.XY)
    parts.append(esc_inf_izq)
    # Tornillo Columna BL:
    parts.append(Pos(-247, 0, 9.5) * (Rotation(0, -90, 0) * screw_base))
    # NOTA: En la escuadra BL, el tornillo horizontal del travesaño está FALTANTE
    # en el prototipo físico de taller (coliso de 5.3 x 9.5 mm abierto y libre).

    # 4. Escuadra Inferior Derecha (BR):
    # Apoya bajo el travesaño en Z = 20 mm, pared vertical en X = +250 mm
    esc_inf_der = Pos(250, 0, 20) * mirror(mirror(bracket_base, about=Plane.YZ), about=Plane.XY)
    parts.append(esc_inf_der)
    # Tornillo Columna BR:
    parts.append(Pos(247, 0, 9.5) * (Rotation(0, 90, 0) * screw_base))
    # Tornillo Travesaño BR:
    parts.append(Pos(239.5, 0, 17) * screw_base)

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
