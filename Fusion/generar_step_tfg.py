import os
from build123d import *

# ==============================================================================
# Generador Oficial STEP (B-Rep Sólido Nativo OpenCASCADE)
# Proyecto: TFG - Banco Mecatrónico de Microgravedad Simulada
# ==============================================================================

def create_model():
    parts = []

    # 1. BASTIDOR BASE FRONTAL (V-SLOT 2020: 540 x 500 mm)
    # Columna Izquierda (20 x 20 x 500 mm)
    col_izq = Box(20, 500, 20, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(col_izq)

    # Columna Derecha (20 x 20 x 500 mm a X = 520 mm)
    col_der = Pos(520, 0, 0) * Box(20, 500, 20, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(col_der)

    # Travesaño Inferior Frontal (540 x 20 x 20 mm a Y = -20 mm)
    trav_inf = Pos(0, -20, 0) * Box(540, 20, 20, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(trav_inf)

    # Travesaño Superior Frontal (540 x 20 x 20 mm a Y = 500 mm)
    trav_sup = Pos(0, 500, 0) * Box(540, 20, 20, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(trav_sup)

    # 2. BATERÍA SUPERIOR DE 5 PERFILES LONGITUDINALES (600 mm de avance en Z)
    # Espaciado entre centros = 120 mm (480 mm / 4 vanos en el ancho útil)
    for i in range(5):
        x_c = 30 + (i * 120)  # X = 30, 150, 270, 390, 510 mm
        p_long = Pos(x_c - 10, 520, 0) * Box(20, 20, 600, align=(Align.MIN, Align.MIN, Align.MIN))
        parts.append(p_long)

    # 3. EJE TRANSVERSAL GUÍA GT2 (540 mm a Z = 300 mm)
    eje_trans = Pos(0, 540, 290) * Box(540, 20, 20, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(eje_trans)

    # 4. SOPORTE Y MOTOR PASO A PASO NEMA 17 (Extremo derecho del eje transversal)
    motor = Pos(498, 540, 279) * Box(42, 42, 42, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(motor)

    # 5. SOPORTE TENSOR DE POLEA LOCA IDLER GT2 (Extremo izquierdo)
    tensor = Pos(0, 540, 285) * Box(30, 30, 30, align=(Align.MIN, Align.MIN, Align.MIN))
    parts.append(tensor)

    # 6. CARRO MÓVIL V-WHEEL CON SOPORTE DE JOYSTICK Y OJAL PARA HILO CUBESAT
    # Placa gantry móvil centrada en X = 270 mm
    with BuildPart() as carro_builder:
        with Locations((270, 550, 300)):
            Box(70, 40, 12)
            # Taladro pasante central de 4.5 mm para el hilo de suspensión
            Cylinder(radius=2.25, height=20, mode=Mode.SUBTRACT)
        # Bloque de soporte del sensor joystick COTS
        with Locations((270, 530, 300)):
            Box(30, 20, 15)
            Cylinder(radius=2.5, height=25, mode=Mode.SUBTRACT)

    parts.append(carro_builder.part)

    # Crear ensamblaje compuesto
    ensamblaje = Compound(children=parts)
    return ensamblaje

if __name__ == "__main__":
    out_path = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Banco_Mecatronico_TFG.step"
    print(f"Generando solido B-Rep STEP en: {out_path}...")
    modelo = create_model()
    export_step(modelo, out_path)
    print("STEP exportado exitosamente!")
