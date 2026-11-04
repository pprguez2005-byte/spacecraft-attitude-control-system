import os
from build123d import *

# ==============================================================================
# Generador Maestro 1:1 del Marco Real Medido en Taller
# Perfilería V-Slot 2020 con ranuras reales en las 4 caras y escuadras huecas
# con nervios de fundición de aluminio y taladros para tornillos M5
# ==============================================================================

def create_2020_profile(length):
    """Crea el perfil V-Slot 2020 con ranuras normalizadas en las 4 caras y núcleo central"""
    with BuildPart() as p:
        with BuildSketch() as s:
            Rectangle(20, 20)
            fillet(s.vertices(), radius=0.8)
            # Taladro central de 4.2 mm (roscable a M5)
            Circle(radius=2.1, mode=Mode.SUBTRACT)
            # 4 Ranuras V-Slot estándar
            for angle in [0, 90, 180, 270]:
                with Locations(Rotation(0, 0, angle)):
                    # Cavidad interior de la ranura (11 mm de ancho x 4.5 mm)
                    with Locations((0, 7.0)):
                        Rectangle(11.0, 4.5, mode=Mode.SUBTRACT)
                    # Boca de entrada de la ranura (6.2 mm de ancho)
                    with Locations((0, 9.25)):
                        Rectangle(6.2, 2.0, mode=Mode.SUBTRACT)
                    # Chaflanes a 45 grados de la guía en V
                    with Locations((-3.1, 10)):
                        Triangle(a=1.5, b=1.5, C=90, rotation=180, mode=Mode.SUBTRACT)
                    with Locations((3.1, 10)):
                        Triangle(a=1.5, b=1.5, C=90, rotation=270, mode=Mode.SUBTRACT)
        extrude(amount=length)
    return p.part

def create_cast_corner_bracket():
    """
    Crea la escuadra de 90° de fundición de aluminio (20x20x20 mm):
    - 2 paredes exteriores perpendiculares de 3 mm de espesor
    - 2 nervios triangulares laterales de 3 mm
    - Bolsillo central vaciado de 14 mm de ancho
    - Taladros pasantes de 5.5 mm para tornillos M5
    """
    with BuildPart() as b:
        # Prisma triangular base (20x20 mm, profundidad 20 mm de Y = -10 a +10)
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                Line((0, 0), (20, 0))
                Line((20, 0), (0, 20))
                Line((0, 20), (0, 0))
            make_face()
        extrude(amount=20, both=True)
        
        # Vaciado del bolsillo central entre los dos nervios triangulares (ancho = 14 mm)
        with BuildSketch(Plane.XZ) as s2:
            with BuildLine() as l2:
                Line((3, 3), (17, 3))
                Line((17, 3), (3, 17))
                Line((3, 17), (3, 3))
            make_face()
        extrude(amount=7, both=True, mode=Mode.SUBTRACT)

        # Taladro en base horizontal (X = 9 mm)
        with Locations((9, 0, 0)):
            Cylinder(radius=2.7, height=10, mode=Mode.SUBTRACT)
        # Taladro en pared vertical (Z = 9 mm)
        with Locations((0, 0, 9)):
            Rot = Rotation(0, 90, 0)
            Rot * Cylinder(radius=2.7, height=10, mode=Mode.SUBTRACT)

    return b.part

def build_full_frame():
    parts = []

    # 1. Columna Izquierda (Longitud 500 mm en vertical Z)
    # Centrada en X = -260 mm (de X = -270 a -250 mm)
    col_izq = Pos(-260, 0, 0) * create_2020_profile(500)
    parts.append(col_izq)

    # 2. Columna Derecha (Longitud 500 mm en vertical Z)
    # Centrada en X = +260 mm (de X = +250 a +270 mm)
    col_der = Pos(260, 0, 0) * create_2020_profile(500)
    parts.append(col_der)

    # 3. Travesaño Superior (Longitud 500 mm en horizontal X)
    # De X = -250 mm a X = +250 mm
    # Centrado en Z = 470 mm (cara inferior a 460 mm, superior a 480 mm)
    trav_sup = Pos(-250, 0, 470) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_sup)

    # 4. Travesaño Inferior (Longitud 500 mm en horizontal X)
    # De X = -250 mm a X = +250 mm
    # Centrado en Z = 30 mm (cara inferior a 20 mm, superior a 40 mm)
    trav_inf = Pos(-250, 0, 30) * (Rotation(0, 90, 0) * create_2020_profile(500))
    parts.append(trav_inf)

    # --------------------------------------------------------------------------
    # 5. Las 4 Escuadras de 90° de fundición
    # --------------------------------------------------------------------------
    bracket_base = create_cast_corner_bracket()

    # Escuadra Superior Izquierda:
    # Reste sobre el travesaño en Z = 480 mm, adosada a la columna en X = -250 mm
    # La pared vertical está en X = -250 mm, la base en Z = 480 mm
    # La hipotenusa baja hacia X = -230 mm
    esc_sup_izq = Pos(-250, 0, 480) * bracket_base
    parts.append(esc_sup_izq)

    # Escuadra Superior Derecha:
    # La pared vertical está en X = 250 mm, la base en Z = 480 mm
    # La hipotenusa baja hacia X = 230 mm (espejo en X)
    esc_sup_der = Pos(250, 0, 480) * (Rotation(0, 0, 180) * (Rotation(0, 90, 0) * bracket_base))
    # Vamos a verificar rotaciones rotando en plano XZ
    # X positivo hacia la izquierda: escala X por -1 o rotación de 180 en Z y luego...
    # Más simple: rotar en Y 90 o reflejar
    return parts

if __name__ == "__main__":
    p = build_full_frame()
    print(f"Piezas creadas con exito: {len(p)}")
