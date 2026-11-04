# ==============================================================================
# Script de Automatización para Autodesk Fusion 360 (API Python)
# Proyecto: TFG - Banco Mecatrónico de Microgravedad Simulada
# Propósito: Modelado de la Batería Superior de 5 Perfiles de 600 mm y Eje Transversal
# Cómo ejecutar: En Fusion 360, presiona Shift + S -> Scripts -> Ejecutar este archivo
# ==============================================================================

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        
        if not design:
            ui.messageBox('No hay ningún diseño activo en Fusion 360.')
            return

        rootComp = design.rootComponent

        # Parámetros nominales en centímetros (Fusion API trabaja internamente en cm)
        profile_w_cm = 2.0         # 20 mm
        profile_len_cm = 60.0      # 600 mm (Longitud batería superior)
        rail_transverse_cm = 54.0  # 540 mm (Ancho transversal total del marco)
        num_perfiles = 5
        pitch_cm = 12.0            # 120 mm entre centros (48 cm / 4 vanos)
        start_x_cm = 0.0           # Posición inicial en X

        # Crear nuevo componente para la batería superior
        trans = adsk.core.Matrix3D.create()
        occGroup = rootComp.occurrences.addNewComponent(trans)
        compBateria = occGroup.component
        compBateria.name = "Bateria_5_Perfiles_Longitudinales_600mm"

        # 1. Crear los 5 perfiles longitudinales paralelos
        sketches = compBateria.sketches
        xyPlane = compBateria.xYConstructionPlane
        
        for i in range(num_perfiles):
            x_pos = start_x_cm + (i * pitch_cm)
            sketch = sketches.add(xyPlane)
            
            # Dibujar sección cuadrada del perfil 20x20
            p1 = adsk.core.Point3D.create(x_pos - profile_w_cm/2, -profile_w_cm/2, 0)
            p2 = adsk.core.Point3D.create(x_pos + profile_w_cm/2, profile_w_cm/2, 0)
            sketch.sketchCurves.sketchLines.addTwoPointRectangle(p1, p2)
            
            # Agujero central de aligeramiento / núcleo del perfil
            center_pt = adsk.core.Point3D.create(x_pos, 0, 0)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(center_pt, 0.25) # 5 mm diámetro

            # Extrusión longitudinal a 600 mm (eje Z hacia adelante)
            prof = sketch.profiles.item(0)
            extrudes = compBateria.features.extrudeFeatures
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            dist = adsk.core.ValueInput.createByReal(profile_len_cm)
            extInput.setDistanceExtent(False, dist)
            extFeature = extrudes.add(extInput)
            
            body = extFeature.bodies.item(0)
            body.name = f"Perfil_Longitudinal_2020_{i+1}_600mm"

        # 2. Crear el perfil transversal superior móvil (Guía del Carro GT2)
        sketchTrans = sketches.add(xyPlane)
        # Situado sobre los perfiles longitudinales en Y
        y_offset = profile_w_cm
        p_t1 = adsk.core.Point3D.create(-profile_w_cm, y_offset, 0)
        p_t2 = adsk.core.Point3D.create(-profile_w_cm + rail_transverse_cm, y_offset + profile_w_cm, 0)
        sketchTrans.sketchCurves.sketchLines.addTwoPointRectangle(p_t1, p_t2)
        
        profTrans = sketchTrans.profiles.item(0)
        extInputTrans = extrudes.createInput(profTrans, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distTrans = adsk.core.ValueInput.createByReal(profile_w_cm) # Sección 20x20
        extInputTrans.setDistanceExtent(False, distTrans)
        extFeatureTrans = extrudes.add(extInputTrans)
        bodyTrans = extFeatureTrans.bodies.item(0)
        bodyTrans.name = "Perfil_Guia_Carro_Transversal_GT2_540mm"

        ui.messageBox(f'¡Batería de {num_perfiles} perfiles de 600 mm y Eje Transversal generados con éxito en Fusion 360!')

    except:
        if ui:
            ui.messageBox('Fallo al ejecutar el script:\n{}'.format(traceback.format_exc()))
