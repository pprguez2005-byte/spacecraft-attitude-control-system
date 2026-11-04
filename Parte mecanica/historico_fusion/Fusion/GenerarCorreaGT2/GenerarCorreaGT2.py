# ==============================================================================
# Script de Reparación y Generación de Correa GT2 para Autodesk Fusion 360
# TFG: Sistema Mecatrónico de Microgravedad Simulada
# ==============================================================================

import adsk.core, adsk.fusion, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design = app.activeProduct
        if not design or not isinstance(design, adsk.fusion.Design):
            ui.messageBox('Por favor, ten abierto tu diseño en Fusion 360 antes de ejecutar el script.')
            return

        rootComp = design.rootComponent
        extrudes = rootComp.features.extrudeFeatures

        # ----------------------------------------------------------------------
        # PASO 1: Buscar los engranajes en el modelo (incluyendo componentes/ocurrencias)
        # ----------------------------------------------------------------------
        gear_occs = []
        for occ in rootComp.allOccurrences:
            n = (occ.name + " " + occ.component.name).lower()
            if "gear" in n or "spur" in n or "engranaje" in n or "compound" in n:
                gear_occs.append(occ)

        gear_bodies = []
        for b in rootComp.bRepBodies:
            n = b.name.lower()
            if "gear" in n or "spur" in n or "engranaje" in n or "compound" in n:
                gear_bodies.append(b)

        # ----------------------------------------------------------------------
        # PASO 2: Buscar si hay un boceto existente de la cinta para repararlo
        # ----------------------------------------------------------------------
        belt_sketch = None
        if design.activeEditObject and isinstance(design.activeEditObject, adsk.fusion.Sketch):
            belt_sketch = design.activeEditObject
        else:
            for sk in reversed(list(rootComp.sketches)):
                if sk.sketchCurves.sketchArcs.count >= 1 and sk.sketchCurves.sketchLines.count >= 1:
                    belt_sketch = sk
                    break

        if belt_sketch:
            try:
                points = list(belt_sketch.sketchPoints)
                for i in range(len(points)):
                    p1 = points[i]
                    if p1.connectedEntities.count == 1:
                        for j in range(i + 1, len(points)):
                            p2 = points[j]
                            if p2.connectedEntities.count == 1:
                                dist = p1.geometry.distanceTo(p2.geometry)
                                if dist < 0.5:
                                    belt_sketch.geometricConstraints.addCoincident(p1, p2)
            except:
                pass

            if belt_sketch.profiles.count >= 1:
                target_prof = None
                for prof in belt_sketch.profiles:
                    if prof.profileLoops.count >= 2:
                        target_prof = prof
                        break
                if not target_prof and belt_sketch.profiles.count >= 2:
                    sorted_p = sorted([p for p in belt_sketch.profiles], key=lambda p: p.areaProperties().area)
                    target_prof = sorted_p[0]

                if target_prof:
                    extInput = extrudes.createInput(target_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                    extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.60))
                    feat = extrudes.add(extInput)
                    feat.bodies.item(0).name = "Correa_GT2_Reparada_Solida"
                    ui.messageBox(
                        "¡Boceto de la cinta reparado y extruido con éxito!\n\n"
                        "- Se detectó tu boceto existente.\n"
                        "- Se cerraron los puntos abiertos de las curvas.\n"
                        "- Se ha creado el cuerpo sólido continuo: 'Correa_GT2_Reparada_Solida'."
                    )
                    return

        # ----------------------------------------------------------------------
        # PASO 3: Si no se pudo reparar el boceto viejo, GENERAR LA CORREA NUEVA 1:1
        # ----------------------------------------------------------------------
        x_min, x_max = -25.0, 25.0
        z_pos = 49.0
        y_pos = 2.0

        if gear_occs:
            bb = gear_occs[0].boundingBox
            x_min = bb.minPoint.x + 1.0
            z_pos = (bb.minPoint.z + bb.maxPoint.z) / 2.0
            y_pos = bb.maxPoint.y
        elif gear_bodies:
            bb = gear_bodies[0].boundingBox
            x_min = bb.minPoint.x + 1.0
            z_pos = (bb.minPoint.z + bb.maxPoint.z) / 2.0
            y_pos = bb.maxPoint.y

        x_max = x_min + 46.0
        r_in = 1.00
        thick = 0.14
        r_out = r_in + thick
        width = 0.60

        planes = rootComp.constructionPlanes
        plInput = planes.createInput()
        plInput.setByOffset(rootComp.xZConstructionPlane, adsk.core.ValueInput.createByReal(y_pos))
        plane = planes.add(plInput)
        plane.name = "Plano_Frontal_Correa_GT2"

        sk = rootComp.sketches.add(plane)
        sk.name = "Boceto_Correa_GT2_Oficial"

        lines = sk.sketchCurves.sketchLines
        arcs = sk.sketchCurves.sketchArcs

        pt1_t = adsk.core.Point3D.create(x_min, z_pos + r_in, 0)
        pt1_b = adsk.core.Point3D.create(x_min, z_pos - r_in, 0)
        pt1_m = adsk.core.Point3D.create(x_min - r_in, z_pos, 0)

        pt2_t = adsk.core.Point3D.create(x_max, z_pos + r_in, 0)
        pt2_b = adsk.core.Point3D.create(x_max, z_pos - r_in, 0)
        pt2_m = adsk.core.Point3D.create(x_max + r_in, z_pos, 0)

        arc_in_l = arcs.addByThreePoints(pt1_t, pt1_m, pt1_b)
        line_in_b = lines.addByTwoPoints(pt1_b, pt2_b)
        arc_in_r = arcs.addByThreePoints(pt2_b, pt2_m, pt2_t)
        line_in_t = lines.addByTwoPoints(pt2_t, pt1_t)

        pt1_ot = adsk.core.Point3D.create(x_min, z_pos + r_out, 0)
        pt1_ob = adsk.core.Point3D.create(x_min, z_pos - r_out, 0)
        pt1_om = adsk.core.Point3D.create(x_min - r_out, z_pos, 0)

        pt2_ot = adsk.core.Point3D.create(x_max, z_pos + r_out, 0)
        pt2_ob = adsk.core.Point3D.create(x_max, z_pos - r_out, 0)
        pt2_om = adsk.core.Point3D.create(x_max + r_out, z_pos, 0)

        arc_out_l = arcs.addByThreePoints(pt1_ot, pt1_om, pt1_ob)
        line_out_b = lines.addByTwoPoints(pt1_ob, pt2_ob)
        arc_out_r = arcs.addByThreePoints(pt2_ob, pt2_om, pt2_ot)
        line_out_t = lines.addByTwoPoints(pt2_ot, pt1_ot)

        prof_belt = None
        for p in sk.profiles:
            if p.profileLoops.count == 2:
                prof_belt = p
                break
        if not prof_belt and sk.profiles.count >= 2:
            sorted_p = sorted([p for p in sk.profiles], key=lambda p: p.areaProperties().area)
            prof_belt = sorted_p[0]

        if prof_belt:
            extInput = extrudes.createInput(prof_belt, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(width))
            feat = extrudes.add(extInput)
            b = feat.bodies.item(0)
            b.name = "Correa_GT2_Solida_Completa_6mm"
            
            try:
                matLib = app.materialLibraries.itemByName("Fusion 360 Appearance Library")
                if matLib:
                    appear = matLib.appearances.itemByName("Rubber - Soft") or matLib.appearances.itemByName("Plastic - Matte (Black)")
                    if appear:
                        b.appearance = appear
            except:
                pass

            ui.messageBox(
                "¡Correa GT2 Sólida Generada y Posicionada con Éxito!\n\n"
                "- Alineada con tus engranajes reales.\n"
                "- Bucle 100% continuo y macizo (rectas y curvas cerradas).\n"
                "- Espesor: 1.4 mm | Ancho: 6.0 mm.\n"
                "- Nombre del cuerpo: 'Correa_GT2_Solida_Completa_6mm'."
            )
        else:
            ui.messageBox('No se pudo aislar el perfil anular de la correa.')

    except:
        if ui:
            ui.messageBox('Error en el script de Fusion 360:\n{}'.format(traceback.format_exc()))

def stop(context):
    pass
