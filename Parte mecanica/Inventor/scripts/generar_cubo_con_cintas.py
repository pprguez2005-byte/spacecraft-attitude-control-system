"""
================================================================================
SCRIPT MAESTRO DE GENERACIÓN DEL BANCO MECATRÓNICO TFG EN AUTODESK INVENTOR 2027
Transmisión cinemática según croquis del usuario (04-11-2026):
- Cinta transportadora en bucle cerrado con DIENTES INTERNOS. Aspecto: Anodizado - Negro.
- Cabezal motriz con DOS ENGRANAJES RECTOS 1:1 (Z=20, m=1.0) engranados en el interior. Aspecto: Oro.
- Motor NEMA 17 acoplado al Engranaje 1. Aspecto: Aluminio - Pulido (Metal).
- Eje transversal de distribución acoplado al Engranaje 2 cruzando hacia la cinta opuesta.
- Batería de 4 perfiles 2020 apoyados sobre las cintas dentadas.
- 16 escuadras de fundición con sus 32 tornillos Allen DIN 912 M5 enrasados.
- Exportación automática: STEP universal (.step) y Paquete completo nativo (.zip).
================================================================================
"""

import sys
import os
import math
import zipfile

INVENTOR_BINDINGS = r"C:\Program Files\Autodesk\Inventor 2027\Bin\PythonBindings"
if INVENTOR_BINDINGS not in sys.path:
    sys.path.insert(0, INVENTOR_BINDINGS)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from inventor_core import InventorManager, mm, pt2d, matrix_transform, inv

INVENTOR_ROOT = os.path.dirname(SCRIPT_DIR)
PIEZAS_DIR = os.path.join(INVENTOR_ROOT, "piezas")
ENSAMBLAJES_DIR = os.path.join(INVENTOR_ROOT, "ensamblajes")
os.makedirs(PIEZAS_DIR, exist_ok=True)
os.makedirs(ENSAMBLAJES_DIR, exist_ok=True)

PART_P500     = os.path.join(PIEZAS_DIR, "Perfil_2020_L500.ipt")
PART_P540     = os.path.join(PIEZAS_DIR, "Perfil_2020_L540.ipt")
PART_P460     = os.path.join(PIEZAS_DIR, "Perfil_2020_L460.ipt")
PART_BRACKET  = os.path.join(PIEZAS_DIR, "Escuadra_90_Fundicion_2020.ipt")
PART_SCREW    = os.path.join(PIEZAS_DIR, "Tornillo_M5x8_DIN912.ipt")
PART_BELT     = os.path.join(PIEZAS_DIR, "Cinta_Transportadora_20mm_L500.ipt")
PART_MOTOR    = os.path.join(PIEZAS_DIR, "Motor_NEMA17.ipt")
PART_GEAR     = os.path.join(PIEZAS_DIR, "Engranaje_Recto_1a1_m1_Z20.ipt")
PART_PULLEY   = os.path.join(PIEZAS_DIR, "Polea_GT2_20T.ipt")
PART_SHAFT    = os.path.join(PIEZAS_DIR, "Eje_Distribucion_5mm_L520.ipt")


def aplicar_aspecto_a_cuerpos(app: inv.Application, doc, nombre_aspecto: str):
    """Aplica un aspecto de la librería 'Autodesk Biblioteca de aspecto' a todos los cuerpos sólidos."""
    try:
        lib_app = None
        for lib in app.AssetLibraries:
            if "aspecto" in lib.DisplayName.lower():
                lib_app = lib
                break
        if not lib_app:
            for lib in app.AssetLibraries:
                if "autodesk" in lib.DisplayName.lower():
                    lib_app = lib
                    break
        if not lib_app:
            print(f"  -> Advertencia: No se encontró librería de aspectos para '{nombre_aspecto}'.")
            return

        local_asset = None
        for a in doc.AppearanceAssets:
            if a.DisplayName.lower() == nombre_aspecto.lower():
                local_asset = a
                break

        if not local_asset:
            for a in lib_app.AppearanceAssets:
                if a.DisplayName.lower() == nombre_aspecto.lower():
                    local_asset = a.CopyTo(doc)
                    break

        if local_asset:
            comp = doc.ComponentDefinition
            for i in range(1, comp.SurfaceBodies.Count + 1):
                comp.SurfaceBodies.Item(i).Appearance = local_asset
            print(f"  -> Aspecto '{nombre_aspecto}' asignado a {comp.SurfaceBodies.Count} cuerpo(s).")
        else:
            print(f"  -> Advertencia: Aspecto '{nombre_aspecto}' no localizado en la librería.")
    except Exception as e:
        print(f"  -> Excepción aplicando aspecto '{nombre_aspecto}':", e)


def generar_engranaje_recto_real(app: inv.Application):
    """Genera el engranaje recto con 20 dientes reales y aspecto metálico oro ('Oro')."""
    print("[Piezas] Generando Engranaje_Recto_1a1_m1_Z20.ipt (Metal Oro)...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    comp = doc.ComponentDefinition
    sk = comp.Sketches.Add(comp.WorkPlanes.Item(3))
    lines = sk.SketchLines

    z = 20
    m = 1.0
    r_a = 11.0
    r_f = 8.75
    pitch_ang = 360.0 / z
    half_tip = 3.0
    half_root = 6.0

    pts = []
    for k in range(z):
        ang_mid = k * pitch_ang
        a0 = math.radians(ang_mid - half_root)
        a1 = math.radians(ang_mid - half_tip)
        a2 = math.radians(ang_mid + half_tip)
        a3 = math.radians(ang_mid + half_root)
        pts.append((r_f * math.cos(a0), r_f * math.sin(a0)))
        pts.append((r_a * math.cos(a1), r_a * math.sin(a1)))
        pts.append((r_a * math.cos(a2), r_a * math.sin(a2)))
        pts.append((r_f * math.cos(a3), r_f * math.sin(a3)))

    n = len(pts)
    for i in range(n):
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        lines.AddByTwoPoints(pt2d(app, p_curr[0], p_curr[1]), pt2d(app, p_next[0], p_next[1]))

    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5))
    prof = sk.Profiles.AddForSolid()
    comp.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof, mm(7.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    aplicar_aspecto_a_cuerpos(app, doc, "Oro")
    doc.SaveAs(PART_GEAR, False)
    doc.Close(True)
    print("  -> Engranaje guardado exitosamente con acabado Oro.")


def generar_cinta_con_dientes(app: inv.Application):
    """Genera la cinta transportadora hueca con dientes internos y aspecto metal negro ('Anodizado - Negro')."""
    print("[Piezas] Generando Cinta_Transportadora_20mm_L500.ipt (Metal Negro)...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    comp = doc.ComponentDefinition

    L = 220.0
    R_out = 14.0
    R_in = 11.5
    w_belt = 12.0

    # 1. Bucle exterior
    sk_out = comp.Sketches.Add(comp.WorkPlanes.Item(3))
    lo = sk_out.SketchLines
    ao = sk_out.SketchArcs
    l1 = lo.AddByTwoPoints(pt2d(app, -L, R_out), pt2d(app, L, R_out))
    a1 = ao.AddByCenterStartEndPoint(pt2d(app, L, 0), l1.EndSketchPoint, pt2d(app, L, -R_out), False)
    l2 = lo.AddByTwoPoints(a1.EndSketchPoint, pt2d(app, -L, -R_out))
    a2 = ao.AddByCenterStartEndPoint(pt2d(app, -L, 0), l2.EndSketchPoint, l1.StartSketchPoint, False)
    prof_out = sk_out.Profiles.AddForSolid()
    comp.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_out, mm(w_belt), inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    # 2. Vaciado interior
    sk_in = comp.Sketches.Add(comp.WorkPlanes.Item(3))
    li = sk_in.SketchLines
    ai = sk_in.SketchArcs
    l3 = li.AddByTwoPoints(pt2d(app, -L, R_in), pt2d(app, L, R_in))
    a3 = ai.AddByCenterStartEndPoint(pt2d(app, L, 0), l3.EndSketchPoint, pt2d(app, L, -R_in), False)
    l4 = li.AddByTwoPoints(a3.EndSketchPoint, pt2d(app, -L, -R_in))
    a4 = ai.AddByCenterStartEndPoint(pt2d(app, -L, 0), l4.EndSketchPoint, l3.StartSketchPoint, False)
    prof_in = sk_in.Profiles.AddForSolid()
    comp.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_in, mm(w_belt), inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kCutOperation
    )

    # 3. Dientes internos
    sk_teeth = comp.Sketches.Add(comp.WorkPlanes.Item(3))
    lt = sk_teeth.SketchLines
    pitch = 16.0
    w_t = 5.0
    h_t = 1.8
    n_teeth = int((2 * L - 40.0) / pitch)
    for i in range(n_teeth):
        x = (-L + 20.0) + i * pitch
        lt.AddAsTwoPointRectangle(pt2d(app, x - w_t/2, -R_in), pt2d(app, x + w_t/2, -R_in + h_t))
        lt.AddAsTwoPointRectangle(pt2d(app, x - w_t/2, R_in - h_t), pt2d(app, x + w_t/2, R_in))

    prof_teeth = sk_teeth.Profiles.AddForSolid(True)
    comp.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_teeth, mm(w_belt), inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kJoinOperation
    )

    aplicar_aspecto_a_cuerpos(app, doc, "Anodizado - Negro")
    doc.SaveAs(PART_BELT, False)
    doc.Close(True)
    print("  -> Cinta con dientes internos guardada exitosamente con acabado Anodizado Negro.")


def actualizar_motor_metal(app: inv.Application):
    """Genera o actualiza el motor NEMA 17 con aspecto metálico ('Aluminio - Pulido')."""
    print("[Piezas] Actualizando Motor_NEMA17.ipt (Metal / Aluminio Pulido)...")
    is_new = False
    if not os.path.exists(PART_MOTOR):
        is_new = True
        doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
        comp = doc.ComponentDefinition
        sk_body = comp.Sketches.Add(comp.WorkPlanes.Item(3))
        sk_body.SketchLines.AddAsTwoPointRectangle(pt2d(app, -21.0, -21.0), pt2d(app, 21.0, 21.0))
        prof_body = sk_body.Profiles.AddForSolid()
        comp.Features.ExtrudeFeatures.AddByDistanceExtent(
            prof_body, mm(40.0), inv.PartFeatureExtentDirectionEnum.kNegativeExtentDirection,
            inv.PartFeatureOperationEnum.kNewBodyOperation
        )
        sk_pilot = comp.Sketches.Add(comp.WorkPlanes.Item(3))
        sk_pilot.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(11.0))
        prof_pilot = sk_pilot.Profiles.AddForSolid()
        comp.Features.ExtrudeFeatures.AddByDistanceExtent(
            prof_pilot, mm(2.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
            inv.PartFeatureOperationEnum.kJoinOperation
        )
        sk_shaft = comp.Sketches.Add(comp.WorkPlanes.Item(3))
        sk_shaft.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5))
        prof_shaft = sk_shaft.Profiles.AddForSolid()
        comp.Features.ExtrudeFeatures.AddByDistanceExtent(
            prof_shaft, mm(24.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
            inv.PartFeatureOperationEnum.kJoinOperation
        )
    else:
        doc = app.Documents.Open(PART_MOTOR, False)

    aplicar_aspecto_a_cuerpos(app, doc, "Aluminio - Pulido")
    if is_new:
        doc.SaveAs(PART_MOTOR, False)
    else:
        doc.Save()
    doc.Close(True)
    print("  -> Motor NEMA 17 guardado con acabado Aluminio Pulido.")


def agregar_escuadra_con_dos_tornillos(app: inv.Application, occs: inv.ComponentOccurrences, m_bracket: inv.Matrix):
    """Inserta una escuadra de 90° con sus dos tornillos Allen M5 enrasados."""
    occs.Add(PART_BRACKET, m_bracket)

    # Tornillo 1 (Cara horizontal, coliso Z = 0)
    m_s1_local = matrix_transform(app, x_mm=10.5, y_mm=0.0, z_mm=3.0)
    m_s1_local.TransformBy(m_bracket)
    occs.Add(PART_SCREW, m_s1_local)

    # Tornillo 2 (Cara vertical, coliso X = 0)
    m_s2_local = matrix_transform(app, x_mm=3.0, y_mm=0.0, z_mm=10.5, rot_y_deg=90.0)
    m_s2_local.TransformBy(m_bracket)
    occs.Add(PART_SCREW, m_s2_local)


def empaquetar_proyecto_zip():
    """Empaqueta el proyecto completo de Inventor en un archivo ZIP portable para compartir."""
    zip_path = os.path.join(INVENTOR_ROOT, "Banco_Mecatronico_Inventor_Completo.zip")
    print(f"\n[Empaquetado] Creando archivo ZIP portable: {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Añadir ipj
        ipj_path = os.path.join(INVENTOR_ROOT, "Banco_Mecatronico_TFG.ipj")
        if os.path.exists(ipj_path):
            zipf.write(ipj_path, arcname=os.path.basename(ipj_path))
        
        # Añadir piezas .ipt
        for root, dirs, files in os.walk(PIEZAS_DIR):
            if "OldVersions" in root:
                continue
            for f in files:
                if f.endswith(".ipt"):
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, INVENTOR_ROOT)
                    zipf.write(full_p, arcname=rel_p)

        # Añadir ensamblajes .iam y .step
        for root, dirs, files in os.walk(ENSAMBLAJES_DIR):
            if "OldVersions" in root:
                continue
            for f in files:
                if f.endswith(".iam") or f.endswith(".step"):
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, INVENTOR_ROOT)
                    zipf.write(full_p, arcname=rel_p)

    tam_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  -> ZIP creado exitosamente: {zip_path} ({tam_mb:.2f} MB)")
    return zip_path


def construir_ensamblaje():
    app = InventorManager.get_app()
    print("================================================================================")
    print("ENSAMBLANDO BANCO MECATRÓNICO CÚBICO EN AUTODESK INVENTOR 2027")
    print("================================================================================")

    # 1. Regenerar piezas críticas con los aspectos y acabados especificados
    generar_engranaje_recto_real(app)
    generar_cinta_con_dientes(app)
    actualizar_motor_metal(app)

    # 2. Crear documento de ensamblaje
    doc = app.Documents.Add(inv.DocumentTypeEnum.kAssemblyDocumentObject, CreateVisible=False)
    comp_def = doc.ComponentDefinition
    occs = comp_def.Occurrences

    # --------------------------------------------------------------------------
    # A. BASTIDOR CÚBICO 50 x 54 cm (H = 50 cm) EN PERFILES 2020 DE CATÁLOGO
    # --------------------------------------------------------------------------
    print("[1/4] Ensamblando columnas y travesaños del cubo...")
    # 4 Columnas verticales en Y (de 0 a 500 mm)
    occs.Add(PART_P500, matrix_transform(app, x_mm=-260, y_mm=0, z_mm=-240, rot_x_deg=-90)).Grounded = True
    occs.Add(PART_P500, matrix_transform(app, x_mm=260, y_mm=0, z_mm=-240, rot_x_deg=-90))
    occs.Add(PART_P500, matrix_transform(app, x_mm=-260, y_mm=0, z_mm=240, rot_x_deg=-90))
    occs.Add(PART_P500, matrix_transform(app, x_mm=260, y_mm=0, z_mm=240, rot_x_deg=-90))

    # 4 Travesaños inferiores de la base (centro Y = 30 mm)
    occs.Add(PART_P500, matrix_transform(app, x_mm=-250, y_mm=30, z_mm=-240, rot_y_deg=90))
    occs.Add(PART_P500, matrix_transform(app, x_mm=-250, y_mm=30, z_mm=240, rot_y_deg=90))
    occs.Add(PART_P460, matrix_transform(app, x_mm=-260, y_mm=30, z_mm=-230))
    occs.Add(PART_P460, matrix_transform(app, x_mm=260, y_mm=30, z_mm=-230))

    # 4 Travesaños superiores de corona (centro Y = 470 mm, cara superior a Y = 480 mm)
    occs.Add(PART_P500, matrix_transform(app, x_mm=-250, y_mm=470, z_mm=-240, rot_y_deg=90))
    occs.Add(PART_P500, matrix_transform(app, x_mm=-250, y_mm=470, z_mm=240, rot_y_deg=90))
    occs.Add(PART_P460, matrix_transform(app, x_mm=-260, y_mm=470, z_mm=-230))
    occs.Add(PART_P460, matrix_transform(app, x_mm=260, y_mm=470, z_mm=-230))

    # --------------------------------------------------------------------------
    # B. 16 ESCUADRAS DE 90° CON 32 TORNILLOS ALLEN M5 ENRASADOS
    # --------------------------------------------------------------------------
    print("[2/4] Posicionando 16 escuadras de 90° con 32 tornillos M5...")
    # Frontal
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-250, y_mm=480, z_mm=-240, rot_x_deg=-90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=250, y_mm=480, z_mm=-240, rot_x_deg=-90, rot_z_deg=180))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-250, y_mm=20, z_mm=-240, rot_x_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=250, y_mm=20, z_mm=-240, rot_x_deg=90, rot_z_deg=180))
    # Trasero
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-250, y_mm=480, z_mm=240, rot_x_deg=-90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=250, y_mm=480, z_mm=240, rot_x_deg=-90, rot_z_deg=180))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-250, y_mm=20, z_mm=240, rot_x_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=250, y_mm=20, z_mm=240, rot_x_deg=90, rot_z_deg=180))
    # Laterales (vigas en Z)
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-260, y_mm=480, z_mm=-230, rot_x_deg=-90, rot_z_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-260, y_mm=480, z_mm=230, rot_x_deg=-90, rot_z_deg=-90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-260, y_mm=20, z_mm=-230, rot_x_deg=90, rot_z_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=-260, y_mm=20, z_mm=230, rot_x_deg=90, rot_z_deg=-90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=260, y_mm=480, z_mm=-230, rot_x_deg=-90, rot_z_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=260, y_mm=480, z_mm=230, rot_x_deg=-90, rot_z_deg=-90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=260, y_mm=20, z_mm=-230, rot_x_deg=90, rot_z_deg=90))
    agregar_escuadra_con_dos_tornillos(app, occs, matrix_transform(app, x_mm=260, y_mm=20, z_mm=230, rot_x_deg=90, rot_z_deg=-90))

    # --------------------------------------------------------------------------
    # C. CINEMÁTICA SUPERIOR SEGÚN CROQUIS: CINTAS, ENGRANAJES 1:1, MOTOR Y EJE
    # --------------------------------------------------------------------------
    print("[3/4] Montando cinemática superior según croquis...")
    y_belt = 494.0

    # 1. Cinta Lateral Izquierda (centrada en X = -260 mm)
    m_belt_l = matrix_transform(app, x_mm=-260, y_mm=y_belt, z_mm=0, rot_y_deg=-90)
    occs.Add(PART_BELT, m_belt_l)

    # 2. Cinta Lateral Derecha (centrada en X = +260 mm)
    m_belt_r = matrix_transform(app, x_mm=260, y_mm=y_belt, z_mm=0, rot_y_deg=-90)
    occs.Add(PART_BELT, m_belt_r)

    # 3. Engranaje 1 (Cabezal frontal, conducido por motor M) en el interior del bucle
    m_gear1 = matrix_transform(app, x_mm=-260, y_mm=y_belt, z_mm=-220, rot_y_deg=90)
    occs.Add(PART_GEAR, m_gear1)

    # 4. Engranaje 2 (Engranado con Engranaje 1 a distancia a = 20.0 mm en Z)
    m_gear2 = matrix_transform(app, x_mm=-260, y_mm=y_belt, z_mm=-200, rot_y_deg=90)
    occs.Add(PART_GEAR, m_gear2)

    # 5. Motor NEMA 17 acoplado al Engranaje 1 en la cara exterior (X = -282 mm)
    m_motor = matrix_transform(app, x_mm=-282, y_mm=y_belt, z_mm=-220, rot_y_deg=90)
    occs.Add(PART_MOTOR, m_motor)

    # 6. Eje de Distribución transversal (5 mm x 520 mm) acoplado al Engranaje 2
    m_shaft = matrix_transform(app, x_mm=0, y_mm=y_belt, z_mm=-200, rot_y_deg=90)
    occs.Add(PART_SHAFT, m_shaft)

    # 7. Engranaje conducido en la cinta derecha (X = +260 mm, Z = -200 mm)
    m_gear_r = matrix_transform(app, x_mm=260, y_mm=y_belt, z_mm=-200, rot_y_deg=90)
    occs.Add(PART_GEAR, m_gear_r)

    # 8. Poleas locas de retorno en el extremo trasero (Z = +220 mm)
    occs.Add(PART_PULLEY, matrix_transform(app, x_mm=-260, y_mm=y_belt, z_mm=220, rot_y_deg=90))
    occs.Add(PART_PULLEY, matrix_transform(app, x_mm=260, y_mm=y_belt, z_mm=220, rot_y_deg=90))

    # --------------------------------------------------------------------------
    # D. BATERÍA DE 4 PERFILES 2020 APOYADOS SOBRE LAS CINTAS DENTADAS
    # --------------------------------------------------------------------------
    print("[4/4] Colocando batería de 4 perfiles apoyados en la cara superior de las cintas...")
    y_bateria = 518.0
    posiciones_z = [-120.0, -40.0, 40.0, 120.0]
    for i, z_pos in enumerate(posiciones_z, start=1):
        m_bat = matrix_transform(app, x_mm=-270, y_mm=y_bateria, z_mm=z_pos, rot_y_deg=90)
        occs.Add(PART_P540, m_bat)
        print(f"  -> Perfil Batería {i}/4 (L=540mm) apoyado en Z = {z_pos:+.1f} mm")

    # --------------------------------------------------------------------------
    # E. GUARDAR ENSAMBLAJES, EXPORTAR STEP UNIVERSAL Y CREAR ZIP
    # --------------------------------------------------------------------------
    ruta_cubo = os.path.join(ENSAMBLAJES_DIR, "Banco_Mecatronico_Cubo_50x54.iam")
    doc.SaveAs(ruta_cubo, False)
    print(f"\n[Ensamblaje] Guardado IAM: {ruta_cubo}")

    ruta_principal = os.path.join(ENSAMBLAJES_DIR, "Banco_Mecatronico_TFG_Principal.iam")
    doc.SaveAs(ruta_principal, True)
    print(f"[Ensamblaje] Guardado Principal IAM: {ruta_principal}")

    ruta_step = os.path.join(ENSAMBLAJES_DIR, "Banco_Mecatronico_Cubo_50x54.step")
    try:
        doc.SaveAs(ruta_step, True)
        print(f"[Exportación STEP] Guardado STEP universal: {ruta_step} ({os.path.getsize(ruta_step)} bytes)")
    except Exception as e:
        print("  -> Error exportando STEP:", e)

    doc.Close(True)
    empaquetar_proyecto_zip()

    # --------------------------------------------------------------------------
    # F. RENDERIZAR VISTAS PARA VERIFICACIÓN VISUAL
    # --------------------------------------------------------------------------
    print("[Verificación] Abriendo visualización en Inventor y generando capturas de alta resolución...")
    doc_ui = app.Documents.Open(ruta_cubo, True)
    view = app.ActiveView

    try:
        view.DisplayMode = inv.DisplayModeEnum.kShadedWithEdgesRendering
    except Exception:
        pass

    # 1. Vista Detalle Croquis: Primer plano del cabezal motriz con los dos engranajes oro y la cinta negra
    cam = view.Camera
    cam.Target = app.TransientGeometry.CreatePoint(mm(-250), mm(494), mm(-210))
    cam.Eye = app.TransientGeometry.CreatePoint(mm(-150), mm(570), mm(-130))
    cam.UpVector = app.TransientGeometry.CreateUnitVector(0, 1, 0)
    cam.SetExtents(mm(170), mm(130))
    cam.ApplyWithoutTransition()
    img_croquis_match = os.path.join(ENSAMBLAJES_DIR, "detalle_cinta_engranajes_croquis.png")
    view.SaveAsBitmap(img_croquis_match, 1280, 960)
    print(f"  -> Captura detalle croquis: {img_croquis_match}")

    # 2. Vista Isométrica General del Banco
    cam.ViewOrientationType = inv.ViewOrientationTypeEnum.kIsoTopRightViewOrientation
    cam.ApplyWithoutTransition()
    view.Fit()
    img_iso = os.path.join(ENSAMBLAJES_DIR, "cubo_completo_isometrica.png")
    view.SaveAsBitmap(img_iso, 1280, 960)
    print(f"  -> Captura isométrica: {img_iso}")

    # 3. Vista Superior en Planta de la Batería
    cam.ViewOrientationType = inv.ViewOrientationTypeEnum.kTopViewOrientation
    cam.ApplyWithoutTransition()
    view.Fit()
    img_top = os.path.join(ENSAMBLAJES_DIR, "cubo_completo_planta_bateria.png")
    view.SaveAsBitmap(img_top, 1280, 960)
    print(f"  -> Captura en planta: {img_top}")

    print("================================================================================")
    print("PROCESO COMPLETADO EXITOSAMENTE. MODELO VISIBLE EN AUTODESK INVENTOR.")
    print("================================================================================")
    return ruta_cubo


if __name__ == "__main__":
    construir_ensamblaje()
