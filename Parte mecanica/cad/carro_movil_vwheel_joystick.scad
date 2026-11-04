// ==============================================================================
// TFG: BANCO MECATRÓNICO DE MICROGRAVEDAD SIMULADA
// Componente: Carro Móvil Transversal V-Wheel con Fijación de Correa GT2
//              y Soporte de Desacoplo para Sensor Joystick COTS
// Diseñado para: Fabricación Aditiva FDM (PLA/PETG/ABS)
// ==============================================================================

$fn = 60;

// Dimensiones de la placa del carro (Gantry Plate)
plate_len        = 65.0;  // Longitud en el sentido del perfil (mm)
plate_width      = 65.0;  // Anchura vertical/transversal (mm)
plate_thick      = 5.0;   // Espesor base (mm)

// Espaciado entre ruedas V-Wheel para perfil 2020
wheel_spacing_x  = 44.0;  // Distancia horizontal entre ejes de ruedas (mm)
wheel_spacing_y  = 40.0;  // Distancia vertical entre ejes de ruedas V-Slot (mm)
m5_wheel_hole    = 5.2;   // Taladro para eje M5 de las ruedas V-Wheel
eccentric_hole   = 7.2;   // Taladro para espaciador excéntrico de ajuste de holgura

// Parámetros de fijación de la correa GT2
belt_slot_w      = 1.6;   // Ranura para el espesor de la correa GT2 (mm)
belt_slot_len    = 7.0;   // Ancho de la correa (6 mm + 1 mm holgura)
tooth_pitch      = 2.0;   // Paso GT2 (mm)

// Soporte inferior del sensor joystick COTS
joystick_pitch_x = 26.0;  // Distancia entre orificios de montaje joystick (mm)
joystick_pitch_y = 32.0;
m3_hole_dia      = 3.4;
wire_eyelet_dia  = 4.5;   // Ojal pasante central para el hilo de suspensión

module carro_movil_vwheel() {
    difference() {
        union() {
            // Placa principal del carro
            translate([-plate_len/2, -plate_width/2, 0])
                cube([plate_len, plate_width, plate_thick]);
            
            // Pletina inferior extendida para el soporte del sensor joystick
            translate([-plate_len/2, -plate_width/2 - 25.0, 0])
                cube([plate_len, 25.0, plate_thick]);
            
            // Nervios de refuerzo entre la placa principal y el soporte inferior
            translate([-plate_len/2 + 2, -plate_width/2 - 25.0, plate_thick])
                linear_extrude(height = 6.0)
                    polygon(points = [[0, 0], [4, 0], [0, 25]]);
                    
            translate([plate_len/2 - 6, -plate_width/2 - 25.0, plate_thick])
                linear_extrude(height = 6.0)
                    polygon(points = [[4, 0], [0, 0], [4, 25]]);
        }

        // --- 4 Orificios para Ruedas V-Wheel ---
        // Ruedas superiores (fijas, orificios M5 normales)
        translate([-wheel_spacing_x/2, wheel_spacing_y/2, -1])
            cylinder(d = m5_wheel_hole, h = plate_thick + 2);
        translate([wheel_spacing_x/2, wheel_spacing_y/2, -1])
            cylinder(d = m5_wheel_hole, h = plate_thick + 2);

        // Ruedas inferiores (con orificio para tuerca excéntrica de regulación)
        translate([-wheel_spacing_x/2, -wheel_spacing_y/2, -1])
            cylinder(d = eccentric_hole, h = plate_thick + 2);
        translate([wheel_spacing_x/2, -wheel_spacing_y/2, -1])
            cylinder(d = eccentric_hole, h = plate_thick + 2);

        // --- Mordazas para Sujeción de los Extremos de la Correa GT2 ---
        // Permiten introducir la correa plegada sobre sí misma con dientes enfrentados
        for (dx = [-plate_len/2 + 10, plate_len/2 - 10]) {
            translate([dx, 0, -1]) {
                cube([belt_slot_w, belt_slot_len, plate_thick + 2], center = true);
                // Dientes de anclaje antideslizante
                for (ty = [-2:2]) {
                    translate([0, ty * tooth_pitch, 0])
                        cylinder(d = 1.0, h = plate_thick + 2, center = true);
                }
            }
        }

        // --- Orificios de Montaje del Sensor Joystick COTS ---
        translate([0, -plate_width/2 - 12.5, 0]) {
            // Ojal central por donde pasa el hilo de suspensión sin rozar
            translate([0, 0, -1])
                cylinder(d = wire_eyelet_dia, h = plate_thick + 2);

            // 4 taladros M3 para atornillar el PCB del joystick
            for (jx = [-joystick_pitch_x/2, joystick_pitch_x/2]) {
                for (jy = [-joystick_pitch_y/2, joystick_pitch_y/2]) {
                    translate([jx, jy, -1])
                        cylinder(d = m3_hole_dia, h = plate_thick + 2);
                }
            }
        }

        // Chaflanes perimetrales para reducción de peso y DFAM
        translate([-plate_len/2, plate_width/2, -1])
            rotate([0, 0, 45])
                cube([10, 10, plate_thick + 2]);
        translate([plate_len/2, plate_width/2, -1])
            rotate([0, 0, 45])
                cube([10, 10, plate_thick + 2]);
    }
}

carro_movil_vwheel();
