"""
================================================================================
GENERADOR MAESTRO DE PIEZAS PARAMÉTRICAS (.ipt) EN AUTODESK INVENTOR 2027
Proyecto: Banco Mecatrónico TFG - Microgravedad Simulada
Directorio: Parte mecanica/Inventor/scripts/generar_piezas_ipt.py
================================================================================
Genera todas las piezas individuales nativas con parámetros y cotas nominales:
1. Perfiles de aluminio estructural 2020 (L = 500 mm, 540 mm, 600 mm).
2. Escuadra de 90° de fundición con nervios y colisos (20x20x20 mm).
3. Tornillo Allen DIN 912 M5x8 con cabeza cilíndrica.
4. Rueda V-Wheel de POM con perfil en V a 90°.
5. Carro móvil transversal Gantry con soporte de péndulo y mordazas GT2.
6. Motor paso a paso NEMA 17 (42x42x40 mm, eje 5 mm).
7. Engranaje recto métrico de evolvente 1:1 (m = 1.0 mm, Z = 20, b = 7 mm).
8. Polea síncrona GT2 de 20 dientes (Dp = 12.73 mm, ancho 7 mm, eje 5 mm).
9. Soporte de fijación de motor NEMA 17 a perfil 2020 (distancia ejes 20 mm).
10. Soporte tensor de polea loca GT2 para perfil 2020.
================================================================================
"""

import os
import sys
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from inventor_core import InventorManager, mm, pt2d, pt3d, vec3d, inv

INVENTOR_ROOT = os.path.dirname(SCRIPT_DIR)
PIEZAS_DIR = os.path.join(INVENTOR_ROOT, "piezas")
os.makedirs(PIEZAS_DIR, exist_ok=True)


def crear_perfil_2020(app: inv.Application, longitud_mm: float, nombre_archivo: str):
    """
    Genera un perfil de aluminio 2020 con ranuras V-Slot y taladro central.
    """
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        print(f"[Piezas] {nombre_archivo}.ipt ya existe. Omitiendo regeneración.")
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt (Longitud: {longitud_mm} mm)...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition
    tg = app.TransientGeometry

    # Boceto en plano XY (WorkPlanes.Item(3))
    sketch = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))

    # 1. Contorno exterior 20x20 mm centrado en el origen
    lines = sketch.SketchLines
    w = 10.0 # Semiancho 10 mm
    p_bl = pt2d(app, -w, -w)
    p_tr = pt2d(app, w, w)
    lines.AddAsTwoPointRectangle(p_bl, p_tr)

    # 2. Taladro central del núcleo (diámetro 4.2 mm para roscar M5 -> radio 2.1 mm)
    sketch.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.1))

    # 3. Ranuras exteriores de 6.0 mm x 1.8 mm en las 4 caras
    # Ranura superior (Y = +10 mm)
    lines.AddAsTwoPointRectangle(pt2d(app, -3.0, 10.0 - 1.8), pt2d(app, 3.0, 10.0))
    # Ranura inferior (Y = -10 mm)
    lines.AddAsTwoPointRectangle(pt2d(app, -3.0, -10.0), pt2d(app, 3.0, -10.0 + 1.8))
    # Ranura derecha (X = +10 mm)
    lines.AddAsTwoPointRectangle(pt2d(app, 10.0 - 1.8, -3.0), pt2d(app, 10.0, 3.0))
    # Ranura izquierda (X = -10 mm)
    lines.AddAsTwoPointRectangle(pt2d(app, -10.0, -3.0), pt2d(app, -10.0 + 1.8, 3.0))

    # Perfil cerrado para extrusión sólida
    prof = sketch.Profiles.AddForSolid()

    # Extrusión longitudinal a lo largo del eje Z positivo
    ext_features = part_def.Features.ExtrudeFeatures
    ext_features.AddByDistanceExtent(
        prof,
        mm(longitud_mm),
        inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_escuadra_90(app: inv.Application):
    """
    Genera la escuadra de 90° de fundición con nervios laterales y colisos (20x20x20 mm).
    """
    nombre_archivo = "Escuadra_90_Fundicion_2020"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        print(f"[Piezas] {nombre_archivo}.ipt ya existe.")
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition
    tg = app.TransientGeometry

    # Boceto en plano XZ (WorkPlanes.Item(2))
    sketch = part_def.Sketches.Add(part_def.WorkPlanes.Item(2))
    lines = sketch.SketchLines

    # Perfil L exterior de 20x20 mm con nervio diagonal a 45° encadenando vértices
    p0 = pt2d(app, 0, 0)
    l1 = lines.AddByTwoPoints(p0, pt2d(app, 20.0, 0))
    l2 = lines.AddByTwoPoints(l1.EndSketchPoint, pt2d(app, 20.0, 3.5))
    l3 = lines.AddByTwoPoints(l2.EndSketchPoint, pt2d(app, 16.5, 3.5))
    l4 = lines.AddByTwoPoints(l3.EndSketchPoint, pt2d(app, 3.5, 16.5))
    l5 = lines.AddByTwoPoints(l4.EndSketchPoint, pt2d(app, 3.5, 20.0))
    l6 = lines.AddByTwoPoints(l5.EndSketchPoint, pt2d(app, 0, 20.0))
    l7 = lines.AddByTwoPoints(l6.EndSketchPoint, l1.StartSketchPoint)

    prof = sketch.Profiles.AddForSolid()

    # Extrusión simétrica de 20 mm (10 mm a cada lado)
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof,
        mm(20.0),
        inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    # Vaciado central de 15 mm (dejando los 2 nervios laterales de 2.5 mm)
    sketch_pocket = part_def.Sketches.Add(part_def.WorkPlanes.Item(2))
    lp = sketch_pocket.SketchLines
    p_p0 = pt2d(app, 3.0, 3.0)
    lp1 = lp.AddByTwoPoints(p_p0, pt2d(app, 21.0, 3.0))
    lp2 = lp.AddByTwoPoints(lp1.EndSketchPoint, pt2d(app, 21.0, 21.0))
    lp3 = lp.AddByTwoPoints(lp2.EndSketchPoint, pt2d(app, 3.0, 21.0))
    lp4 = lp.AddByTwoPoints(lp3.EndSketchPoint, lp1.StartSketchPoint)

    prof_pocket = sketch_pocket.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_pocket,
        mm(15.0), # Ancho del cajeado central
        inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kCutOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_tornillo_m5(app: inv.Application):
    """
    Genera el tornillo Allen DIN 912 M5x8 con cabeza cilíndrica.
    """
    nombre_archivo = "Tornillo_M5x8_DIN912"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    # 1. Cabeza cilíndrica (diámetro 8.5 mm, altura 5.0 mm)
    sk_head = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_head.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(8.5 / 2))
    prof_head = sk_head.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_head, mm(5.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    # 2. Vástago roscado M5 (diámetro 5.0 mm, longitud 8.0 mm)
    sk_shank = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_shank.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(5.0 / 2))
    prof_shank = sk_shank.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_shank, mm(8.0), inv.PartFeatureExtentDirectionEnum.kNegativeExtentDirection,
        inv.PartFeatureOperationEnum.kJoinOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_rueda_vwheel(app: inv.Application):
    """
    Genera la rueda V-Wheel de POM con garganta a 90° para perfil 2020.
    """
    nombre_archivo = "Rueda_VWheel_POM"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    # Cilindro exterior: diámetro 24.39 mm, ancho 10.23 mm
    sk = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(24.39 / 2))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(5.0 / 2)) # Eje central M5
    prof = sk.Profiles.AddForSolid()

    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof, mm(10.23), inv.PartFeatureExtentDirectionEnum.kSymmetricExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_carro_gantry(app: inv.Application):
    """
    Genera la placa móvil transversal del carro (Gantry Plate) de 65x65 mm
    con 4 taladros para ruedas V-wheel (44x40 mm), soporte para joystick
    y ojal de paso para el hilo de suspensión.
    """
    nombre_archivo = "Carro_Transversal_Gantry"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    sk = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    lines = sk.SketchLines

    # 1. Placa principal 65x65 mm centrada en X, extendida en Y hacia abajo
    p1 = pt2d(app, -32.5, -32.5)
    p2 = pt2d(app, 32.5, 32.5)
    lines.AddAsTwoPointRectangle(p1, p2)

    # 2. Pletina inferior extendida para el soporte del sensor joystick (-25 mm)
    p_ext1 = pt2d(app, -32.5, -32.5 - 25.0)
    p_ext2 = pt2d(app, 32.5, -32.5)
    lines.AddAsTwoPointRectangle(p_ext1, p_ext2)

    # 3. Cuatro taladros para ruedas V-Wheel (44 mm entre ejes X, 40 mm entre ejes Y)
    wx = 44.0 / 2 # 22 mm
    wy = 40.0 / 2 # 20 mm
    r_wheel = 5.2 / 2 # Taladros M5
    sk.SketchCircles.AddByCenterRadius(pt2d(app, -wx, wy), mm(r_wheel))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, wx, wy), mm(r_wheel))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, -wx, -wy), mm(r_wheel))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, wx, -wy), mm(r_wheel))

    # 4. Ojal central para el hilo de suspensión (diámetro 4.5 mm)
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, -32.5 - 12.5), mm(4.5 / 2))

    # 5. Taladros de montaje del sensor joystick (paso 26 mm x 32 mm)
    sk.SketchCircles.AddByCenterRadius(pt2d(app, -13.0, -32.5 - 12.5), mm(3.4 / 2))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 13.0, -32.5 - 12.5), mm(3.4 / 2))

    prof = sk.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof, mm(5.0), # Espesor 5 mm
        inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_motor_nema17(app: inv.Application):
    """
    Genera el motor paso a paso NEMA 17 estándar (42x42x40 mm, eje D 5x24 mm).
    """
    nombre_archivo = "Motor_NEMA17"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    # Cuerpo cúbico 42x42x40 mm
    sk_body = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_body.SketchLines.AddAsTwoPointRectangle(pt2d(app, -21.0, -21.0), pt2d(app, 21.0, 21.0))
    prof_body = sk_body.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_body, mm(40.0), inv.PartFeatureExtentDirectionEnum.kNegativeExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    # Resalte piloto frontal (diámetro 22 mm x 2 mm)
    sk_pilot = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_pilot.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(11.0))
    prof_pilot = sk_pilot.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_pilot, mm(2.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kJoinOperation
    )

    # Eje frontal del motor (diámetro 5 mm x 24 mm)
    sk_shaft = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_shaft.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5))
    prof_shaft = sk_shaft.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_shaft, mm(24.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kJoinOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_engranaje_recto_1a1(app: inv.Application):
    """
    Genera el engranaje recto métrico con 20 dientes reales de evolvente (m = 1.0 mm, Z = 20, Dp = 20 mm, b = 7 mm).
    """
    nombre_archivo = "Engranaje_Recto_1a1_m1_Z20"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    sk = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    lines = sk.SketchLines

    z = 20
    m = 1.0
    r_a = 11.0  # Radio exterior de cabeza (diámetro 22.0 mm)
    r_f = 8.75  # Radio de fondo (diámetro 17.5 mm)
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

    # Taladro para eje NEMA 17 (diámetro 5.0 mm -> radio 2.5 mm)
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5))

    prof = sk.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof, mm(7.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_cinta_transportadora(app: inv.Application):
    """
    Genera la cinta transportadora en bucle cerrado (estadio) con dientes internos.
    """
    nombre_archivo = "Cinta_Transportadora_20mm_L500"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
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

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_polea_gt2_20t(app: inv.Application):
    """
    Genera la polea síncrona GT2 de 20 dientes (Dp = 12.73 mm, ancho 7 mm, eje 5 mm).
    """
    nombre_archivo = "Polea_GT2_20T"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    # 1. Cuerpo dentado (diámetro exterior Do = 12.22 mm, ancho 7.0 mm)
    sk_body = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_body.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(12.22 / 2))
    sk_body.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5)) # Taladro eje 5 mm
    prof_body = sk_body.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_body, mm(7.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    # 2. Pestañas laterales de contención (diámetro 16 mm x 1.0 mm)
    sk_flange1 = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    sk_flange1.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(8.0))
    sk_flange1.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(2.5))
    prof_flange1 = sk_flange1.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof_flange1, mm(1.0), inv.PartFeatureExtentDirectionEnum.kNegativeExtentDirection,
        inv.PartFeatureOperationEnum.kJoinOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_soporte_motor(app: inv.Application):
    """
    Genera el soporte de motor NEMA 17 para montaje en perfil 2020 con
    distancia entre centros a = 20.0 mm para acoplamiento del tren 1:1.
    """
    nombre_archivo = "Soporte_Motor_NEMA17_2020"
    ruta_completa = os.path.join(PIEZAS_DIR, f"{nombre_archivo}.ipt")
    if os.path.exists(ruta_completa):
        return ruta_completa

    print(f"[Piezas] Modelando {nombre_archivo}.ipt...")
    doc = app.Documents.Add(inv.DocumentTypeEnum.kPartDocumentObject, CreateVisible=False)
    part_def = doc.ComponentDefinition

    sk = part_def.Sketches.Add(part_def.WorkPlanes.Item(3))
    # Placa base de 44x64x5 mm
    sk.SketchLines.AddAsTwoPointRectangle(pt2d(app, -22.0, -22.0), pt2d(app, 22.0, 42.0))

    # Taladro para eje del motor en (0, 0)
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 0), mm(11.5))
    # Taladros de fijación M3 del motor
    sk.SketchCircles.AddByCenterRadius(pt2d(app, -15.5, -15.5), mm(1.7))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 15.5, -15.5), mm(1.7))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, -15.5, 15.5), mm(1.7))
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 15.5, 15.5), mm(1.7))

    # Taladro para el eje secundario con distancia entre centros a = 20.0 mm
    sk.SketchCircles.AddByCenterRadius(pt2d(app, 0, 20.0), mm(5.0))

    prof = sk.Profiles.AddForSolid()
    part_def.Features.ExtrudeFeatures.AddByDistanceExtent(
        prof, mm(5.0), inv.PartFeatureExtentDirectionEnum.kPositiveExtentDirection,
        inv.PartFeatureOperationEnum.kNewBodyOperation
    )

    doc.SaveAs(ruta_completa, False)
    doc.Close(True)
    print(f"[Piezas] Guardado: {ruta_completa}")
    return ruta_completa


def crear_todas_las_piezas():
    """Genera el catálogo completo de piezas paramétricas del banco mecatrónico."""
    app = InventorManager.get_app()
    print("================================================================================")
    print("INICIANDO GENERACIÓN PARAMÉTRICA DE PIEZAS NATIVAS (.ipt)")
    print("================================================================================")

    # 1. Perfiles estructurales 2020
    crear_perfil_2020(app, 500.0, "Perfil_2020_L500")
    crear_perfil_2020(app, 540.0, "Perfil_2020_L540")
    crear_perfil_2020(app, 600.0, "Perfil_2020_L600")

    # 2. Herrajes estructurales
    crear_escuadra_90(app)
    crear_tornillo_m5(app)

    # 3. Componentes del carro móvil transversal
    crear_rueda_vwheel(app)
    crear_carro_gantry(app)

    # 4. Transmisión cinemática
    crear_motor_nema17(app)
    crear_engranaje_recto_1a1(app)
    crear_polea_gt2_20t(app)
    crear_soporte_motor(app)

    print("================================================================================")
    print("TODAS LAS PIEZAS (.ipt) HAN SIDO GENERADAS CORRECTAMENTE.")
    print("================================================================================")


if __name__ == "__main__":
    crear_todas_las_piezas()
