"""
================================================================================
GENERADOR MAESTRO DEL BANCO MECATRÓNICO CÚBICO EN AUTODESK INVENTOR 2027
Proyecto: Banco Mecatrónico TFG - Microgravedad Simulada
Directorio: Parte mecanica/Inventor/scripts/generar_cubo_con_cintas.py
================================================================================
Estructura oficial alineada con el sistema de coordenadas estándar de Inventor:
- Eje Y = VERTICAL (ALTURA): de Y = 0 a Y = 500 mm.
- Eje X = TRANSVERSAL (ANCHO): de X = -270 a +270 mm (540 mm exterior).
- Eje Z = LONGITUDINAL (PROFUNDIDAD): de Z = -250 a +250 mm (500 mm).

Componentes modelados y ensamblados:
1. Bastidor Cúbico 50x54 cm en perfiles 2020 de catálogo oficial B-Rep:
   - 4 Columnas verticales de 500 mm (orientadas en Y de 0 a 500 mm).
   - 4 Travesaños de base en el plano inferior (2 en X de 500 mm, 2 en Z de 460 mm).
   - 4 Travesaños superiores de corona (2 en X de 500 mm, 2 en Z de 460 mm).
2. 16 Escuadras de 90° con sus 32 tornillos Allen DIN 912 M5 con arandela:
   - Caras perfectamente enrasadas con las ranuras de perfilería.
   - 2 tornillos por escuadra colocados analíticamente en sus colisos.
3. Mecanismo de tracción superior (Croquis 04-11-2026):
   - 2 Cintas transportadoras en bucle cerrado sobre los dos perfiles laterales superiores.
   - Motor NEMA 17 acoplado mediante tren de engranajes rectos 1:1 (Z=20, m=1.0).
   - Eje transversal de distribución (5 mm x 520 mm) conectando ambas poleas motrices GT2.
   - 2 Poleas locas traseras de retorno.
4. Batería de 4 perfiles transversales apoyados directamente sobre las 2 cintas:
   - 4 perfiles 2020 de 540 mm de longitud cruzando de X = -270 a +270 mm.
   - Apoyados sobre la cara superior de las cintas a Y = 500 mm.
================================================================================
"""

import os
import sys
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from inventor_core import InventorManager, mm, matrix_transform, inv

INVENTOR_ROOT = os.path.dirname(SCRIPT_DIR)
PIEZAS_DIR = os.path.join(INVENTOR_ROOT, "piezas")
ENSAMBLAJES_DIR = os.path.join(INVENTOR_ROOT, "ensamblajes")
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


def agregar_escuadra_con_dos_tornillos(app: inv.Application, occs: inv.ComponentOccurrences, 
                                       m_bracket: inv.Matrix):
    """
    Inserta una escuadra de 90° con sus DOS tornillos Allen M5 con arandela.
    - Tornillo 1: Cara horizontal Z=0 (hacia viga horizontal).
    - Tornillo 2: Cara vertical X=0 (hacia columna vertical).
    """
    occs.Add(PART_BRACKET, m_bracket)

    # Tornillo 1 (Cara horizontal, coliso Z = 0)
    m_s1_local = matrix_transform(app, x_mm=10.5, y_mm=0.0, z_mm=3.0)
    m_s1_local.TransformBy(m_bracket)
    occs.Add(PART_SCREW, m_s1_local)

    # Tornillo 2 (Cara vertical, coliso X = 0)
    m_s2_local = matrix_transform(app, x_mm=3.0, y_mm=0.0, z_mm=10.5, rot_y_deg=90.0)
    m_s2_local.TransformBy(m_bracket)
    occs.Add(PART_SCREW, m_s2_local)


def construir_ensamblaje_completo():
    app = InventorManager.get_app()
    print("================================================================================")
    print("CONSTRUYENDO MODELO OFICIAL EN INVENTOR 2027 (Y = VERTICAL UP)")
    print("================================================================================")

    doc = app.Documents.Add(inv.DocumentTypeEnum.kAssemblyDocumentObject, CreateVisible=False)
    comp_def = doc.ComponentDefinition
    occs = comp_def.Occurrences

    # --------------------------------------------------------------------------
    # 1. CUBO DE PERFILES 2020 DE ALTA FIDELIDAD (50 x 54 cm, H = 50 cm)
    # X: -270 a +270 mm (Ancho 540 mm)
    # Y: 0 a 500 mm (Altura 500 mm)
    # Z: -250 a +250 mm (Profundidad 500 mm)
    # --------------------------------------------------------------------------
    print("[1/4] Ensamblando 4 columnas verticales 2020 de 500 mm en Y...")
    # Las columnas van a lo largo de +Y (rot_x_deg = -90 convierte Z a +Y)
    # Front-Left (FL)
    m_c_fl = matrix_transform(app, x_mm=-260, y_mm=0, z_mm=-240, rot_x_deg=-90)
    occ_ref = occs.Add(PART_P500, m_c_fl)
    occ_ref.Grounded = True

    # Front-Right (FR)
    m_c_fr = matrix_transform(app, x_mm=260, y_mm=0, z_mm=-240, rot_x_deg=-90)
    occs.Add(PART_P500, m_c_fr)

    # Back-Left (BL)
    m_c_bl = matrix_transform(app, x_mm=-260, y_mm=0, z_mm=240, rot_x_deg=-90)
    occs.Add(PART_P500, m_c_bl)

    # Back-Right (BR)
    m_c_br = matrix_transform(app, x_mm=260, y_mm=0, z_mm=240, rot_x_deg=-90)
    occs.Add(PART_P500, m_c_br)

    # --- TRAVESAÑOS INFERIORES DE LA BASE (Y de 20 a 40 mm, centro Y = 30 mm) ---
    print("[1/4] Ensamblando 4 travesaños inferiores de la base...")
    # Frontal Inferior en X (L = 500 mm, de X = -250 a +250 mm)
    m_b_f = matrix_transform(app, x_mm=-250, y_mm=30, z_mm=-240, rot_y_deg=90)
    occs.Add(PART_P500, m_b_f)

    # Trasero Inferior en X (L = 500 mm, de X = -250 a +250 mm)
    m_b_b = matrix_transform(app, x_mm=-250, y_mm=30, z_mm=240, rot_y_deg=90)
    occs.Add(PART_P500, m_b_b)

    # Lateral Izquierdo Inferior en Z (L = 460 mm, de Z = -230 a +230 mm)
    m_b_l = matrix_transform(app, x_mm=-260, y_mm=30, z_mm=-230)
    occs.Add(PART_P460, m_b_l)

    # Lateral Derecho Inferior en Z (L = 460 mm, de Z = -230 a +230 mm)
    m_b_r = matrix_transform(app, x_mm=260, y_mm=30, z_mm=-230)
    occs.Add(PART_P460, m_b_r)

    # --- TRAVESAÑOS SUPERIORES DE CORONA (Y de 460 a 480 mm, centro Y = 470 mm) ---
    print("[1/4] Ensamblando 4 travesaños superiores de corona...")
    # Frontal Superior en X (L = 500 mm)
    m_t_f = matrix_transform(app, x_mm=-250, y_mm=470, z_mm=-240, rot_y_deg=90)
    occs.Add(PART_P500, m_t_f)

    # Trasero Superior en X (L = 500 mm)
    m_t_b = matrix_transform(app, x_mm=-250, y_mm=470, z_mm=240, rot_y_deg=90)
    occs.Add(PART_P500, m_t_b)

    # Lateral Izquierdo Superior en Z (L = 460 mm, cara superior a Y = 480 mm)
    m_t_l = matrix_transform(app, x_mm=-260, y_mm=470, z_mm=-230)
    occs.Add(PART_P460, m_t_l)

    # Lateral Derecho Superior en Z (L = 460 mm, cara superior a Y = 480 mm)
    m_t_r = matrix_transform(app, x_mm=260, y_mm=470, z_mm=-230)
    occs.Add(PART_P460, m_t_r)

    # --------------------------------------------------------------------------
    # 2. ESCUADRAS DE 90° CON DOS TORNILLOS ALLEN M5 CADA UNA
    # --------------------------------------------------------------------------
    print("[2/4] Colocando 16 escuadras de 90° con 32 tornillos M5 enrasados...")

    # A) Marco Frontal (Z = -240 mm, vigas en X):
    # FL-Top: (-250, 480, -240)
    m_f_fl_t = matrix_transform(app, x_mm=-250, y_mm=480, z_mm=-240, rot_x_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_f_fl_t)

    # FR-Top: (+250, 480, -240)
    m_f_fr_t = matrix_transform(app, x_mm=250, y_mm=480, z_mm=-240, rot_x_deg=-90, rot_z_deg=180)
    agregar_escuadra_con_dos_tornillos(app, occs, m_f_fr_t)

    # FL-Bottom: (-250, 20, -240)
    m_f_fl_b = matrix_transform(app, x_mm=-250, y_mm=20, z_mm=-240, rot_x_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_f_fl_b)

    # FR-Bottom: (+250, 20, -240)
    m_f_fr_b = matrix_transform(app, x_mm=250, y_mm=20, z_mm=-240, rot_x_deg=90, rot_z_deg=180)
    agregar_escuadra_con_dos_tornillos(app, occs, m_f_fr_b)

    # B) Marco Trasero (Z = +240 mm, vigas en X):
    # BL-Top: (-250, 480, 240)
    m_b_bl_t = matrix_transform(app, x_mm=-250, y_mm=480, z_mm=240, rot_x_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_b_bl_t)

    # BR-Top: (+250, 480, 240)
    m_b_br_t = matrix_transform(app, x_mm=250, y_mm=480, z_mm=240, rot_x_deg=-90, rot_z_deg=180)
    agregar_escuadra_con_dos_tornillos(app, occs, m_b_br_t)

    # BL-Bottom: (-250, 20, 240)
    m_b_bl_b = matrix_transform(app, x_mm=-250, y_mm=20, z_mm=240, rot_x_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_b_bl_b)

    # BR-Bottom: (+250, 20, 240)
    m_b_br_b = matrix_transform(app, x_mm=250, y_mm=20, z_mm=240, rot_x_deg=90, rot_z_deg=180)
    agregar_escuadra_con_dos_tornillos(app, occs, m_b_br_b)

    # C) Marcos Laterales Izquierdo y Derecho (vigas en Z):
    # Left-Side Top Front: (-260, 480, -230)
    m_s_lf_t = matrix_transform(app, x_mm=-260, y_mm=480, z_mm=-230, rot_x_deg=-90, rot_z_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_lf_t)

    # Left-Side Top Rear: (-260, 480, 230)
    m_s_lr_t = matrix_transform(app, x_mm=-260, y_mm=480, z_mm=230, rot_x_deg=-90, rot_z_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_lr_t)

    # Left-Side Bottom Front: (-260, 20, -230)
    m_s_lf_b = matrix_transform(app, x_mm=-260, y_mm=20, z_mm=-230, rot_x_deg=90, rot_z_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_lf_b)

    # Left-Side Bottom Rear: (-260, 20, 230)
    m_s_lr_b = matrix_transform(app, x_mm=-260, y_mm=20, z_mm=230, rot_x_deg=90, rot_z_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_lr_b)

    # Right-Side Top Front: (+260, 480, -230)
    m_s_rf_t = matrix_transform(app, x_mm=260, y_mm=480, z_mm=-230, rot_x_deg=-90, rot_z_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_rf_t)

    # Right-Side Top Rear: (+260, 480, 230)
    m_s_rr_t = matrix_transform(app, x_mm=260, y_mm=480, z_mm=230, rot_x_deg=-90, rot_z_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_rr_t)

    # Right-Side Bottom Front: (+260, 20, -230)
    m_s_rf_b = matrix_transform(app, x_mm=260, y_mm=20, z_mm=-230, rot_x_deg=90, rot_z_deg=90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_rf_b)

    # Right-Side Bottom Rear: (+260, 20, 230)
    m_s_rr_b = matrix_transform(app, x_mm=260, y_mm=20, z_mm=230, rot_x_deg=90, rot_z_deg=-90)
    agregar_escuadra_con_dos_tornillos(app, occs, m_s_rr_b)

    # --------------------------------------------------------------------------
    # 3. MECANISMO SUPERIOR DE TRACCIÓN (Cintas, Engranajes 1:1, Motor y Eje)
    # --------------------------------------------------------------------------
    print("[3/4] Montando sistema cinemático superior (Cintas cerradas, Engranajes 1:1, Motor y Eje)...")
    # Cara superior de las vigas superiores: Y = 480 mm.
    # El centro del bucle de cinta se sitúa a Y = 489.5 mm (cara superior a Y = 499.0 mm)
    y_belt_center = 489.5

    # 1. Cinta Lateral Izquierda (X = -260 mm, extendida en Z de -230 a +230 mm)
    m_belt_l = matrix_transform(app, x_mm=-260, y_mm=y_belt_center, z_mm=0, rot_x_deg=90)
    occs.Add(PART_BELT, m_belt_l)

    # 2. Cinta Lateral Derecha (X = +260 mm, extendida en Z de -230 a +230 mm)
    m_belt_r = matrix_transform(app, x_mm=260, y_mm=y_belt_center, z_mm=0, rot_x_deg=90)
    occs.Add(PART_BELT, m_belt_r)

    # 3. Poleas Motrices Dentadas GT2 (Z = -230 mm, Y = 489.5 mm)
    m_pulley_l = matrix_transform(app, x_mm=-260, y_mm=y_belt_center, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_PULLEY, m_pulley_l)

    m_pulley_r = matrix_transform(app, x_mm=260, y_mm=y_belt_center, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_PULLEY, m_pulley_r)

    # 4. Poleas Locas Traseras de Retorno (Z = +230 mm, Y = 489.5 mm)
    m_pulley_lr = matrix_transform(app, x_mm=-260, y_mm=y_belt_center, z_mm=230, rot_y_deg=90)
    occs.Add(PART_PULLEY, m_pulley_lr)

    m_pulley_rr = matrix_transform(app, x_mm=260, y_mm=y_belt_center, z_mm=230, rot_y_deg=90)
    occs.Add(PART_PULLEY, m_pulley_rr)

    # 5. Eje Transversal de Sincronización y Distribución (L = 520 mm en X, de -260 a +260 mm)
    m_shaft = matrix_transform(app, x_mm=0, y_mm=y_belt_center, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_SHAFT, m_shaft)

    # 6. Tren de Engranajes 1:1 y Motor NEMA 17:
    # Engranaje conducido montado coaxial al eje de distribución en el exterior izquierdo (X = -275 mm)
    m_gear_driven = matrix_transform(app, x_mm=-275, y_mm=y_belt_center, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_GEAR, m_gear_driven)

    # Engranaje motor conductor engranando a distancia entre centros a = 20.0 mm en Y (Y = 509.5 mm)
    m_gear_motor = matrix_transform(app, x_mm=-275, y_mm=y_belt_center + 20.0, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_GEAR, m_gear_motor)

    # Motor NEMA 17 acoplado al engranaje conductor con eje entrando hacia +X a través del engranaje
    m_motor = matrix_transform(app, x_mm=-282, y_mm=y_belt_center + 20.0, z_mm=-230, rot_y_deg=90)
    occs.Add(PART_MOTOR, m_motor)

    # --------------------------------------------------------------------------
    # 4. BATERÍA DE 4 PERFILES APOYADOS DIRECTAMENTE SOBRE LAS CINTAS
    # --------------------------------------------------------------------------
    print("[4/4] Apoyando la batería de 4 perfiles transversales 2020 (L = 540 mm) sobre las dos cintas...")
    # Cara superior de las cintas a Y = 499.0 mm.
    # El perfil 2020 mide 20x20 mm, centro en Y a Y = 509.0 mm.
    # Los 4 perfiles cruzan transversalmente de X = -270 a +270 mm (longitud 540 mm)
    # y se distribuyen longitudinalmente en Z: Z = -120 mm, -40 mm, +40 mm, +120 mm
    y_bateria = 509.0
    posiciones_z_bateria = [-120.0, -40.0, 40.0, 120.0]

    for i, z_pos in enumerate(posiciones_z_bateria, start=1):
        m_bateria_perfil = matrix_transform(app, x_mm=-270, y_mm=y_bateria, z_mm=z_pos, rot_y_deg=90)
        occs.Add(PART_P540, m_bateria_perfil)
        print(f"  -> Perfil Batería {i}/4 (L=540mm) apoyado en Z = {z_pos:+.1f} mm (Y_apoyo = {y_bateria - 10.0:.1f} mm)")

    # --------------------------------------------------------------------------
    # 5. GUARDAR Y RENDERIZAR VISTAS MULTI-ÁNGULO PARA VERIFICACIÓN
    # --------------------------------------------------------------------------
    ruta_cubo = os.path.join(ENSAMBLAJES_DIR, "Banco_Mecatronico_Cubo_50x54.iam")
    doc.SaveAs(ruta_cubo, False)
    print(f"\n[Ensamblaje] Guardado: {ruta_cubo}")

    ruta_principal = os.path.join(ENSAMBLAJES_DIR, "Banco_Mecatronico_TFG_Principal.iam")
    doc.SaveAs(ruta_principal, True)
    print(f"[Ensamblaje] Guardado Ensamblaje Principal: {ruta_principal}")
    doc.Close(True)

    print("[Verificación] Abriendo documento en pantalla y generando capturas de alta resolución...")
    doc_ui = app.Documents.Open(ruta_cubo, True)
    view = app.ActiveView

    # 1. Vista Isométrica General
    view.Fit()
    img_iso = os.path.join(ENSAMBLAJES_DIR, "cubo_completo_isometrica.png")
    view.SaveAsBitmap(img_iso, 1280, 960)
    print(f"  -> Captura isométrica: {img_iso}")

    # 2. Vista Superior (Top View de la batería y cintas)
    cam = view.Camera
    cam.ViewOrientationType = inv.ViewOrientationTypeEnum.kTopViewOrientation
    cam.ApplyWithoutTransition()
    view.Fit()
    img_top = os.path.join(ENSAMBLAJES_DIR, "cubo_completo_planta_bateria.png")
    view.SaveAsBitmap(img_top, 1280, 960)
    print(f"  -> Captura en planta: {img_top}")

    # 3. Vista Detalle de la Transmisión Motor + Engranajes 1:1
    cam.ViewOrientationType = inv.ViewOrientationTypeEnum.kIsoTopLeftViewOrientation
    cam.ApplyWithoutTransition()
    view.Fit()
    img_detail = os.path.join(ENSAMBLAJES_DIR, "cubo_completo_detalle_transmision.png")
    view.SaveAsBitmap(img_detail, 1280, 960)
    print(f"  -> Captura detalle motor: {img_detail}")

    # 4. Vista Detalle Primer Plano de Escuadra con 2 Tornillos
    cam.Target = app.TransientGeometry.CreatePoint(mm(-245), mm(475), mm(-235))
    cam.Eye = app.TransientGeometry.CreatePoint(mm(-200), mm(510), mm(-190))
    cam.UpVector = app.TransientGeometry.CreateUnitVector(0, 1, 0)
    cam.ApplyWithoutTransition()
    img_corner = os.path.join(ENSAMBLAJES_DIR, "detalle_escuadra_y_tornillos_m5.png")
    view.SaveAsBitmap(img_corner, 1280, 960)
    print(f"  -> Captura detalle escuadra + tornillos: {img_corner}")

    # 5. Vista Detalle Primer Plano del Motor y Tren 1:1
    cam.Target = app.TransientGeometry.CreatePoint(mm(-275), mm(500), mm(-230))
    cam.Eye = app.TransientGeometry.CreatePoint(mm(-340), mm(530), mm(-170))
    cam.UpVector = app.TransientGeometry.CreateUnitVector(0, 1, 0)
    cam.ApplyWithoutTransition()
    img_gear_close = os.path.join(ENSAMBLAJES_DIR, "detalle_motor_engranajes_eje.png")
    view.SaveAsBitmap(img_gear_close, 1280, 960)
    print(f"  -> Captura detalle engranajes y motor: {img_gear_close}")

    print("================================================================================")
    print("PROCESO COMPLETADO EXITOSAMENTE: MODELO 100% PARAMÉTRICO Y NATIVO EN INVENTOR.")
    print("================================================================================")
    return ruta_principal


if __name__ == "__main__":
    construir_ensamblaje_completo()
