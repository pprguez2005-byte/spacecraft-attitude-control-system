import os
from build123d import *

# ==============================================================================
# Generador Maestro 1:1 del Marco Real Medido en Taller
# Perfilería V-Slot 2020 con ranuras normalizadas en las 4 caras y
# escuadras de fundición de aluminio huecas con nervios y taladros para tornillos M5
# ==============================================================================

def create_2020_profile(length):
    """
    Crea el perfil V-Slot 2020 exacto:
    - Cuadrado exterior de 20x20 mm con chaflanes en esquinas
    - Taladro central de 4.2 mm para roscar a M5
    - 4 ranuras normalizadas V-Slot / T-Slot con labios a 45 grados y cavidad interior de 11 mm
    """
    with BuildPart() as p:
        with BuildSketch() as s:
            Rectangle(20, 20)
            fillet(s.vertices(), radius=0.8)
            # Taladro central
            Circle(radius=2.1, mode=Mode.SUBTRACT)
            # 4 Ranuras V-Slot simétricas
            for angle in [0, 90, 180, 270]:
                with Locations(Rotation(0, 0, angle)):
                    # Cavidad interna de la ranura (11.0 mm de ancho x 4.5 mm de fondo)
                    with Locations((0, 7.0)):
                        Rectangle(11.0, 4.5, mode=Mode.SUBTRACT)
                    # Boca de entrada (6.2 mm de ancho x 2.0 mm de labio)
                    with Locations((0, 9.25)):
                        Rectangle(6.2, 2.0, mode=Mode.SUBTRACT)
                    # Chaflanes a 45° del canal en V
                    with Locations((-3.1, 10.0)):
                        Triangle(a=1.5, b=1.5, C=90, rotation=180, mode=Mode.SUBTRACT)
                    with Locations((3.1, 10.0)):
                        Triangle(a=1.5, b=1.5, C=90, rotation=270, mode=Mode.SUBTRACT)
        extrude(amount=length)
    return p.part

def create_cast_corner_bracket():
    """
    Crea la escuadra de 90° de fundición de aluminio (20 x 20 x 20 mm):
    - Base y pared vertical de 3 mm de espesor
    - 2 nervios triangulares laterales de 3 mm de grosor
    - Bolsillo central vaciado de 14 mm de ancho (para alojamiento de cabeza de tornillo)
    - Taladro pasante de 5.5 mm en la base horizontal (para tornillo M5)
    - Taladro pasante de 5.5 mm en la pared vertical (para tornillo M5)
    """
    with BuildPart() as b:
        # Prisma triangular exterior (20x20 mm en XZ, de Y = -10 a +10 mm)
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 0), (20, 0))
                Line((20, 0), (0, 20))
                Line((0, 20), (0, 0))
            make_face()
        extrude(amount=10, both=True)
        
        # Vaciado del bolsillo central entre los dos nervios (deja 3 mm en cada lateral)
        with BuildSketch(Plane.XZ) as s2:
            with BuildLine() as l2:
                Line((3, 3), (17, 3))
                Line((17, 3), (3, 17))
                Line((3, 17), (3, 3))
            make_face()
        extrude(amount=7, both=True, mode=Mode.SUBTRACT)

        # Taladro pasante M5 en base horizontal (a X = 9 mm del vértice)
        with Locations((9, 0, 0)):
            Cylinder(radius=2.7, height=10, mode=Mode.SUBTRACT)
        # Taladro pasante M5 en pared vertical (a Z = 9 mm del vértice)
        with Locations((0, 0, 9)):
            Rot = Rotation(0, 90, 0)
            Rot * Cylinder(radius=2.7, height=10, mode=Mode.SUBTRACT)

    return b.part

def build_real_frame():
    parts = []

    # 1. Columna Izquierda (Longitud 500 mm en vertical Z)
    # Centrada en X = -260 mm (de X = -270 a -250 mm, Y de -10 a +10 mm)
    col_izq = Pos(-260, 0, 0) * create_2020_profile(500)
    parts.append(col_izq)

    # 2. Columna Derecha (Longitud 500 mm en vertical Z)
    # Centrada en X = +260 mm (de X = +250 a +270 mm, Y de -10 a +10 mm)
    col_der = Pos(260, 0, 0) * create_2020_profile(500)
    parts.append(col_der)

    # 3. Travesaño Superior (Longitud 500 mm en horizontal X)
    # Entre X = -250 mm y X = +250 mm (luz interior de 500 mm)
    # Centrado en Z = 470 mm (cara inferior a 460 mm, superior a 480 mm)
    # Rotado para que el eje de extrusión sea X
    trav_sup = Pos(-250, 0, 470) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_sup)

    # 4. Travesaño Inferior (Longitud 500 mm en horizontal X)
    # Entre X = -250 mm y X = +250 mm
    # Centrado en Z = 30 mm (cara inferior a 20 mm, superior a 40 mm)
    trav_inf = Pos(-250, 0, 30) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_inf)

    # 5. Las 4 Escuadras de 90° de fundición
    bracket_base = create_cast_corner_bracket()

    # Escuadra Superior Izquierda:
    # Apoya en Z = 480 mm sobre el travesaño, adosada a la columna en X = -250 mm
    # Hipotenusa baja hacia X = -230 mm
    esc_sup_izq = Pos(-250, 0, 480) * bracket_base
    parts.append(esc_sup_izq)

    # Escuadra Superior Derecha:
    # Apoya en Z = 480 mm sobre el travesaño, adosada a la columna en X = +250 mm
    # Hipotenusa baja hacia X = +230 mm
    esc_sup_der = Pos(250, 0, 480) * mirror(bracket_base, about=Plane.YZ)
    parts.append(esc_sup_der)

    # Escuadra Inferior Izquierda:
    # Apoya bajo el travesaño en Z = 20 mm, adosada a la columna en X = -250 mm
    # Hipotenusa sube hacia X = -230 mm
    esc_inf_izq = Pos(-250, 0, 20) * mirror(bracket_base, about=Plane.XY)
    parts.append(esc_inf_izq)

    # Escuadra Inferior Derecha:
    # Apoya bajo el travesaño en Z = 20 mm, adosada a la columna en X = +250 mm
    # Hipotenusa sube hacia X = +230 mm
    esc_inf_der = Pos(250, 0, 20) * (Rotation(0, 180, 0) * bracket_base)
    parts.append(esc_inf_der)

    ensamblaje = Compound(children=parts)
    return ensamblaje

if __name__ == "__main__":
    out_step_1 = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Marco_Real_2020_TFG.step"
    out_step_2 = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Banco_Mecatronico_TFG.step"
    out_obj_1  = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Marco_Real_2020_TFG.obj"
    out_obj_2  = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Banco_Mecatronico_TFG.obj"
    out_stl_1  = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Marco_Real_2020_TFG.stl"
    print("Generando B-Rep solido de alta precision del marco real 1:1...")
    modelo = build_real_frame()
    export_step(modelo, out_step_1)
    export_step(modelo, out_step_2)
    export_obj(modelo, out_obj_1)
    export_obj(modelo, out_obj_2)
    export_stl(modelo, out_stl_1)
    print("Archivos STEP, OBJ y STL exportados exitosamente!")
    print(f" -> {out_step_1}")
    print(f" -> {out_obj_1}")
    print(f" -> {out_stl_1}")

