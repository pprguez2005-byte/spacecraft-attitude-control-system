# Generador de archivo OBJ 3D para el Bastidor Real de las Fotos (1:1)
# Perfiles 2020 (540 x 500 mm) con 4 escuadras de fundicion de aluminio de 90 grados

def export_frame_obj(filename):
    vertices = []
    faces = []

    def add_box(name, x0, y0, z0, dx, dy, dz):
        start_v = len(vertices) + 1
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

    def add_wedge(name, x0, y0, z0, dx, dy, dz):
        start_v = len(vertices) + 1
        # Triangular prism
        # Base: (x0, y0, z0) to (x0+dx, y0, z0)
        # Vertical: (x0, y0, z0+dz)
        # Depth: y0 + dy
        v_coords = [
            (x0, y0, z0),           # 0
            (x0 + dx, y0, z0),      # 1
            (x0, y0, z0 + dz),      # 2
            (x0, y0 + dy, z0),      # 3
            (x0 + dx, y0 + dy, z0), # 4
            (x0, y0 + dy, z0 + dz)  # 5
        ]
        vertices.extend(v_coords)
        f = [
            # Front triangle
            (start_v + 0, start_v + 1, start_v + 2),
            # Back triangle
            (start_v + 3, start_v + 5, start_v + 4),
            # Bottom quad
            (start_v + 0, start_v + 3, start_v + 4),
            (start_v + 0, start_v + 4, start_v + 1),
            # Vertical quad
            (start_v + 0, start_v + 2, start_v + 5),
            (start_v + 0, start_v + 5, start_v + 3),
            # Slanted quad
            (start_v + 1, start_v + 4, start_v + 5),
            (start_v + 1, start_v + 5, start_v + 2)
        ]
        faces.append((name, f))

    # BASTIDOR EXACTO DE LAS FOTOS (540 mm exterior, 500 mm interior, 500 mm altura)
    # Centrado en X = 0
    # Columna Izquierda: 20x20x500 mm en X = -270 a -250 mm
    add_box("Columna_Izquierda_2020_500mm", -270, -10, 0, 20, 20, 500)
    # Columna Derecha: 20x20x500 mm en X = 250 a 270 mm
    add_box("Columna_Derecha_2020_500mm", 250, -10, 0, 20, 20, 500)
    # Travesaño Superior: 500 mm de largo, de X = -250 a 250 mm, Z = 460 a 480 mm
    add_box("Travesano_Superior_2020_500mm", -250, -10, 460, 500, 20, 20)
    # Travesaño Inferior: 500 mm de largo, de X = -250 a 250 mm, Z = 20 a 40 mm
    add_box("Travesano_Inferior_2020_500mm", -250, -10, 20, 500, 20, 20)

    # 4 Escuadras de 90 grados
    # Superior Izquierda (sobre travesaño superior)
    add_wedge("Escuadra_Superior_Izquierda", -250, -9, 480, 20, 18, 20)
    # Superior Derecha
    add_wedge("Escuadra_Superior_Derecha", 250, -9, 480, -20, 18, 20)
    # Inferior Izquierda (debajo travesaño inferior)
    add_wedge("Escuadra_Inferior_Izquierda", -250, -9, 20, 20, 18, -20)
    # Inferior Derecha
    add_wedge("Escuadra_Inferior_Derecha", 250, -9, 20, -20, 18, -20)

    with open(filename, 'w', encoding='utf-8') as out:
        out.write("# Bastidor Real Medido en Taller - Perfiles 2020 (540 x 500 mm)\n")
        out.write("# Modelo 1:1 exacto de las fotos para Autodesk Fusion 360\n\n")
        for v in vertices:
            out.write(f"v {v[0]:.2f} {v[1]:.2f} {v[2]:.2f}\n")
        
        for name, flist in faces:
            out.write(f"\no {name}\n")
            out.write(f"g {name}\n")
            for tri in flist:
                out.write(f"f {tri[0]} {tri[1]} {tri[2]}\n")

if __name__ == "__main__":
    out_obj = r"C:\Users\Usuario\Desktop\universidad\clase\TFG\DESARROLLO_TFG\Fusion\Banco_Mecatronico_TFG.obj"
    export_frame_obj(out_obj)
    export_frame_obj(r"C:\Users\Usuario\Desktop\universidad\clase\TFG\DESARROLLO_TFG\Fusion\Marco_Real_2020_TFG.obj")
    print("Exportacion exitosa: Marco_Real_2020_TFG.obj")
