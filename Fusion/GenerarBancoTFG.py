# ==============================================================================
# Script de Automatización Oficial para Autodesk Fusion 360
# TFG: Banco Mecatrónico - Modelo 1:1 del Bastidor Real Medido en Taller
# Perfilería 2020: 540 x 500 mm con 4 escuadras de fundición de aluminio
# ==============================================================================

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # 1. Obtener o crear un documento nuevo en Fusion 360
        design = app.activeProduct
        if not design or not isinstance(design, adsk.fusion.Design):
            doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
            design = app.activeProduct

        rootComp = design.rootComponent
        extrudes = rootComp.features.extrudeFeatures

        # Parámetros en centímetros (la API de Fusion 360 usa cm)
        # 1 cm = 10 mm
        P_SZ = 2.0        # 20 mm
        H_COL = 50.0      # 500 mm (Altura columnas)
        L_TRAV = 50.0     # 500 mm (Luz interior / longitud travesaño)
        W_EXT = 54.0      # 540 mm (Ancho exterior total)
        Z_TRAV_SUP = 46.0 # Cara inferior a 46 cm, superior a 48 cm (deja 2 cm para escuadra)
        Z_TRAV_INF = 2.0  # Cara inferior a 2 cm sobre el suelo

        # Función auxiliar para extruir prisma de perfil
        def crear_perfil(nombre, p1, p2, dist):
            sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
            sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(p1[0], p1[1], 0),
                adsk.core.Point3D.create(p2[0], p2[1], 0)
            )
            prof = sketch.profiles.item(0)
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(dist))
            feat = extrudes.add(extInput)
            b = feat.bodies.item(0)
            b.name = nombre
            return b

        # Centrado en X = 0:
        # Columna Izquierda: X de -27 cm a -25 cm, Y de -1 cm a +1 cm, extrusión en Z de 0 a 50 cm
        crear_perfil("Columna_Izquierda_2020_500mm", [-27.0, -1.0], [-25.0, 1.0], H_COL)

        # Columna Derecha: X de +25 cm a +27 cm, Y de -1 cm a +1 cm, extrusión en Z de 0 a 50 cm
        crear_perfil("Columna_Derecha_2020_500mm", [25.0, -1.0], [27.0, 1.0], H_COL)

        # Travesaño Superior: entre X = -25 cm y X = +25 cm (50 cm de largo)
        # Dibujamos en plano XZ a Z = 46 cm y extruimos en Y
        sketchTS = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchTS.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(-25.0, 46.0, 0),
            adsk.core.Point3D.create(25.0, 48.0, 0)
        )
        profTS = sketchTS.profiles.item(0)
        extTS = extrudes.createInput(profTS, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extTS.setDistanceExtent(False, adsk.core.ValueInput.createByReal(P_SZ))
        featTS = extrudes.add(extTS)
        featTS.bodies.item(0).name = "Travesano_Superior_2020_500mm"

        # Travesaño Inferior: entre X = -25 cm y X = +25 cm a Z = 2 cm
        sketchTI = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchTI.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(-25.0, 2.0, 0),
            adsk.core.Point3D.create(25.0, 4.0, 0)
        )
        profTI = sketchTI.profiles.item(0)
        extTI = extrudes.createInput(profTI, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extTI.setDistanceExtent(False, adsk.core.ValueInput.createByReal(P_SZ))
        featTI = extrudes.add(extTI)
        featTI.bodies.item(0).name = "Travesano_Inferior_2020_500mm"

        # 4 Escuadras de 90 grados
        def crear_escuadra(nombre, x0, z0, dx, dz):
            sketchE = rootComp.sketches.add(rootComp.xZConstructionPlane)
            lines = sketchE.sketchCurves.sketchLines
            pA = adsk.core.Point3D.create(x0, z0, 0)
            pB = adsk.core.Point3D.create(x0 + dx, z0, 0)
            pC = adsk.core.Point3D.create(x0, z0 + dz, 0)
            lines.addByTwoPoints(pA, pB)
            lines.addByTwoPoints(pB, pC)
            lines.addByTwoPoints(pC, pA)
            profE = sketchE.profiles.item(0)
            extE = extrudes.createInput(profE, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extE.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.8))
            featE = extrudes.add(extE)
            featE.bodies.item(0).name = nombre

        # Superior Izquierda (sobre travesaño superior)
        crear_escuadra("Escuadra_Superior_Izquierda", -25.0, 48.0, 2.0, 2.0)
        # Superior Derecha
        crear_escuadra("Escuadra_Superior_Derecha", 25.0, 48.0, -2.0, 2.0)
        # Inferior Izquierda (bajo travesaño inferior)
        crear_escuadra("Escuadra_Inferior_Izquierda", -25.0, 2.0, 2.0, -2.0)
        # Inferior Derecha
        crear_escuadra("Escuadra_Inferior_Derecha", 25.0, 2.0, -2.0, -2.0)

        if ui:
            ui.messageBox(
                "¡Bastidor Real 1:1 generado con éxito en Fusion 360!\n\n"
                "- 2 Columnas verticales: 500 mm (Perfil 2020)\n"
                "- 2 Travesaños horizontales: 500 mm (Luz interior 500 mm)\n"
                "- Ancho exterior total: 540 mm\n"
                "- 4 Escuadras triangulares de 90° de fundición de aluminio"
            )

    except:
        if ui:
            ui.messageBox('Error en el script de Fusion 360:\n{}'.format(traceback.format_exc()))

def stop(context):
    pass
