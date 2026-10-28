# Generador de archivo OBJ 3D para el Banco Mecatrónico TFG
# Dimensiones en milímetros reales (1:1)

def export_obj(filename):
    vertices = []
    faces = []

    def add_box(name, x0, y0, z0, dx, dy, dz):
        start_v = len(vertices) + 1
        # 8 vertices of a box
        # 0: x0, y0, z0
        # 1: x0+dx, y0, z0
        # 2: x0+dx, y0+dy, z0
        # 3: x0, y0+dy, z0
        # 4: x0, y0, z0+dz
        # 5: x0+dx, y0, z0+dz
        # 6: x0+dx, y0+dy, z0+dz
        # 7: x0, y0+dy, z0+dz
        v_coords = [
            (x0, y0, z0),
            (x0 + dx, y0, z0),
            (x0 + dx, y0 + dy, z0),
            (x0, y0 + dy, z0),
            (x0, y0, z0 + dz),
            (x0 + dx, y0, z0 + dz),
            (x0 + dx, y0 + dy, z0 + dz),
            (x0, y0 + dy, z0 + dz)
        ]
        vertices.extend(v_coords)
        
        # 6 quad faces (12 triangles)
        # bottom: 0, 1, 2, 3
        # top: 4, 7, 6, 5
        # front: 0, 4, 5, 1
        # back: 3, 2, 6, 7
        # left: 0, 3, 7, 4
        # right: 1, 5, 6, 2
        f = [
            # Front
            (start_v + 0, start_v + 1, start_v + 5),
            (start_v + 0, start_v + 5, start_v + 4),
            # Back
            (start_v + 3, start_v + 6, start_v + 2),
            (start_v + 3, start_v + 7, start_v + 6),
            # Top
            (start_v + 4, start_v + 5, start_v + 6),
            (start_v + 4, start_v + 6, start_v + 7),
            # Bottom
            (start_v + 0, start_v + 2, start_v + 1),
            (start_v + 0, start_v + 3, start_v + 2),
            # Left
            (start_v + 0, start_v + 4, start_v + 7),
            (start_v + 0, start_v + 7, start_v + 3),
            # Right
            (start_v + 1, start_v + 2, start_v + 6),
            (start_v + 1, start_v + 6, start_v + 5)
        ]
        faces.append((name, f))

    # 1. BASTIDOR BASE (540 x 500 mm)
    # Columna izquierda: 20x500x20 mm
    add_box("Columna_Izquierda_2020_500mm", 0, 0, 0, 20, 500, 20)
    # Columna derecha: 20x500x20 mm en X = 520
    add_box("Columna_Derecha_2020_500mm", 520, 0, 0, 20, 500, 20)
    # Travesaño inferior: 540x20x20 mm en Y = -20
    add_box("Travesano_Inferior_540mm", 0, -20, 0, 540, 20, 20)
    # Travesaño superior: 540x20x20 mm en Y = 500
    add_box("Travesano_Superior_540mm", 0, 500, 0, 540, 20, 20)

    # 2. BATERÍA SUPERIOR DE 5 PERFILES (600 mm en Z)
    # Espaciado entre centros = 120 mm
    for i in range(5):
        x_c = 30 + (i * 120) # 30, 150, 270, 390, 510
        add_box(f"Bateria_Longitudinal_Perfil_{i+1}_600mm", x_c - 10, 520, 0, 20, 20, 600)

    # 3. EJE TRANSVERSAL GUÍA GT2 (540 mm en X a Z = 300 mm)
    add_box("Perfil_Transversal_Guia_GT2_540mm", 0, 540, 290, 540, 20, 20)

    # 4. SOPORTE Y MOTOR NEMA 17 (Extremo derecho)
    add_box("Soporte_Motor_NEMA17", 498, 540, 279, 42, 42, 42)

    # 5. SOPORTE TENSOR IDLER GT2 (Extremo izquierdo)
    add_box("Soporte_Tensor_Idler_GT2", 0, 540, 285, 30, 30, 30)

    # 6. CARRO MÓVIL V-WHEEL CON JOYSTICK (Centrado en X = 270 mm)
    add_box("Carro_Movil_Gantry_Plate", 235, 530, 280, 70, 40, 40)
    add_box("Modulo_Joystick_Sensor", 255, 510, 290, 30, 20, 20)

    with open(filename, 'w', encoding='utf-8') as out:
        out.write("# Banco Mecatronico TFG - Microgravedad Simulada\n")
        out.write("# Exportado directamente para Autodesk Fusion 360\n\n")
        for v in vertices:
            out.write(f"v {v[0]:.2f} {v[1]:.2f} {v[2]:.2f}\n")
        
        for name, flist in faces:
            out.write(f"\no {name}\n")
            out.write(f"g {name}\n")
            for tri in flist:
                out.write(f"f {tri[0]} {tri[1]} {tri[2]}\n")

if __name__ == "__main__":
    export_obj(r"C:\Users\Usuario\Desktop\universidad\clase\TFG\DESARROLLO_TFG\Fusion\Banco_Mecatronico_TFG.obj")
    print("Exportacion exitosa: Banco_Mecatronico_TFG.obj")
