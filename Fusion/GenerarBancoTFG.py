# ==============================================================================
# Script de Automatización Oficial para Autodesk Fusion 360
# TFG: Banco Mecatrónico de Microgravedad Simulada - Despliegue de Satélites
# Autor: TFG Ingeniería Mecatrónica
# ==============================================================================

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # 1. Obtener o crear un documento de diseño nuevo en Fusion 360
        design = app.activeProduct
        if not design or not isinstance(design, adsk.fusion.Design):
            doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
            design = app.activeProduct

        rootComp = design.rootComponent
        extrudes = rootComp.features.extrudeFeatures

        # ======================================================================
        # PARÁMETROS GEOMÉTRICOS NOMINALES (Medidas reales en centímetros)
        # 1 cm = 10 mm
        # ======================================================================
        P_SZ = 2.0        # Perfil 20x20 mm (2.0 cm)
        H_MARCO = 50.0    # Altura columnas 500 mm (50.0 cm)
        W_INT = 50.0      # Luz interior marco 500 mm (50.0 cm)
        W_EXT = 54.0      # Ancho total exterior 540 mm (54.0 cm)
        L_BAT = 60.0      # Batería perfiles longitudinales 600 mm (60.0 cm)
        N_PERF = 5        # 5 perfiles superiores
        PITCH = 12.0      # 120 mm entre centros (12.0 cm)

        # ----------------------------------------------------------------------
        # FUNCIÓN AUXILIAR PARA CREAR UN PERFIL T-SLOT / V-SLOT SIMPLIFICADO
        # ----------------------------------------------------------------------
        def crear_perfil_prisma(nombre, p_min, p_max, eje_extrude, distancia):
            sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
            lines = sketch.sketchCurves.sketchLines
            # Rectángulo exterior
            lines.addTwoPointRectangle(
                adsk.core.Point3D.create(p_min[0], p_min[1], p_min[2]),
                adsk.core.Point3D.create(p_max[0], p_max[1], p_max[2])
            )
            prof = sketch.profiles.item(0)
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extDist = adsk.core.ValueInput.createByReal(distancia)
            extInput.setDistanceExtent(False, extDist)
            extFeature = extrudes.add(extInput)
            body = extFeature.bodies.item(0)
            body.name = nombre
            return body

        # ----------------------------------------------------------------------
        # 1. BASTIDOR FRONTAL BASE (MEDIDAS DE TALLER: 540 x 500 mm)
        # ----------------------------------------------------------------------
        # Columna Izquierda (20x20x500 mm en vertical Y)
        crear_perfil_prisma("Columna_Izquierda_2020_500mm", 
                           [0, 0, 0], [P_SZ, H_MARCO, 0], 'Z', P_SZ)
        
        # Columna Derecha (20x20x500 mm a X = 52 cm)
        crear_perfil_prisma("Columna_Derecha_2020_500mm", 
                           [P_SZ + W_INT, 0, 0], [W_EXT, H_MARCO, 0], 'Z', P_SZ)

        # Travesaño Superior Frontal (540 mm en horizontal X a Y = 50 cm)
        crear_perfil_prisma("Travesano_Superior_540mm", 
                           [0, H_MARCO, 0], [W_EXT, H_MARCO + P_SZ, 0], 'Z', P_SZ)

        # Travesaño Inferior Frontal (540 mm en horizontal X a Y = -2 cm)
        crear_perfil_prisma("Travesano_Inferior_540mm", 
                           [0, -P_SZ, 0], [W_EXT, 0, 0], 'Z', P_SZ)

        # ----------------------------------------------------------------------
        # 2. BATERÍA SUPERIOR DE 5 PERFILES LONGITUDINALES (600 mm de avance)
        # ----------------------------------------------------------------------
        sketchBat = rootComp.sketches.add(rootComp.xYConstructionPlane)
        for i in range(N_PERF):
            # Posición en X: distribuido simétricamente en el marco
            # Desde X = 3.0 cm hasta X = 51.0 cm con paso de 12 cm
            x_centro = (P_SZ + 1.0) + (i * PITCH)
            x0 = x_centro - (P_SZ / 2.0)
            x1 = x_centro + (P_SZ / 2.0)
            y0 = H_MARCO + P_SZ
            y1 = H_MARCO + (2.0 * P_SZ)

            sketchPerf = rootComp.sketches.add(rootComp.xYConstructionPlane)
            sketchPerf.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(x0, y0, 0),
                adsk.core.Point3D.create(x1, y1, 0)
            )
            # Extrusión hacia adelante en Z a 600 mm (60.0 cm)
            profB = sketchPerf.profiles.item(0)
            extInB = extrudes.createInput(profB, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extInB.setDistanceExtent(False, adsk.core.ValueInput.createByReal(L_BAT))
            featB = extrudes.add(extInB)
            b = featB.bodies.item(0)
            b.name = f"Bateria_Longitudinal_Perfil_{i+1}_600mm"

        # ----------------------------------------------------------------------
        # 3. EJE TRANSVERSAL GUÍA PARA EL CARRO MÓVIL GT2 (540 mm)
        # ----------------------------------------------------------------------
        # Situado a mitad de la batería (Z = 30 cm) apoyado sobre la bancada
        sketchGuia = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchGuia.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 30.0, 0),
            adsk.core.Point3D.create(W_EXT, 30.0 + P_SZ, 0)
        )
        profG = sketchGuia.profiles.item(0)
        extInG = extrudes.createInput(profG, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInG.setDistanceExtent(False, adsk.core.ValueInput.createByReal(P_SZ))
        featG = extrudes.add(extInG)
        bGuia = featG.bodies.item(0)
        bGuia.name = "Perfil_Transversal_Guia_Carro_GT2_540mm"

        # ----------------------------------------------------------------------
        # 4. SOPORTE DE MOTOR PASO A PASO NEMA 17 (EXTREMO DERECHO)
        # ----------------------------------------------------------------------
        sketchMotor = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchMotor.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(W_EXT - 4.2, 28.0, 0),
            adsk.core.Point3D.create(W_EXT + 1.0, 34.0, 0)
        )
        profM = sketchMotor.profiles.item(0)
        extInM = extrudes.createInput(profM, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInM.setDistanceExtent(False, adsk.core.ValueInput.createByReal(4.2))
        featM = extrudes.add(extInM)
        bMotor = featM.bodies.item(0)
        bMotor.name = "Soporte_y_Motor_NEMA17_GT2"

        # ----------------------------------------------------------------------
        # 5. SOPORTE TENSOR CON POLEA LOCA IDLER GT2 (EXTREMO IZQUIERDO)
        # ----------------------------------------------------------------------
        sketchIdler = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchIdler.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(-1.0, 28.5, 0),
            adsk.core.Point3D.create(3.5, 33.5, 0)
        )
        profI = sketchIdler.profiles.item(0)
        extInI = extrudes.createInput(profI, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInI.setDistanceExtent(False, adsk.core.ValueInput.createByReal(3.0))
        featI = extrudes.add(extInI)
        bIdler = featI.bodies.item(0)
        bIdler.name = "Soporte_Tensor_Polea_GT2"

        # ----------------------------------------------------------------------
        # 6. CARRO MÓVIL V-WHEEL CON BRIDA JOYSTICK Y OJAL PARA HILO CUBESAT
        # ----------------------------------------------------------------------
        # Centrado inicialmente en X = 27 cm (mitad del recorrido)
        sketchCarro = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchCarro.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(23.5, 27.5, 0),
            adsk.core.Point3D.create(30.5, 34.5, 0)
        )
        # Taladro pasante central de 4.5 mm (0.45 cm) para el hilo de suspensión
        centerHole = adsk.core.Point3D.create(27.0, 31.0, 0)
        sketchCarro.sketchCurves.sketchCircles.addByCenterRadius(centerHole, 0.225)

        profC = sketchCarro.profiles.item(0)
        extInC = extrudes.createInput(profC, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInC.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.5))
        featC = extrudes.add(extInC)
        bCarro = featC.bodies.item(0)
        bCarro.name = "Carro_Movil_VWheel_Gantry_Joystick"

        # Mensaje de confirmación en la UI de Fusion
        if ui:
            ui.messageBox(
                "¡Banco Mecatrónico TFG Generado Exitosamente con la API Oficial de Fusion 360!\n\n"
                "- Bastidor base: 540 x 500 mm (Perfil V-Slot 2020)\n"
                "- Batería superior: 5 perfiles longitudinales de 600 mm (paso 120 mm)\n"
                "- Eje transversal móvil de 540 mm con correa GT2\n"
                "- Soporte NEMA 17 y Tensor Idler en extremos\n"
                "- Carro móvil V-Wheel con soporte de sensor Joystick y ojal para CubeSat"
            )

    except:
        if ui:
            ui.messageBox('Error en el script de Fusion 360:\n{}'.format(traceback.format_exc()))

def stop(context):
    pass

