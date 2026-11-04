// ==============================================================================
// TFG: BANCO MECATRÓNICO DE MICROGRAVEDAD SIMULADA
// Componente: Soporte de Motor Paso a Paso NEMA 17 para Extremo de Perfil 2020
// Aplicación: Transmisión por Correa GT2 del Carro Transversal
// Diseñado para: Fabricación Aditiva FDM (PLA/PETG/ABS) con DFAM
// ==============================================================================

$fn = 60;

// --- Parámetros Motor NEMA 17 ---
nema_side        = 42.3;  // Ancho nominal NEMA 17 (mm)
nema_hole_pitch  = 31.0;  // Distancia entre centros de taladros M3 (mm)
nema_pilot_dia   = 23.0;  // Diámetro del resalte central (mm, con holgura)
m3_pass_dia      = 3.4;   // Taladro pasante M3 (+0.4 mm holgura)

// --- Parámetros Perfil V-Slot / T-Slot 2020 ---
profile_width    = 20.0;  // Ancho del perfil (mm)
m5_pass_dia      = 5.4;   // Taladro pasante M5 para tuerca T (+0.4 mm)
m5_head_dia      = 9.5;   // Alojamiento para cabeza de tornillo M5

// --- Parámetros del Soporte ---
wall_thick       = 5.0;   // Espesor estructural de paredes (mm)
flange_len       = 35.0;  // Longitud de las alas de sujeción al perfil (mm)
base_width       = nema_side + 4.0;
bracket_depth    = 45.0;  // Altura total del soporte

module soporte_motor_nema17() {
    difference() {
        union() {
            // Placa frontal de montaje del motor
            translate([-base_width/2, 0, 0])
                cube([base_width, wall_thick, bracket_depth]);
            
            // Alas de fijación laterales al perfil 2020 (en ángulo de 90°)
            translate([-profile_width/2, wall_thick, 0])
                cube([profile_width, flange_len, wall_thick]);
            
            // Cartelas de refuerzo triangulares para rigidez frente a la tensión de la correa
            translate([-base_width/2, wall_thick, 0])
                linear_extrude(height = bracket_depth)
                    polygon(points = [[0, 0], [4, 0], [0, flange_len * 0.7]]);
            
            translate([base_width/2 - 4, wall_thick, 0])
                linear_extrude(height = bracket_depth)
                    polygon(points = [[4, 0], [0, 0], [4, flange_len * 0.7]]);
        }

        // --- Taladros NEMA 17 en la placa vertical ---
        translate([0, wall_thick + 1, bracket_depth - nema_side/2]) {
            rotate([90, 0, 0]) {
                // Cuello central del motor
                cylinder(d = nema_pilot_dia, h = wall_thick + 2, center = true);
                
                // 4 taladros de fijación M3
                for (dx = [-nema_hole_pitch/2, nema_hole_pitch/2]) {
                    for (dz = [-nema_hole_pitch/2, nema_hole_pitch/2]) {
                        translate([dx, dz, 0])
                            cylinder(d = m3_pass_dia, h = wall_thick + 2, center = true);
                    }
                }
            }
        }

        // --- Taladros M5 de fijación a la ranura del perfil 2020 ---
        translate([0, wall_thick + flange_len/2, -1]) {
            cylinder(d = m5_pass_dia, h = wall_thick + 2);
            // Chaflán inferior
            cylinder(d1 = m5_head_dia, d2 = m5_pass_dia, h = 2.0);
        }
    }
}

soporte_motor_nema17();
