// ==============================================================================
// TFG: BANCO MECATRÓNICO DE MICROGRAVEDAD SIMULADA
// Componente: Soporte Tensor para Polea Loca (Idler GT2) en Perfil 2020
// Aplicación: Extremo de retorno y tensado de la correa del Carro Transversal
// Diseñado para: Fabricación Aditiva FDM (PLA/PETG/ABS)
// ==============================================================================

$fn = 60;

// Parámetros de la polea y perfil
profile_width    = 20.0;
wall_thick       = 4.5;
idler_slot_len   = 16.0;  // Longitud de corredera para regular la tensión de la correa
m5_pass_dia      = 5.4;   // Para eje de la polea loca GT2 (5 mm)
m5_mount_dia     = 5.4;   // Para fijación a ranura de perfil 2020 con tuerca T
body_length      = 40.0;
body_height      = 28.0;
pulley_gap       = 12.0;  // Hueco para alojar la polea GT2 con rodamientos

module soporte_tensor_idler() {
    difference() {
        // Bloque en forma de U / horquilla
        cube([profile_width + 2 * wall_thick, body_length, body_height]);

        // Vaciado central para la polea loca y el paso de la correa
        translate([wall_thick, -1, wall_thick])
            cube([profile_width, body_length - wall_thick + 1, body_height]);

        // Ranuras de corredera lateral para el eje M5 de la polea tensora
        for (side = [-1, 1]) {
            translate([side > 0 ? profile_width + wall_thick - 1 : -1, body_length/2 - idler_slot_len/2, body_height/2]) {
                rotate([0, 90, 0]) {
                    hull() {
                        cylinder(d = m5_pass_dia, h = wall_thick + 2);
                        translate([0, idler_slot_len, 0])
                            cylinder(d = m5_pass_dia, h = wall_thick + 2);
                    }
                }
            }
        }

        // Taladros M5 en la base inferior para fijar rígidamente al perfil 2020
        translate([(profile_width + 2*wall_thick)/2, 10.0, -1])
            cylinder(d = m5_mount_dia, h = wall_thick + 2);
            
        translate([(profile_width + 2*wall_thick)/2, 28.0, -1])
            cylinder(d = m5_mount_dia, h = wall_thick + 2);
    }
}

soporte_tensor_idler();
