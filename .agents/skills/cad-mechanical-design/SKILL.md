---
name: cad-mechanical-design
description: Diseño mecánico, cálculo estructural y modelado paramétrico 3D para bancos de ensayo mecatrónicos y fabricación aditiva (impresión 3D FDM). Usar para diseñar carros de guiado, soportes de motores NEMA 17, acoplamientos de husillo T8, perfiles de aluminio 2020/2040, o generar scripts en OpenSCAD y FreeCAD.
---

# Skill: Diseño Mecánico y Fabricación Aditiva para Bancos Mecatrónicos

Esta habilidad proporciona directrices de ingeniería, reglas de dimensionamiento mecánico y plantillas paramétricas (OpenSCAD / FreeCAD) para el diseño del banco de ensayos cartesiano de 2 grados de libertad ($X$ y $Z$).

---

## 1. Arquitectura Mecánica del Banco de Ensayos

El banco cartesiano debe proporcionar alta rigidez estructural para evitar que las flexiones de la estructura introduzcan vibraciones en el punto de suspensión del satélite.

```
       +---------------------------------------------+
       |   Viga Superior (Perfil 2020/2040)          |
       +---------------------------------------------+
       |                                             |
[Columna Z1]     [Carro Horizontal X - Husillo T8] [Columna Z2]
(Perfil 2040)         [Soporte de Hilo]            (Perfil 2040)
       |                      |                      |
       |                   [Cable]                   |
       |                      |                      |
       |                 [🛰️ Prototipo]             |
       +---------------------------------------------+
       |             Base Inferior Rígida            |
       +---------------------------------------------+
```

### 1.1. Selección de Perfiles Estructurales y Cálculo de Flecha
- **Columnas verticales:** Se recomienda perfil de aluminio ranurado **2040** (sección $20 \times 40\text{ mm}$ orientada con el momento de inercia mayor en la dirección del movimiento del satélite).
- **Viga transversal horizontal:** Perfil **2020** o **2040** según la luz de trabajo ($L_{span}$).
- **Cálculo de flecha máxima en viga biapoyada:**
  $$\delta_{max} = \frac{F_{total} \cdot L_{span}^3}{48 \cdot E \cdot I_x}$$
  *Para aluminio 6063-T5 ($E \approx 69\text{ GPa}$) y luz de $500\text{ mm}$, la flecha para cargas inferiores a $2\text{ kg}$ es inferior a $0.05\text{ mm}$, garantizando alineación.*

### 1.2. Transmisión y Guiado Lineal
1. **Guiado Horizontal y Vertical:**
   - *Opción A (Ruedas V-Slot de policarbonato/POM con espaciadores excéntricos):* Económicas, silenciosas y autoalineables sobre las ranuras del perfil.
   - *Opción B (Guías lineales prismáticas MGN12 / MGN12H):* Rigidez superior, cero holgura angular y alta repetibilidad.
2. **Husillos Trapezoidales T8:**
   - **Paso recomendado:** T8x8 ($8\text{ mm}$ avance por vuelta) para buena velocidad horizontal; o T8x2 ($2\text{ mm}$ avance por vuelta) para el eje vertical $Z$ si se desea autobloqueo total frente a caída por gravedad.
   - **Tuerca Anti-Backlash:** Obligatoria. Dispone de dos cuerpos de latón o POM unidos por un resorte de compresión que elimina la holgura axial al invertir el giro del motor.
3. **Descarga Axial de Rodamientos:**
   - **Regla crítica:** Los rodamientos internos del motor NEMA 17 no están diseñados para soportar carga axial continua. El husillo vertical debe estar soportado por un soporte con rodamiento axial (ej. `KFL08` o `KP08`) en la base o parte superior.

---

## 2. Reglas de Diseño para Fabricación Aditiva (DFAM - FDM)

Al diseñar piezas para imprimir en 3D (PLA, PETG o ABS) que soporten motores, guías y husillos:

### 2.1. Tolerancias y Ajustes Dimensionales
| Tipo de Ajuste | Holgura Diametral Típica | Aplicación |
| :--- | :--- | :--- |
| **Ajuste Deslizante** | $+0.30\text{ mm}$ a $+0.40\text{ mm}$ | Pasantes para tornillos M3, M4, M5 sin rosca. |
| **Ajuste a Presión Ligera** | $+0.10\text{ mm}$ a $+0.15\text{ mm}$ | Alojamiento para rodamientos 608ZZ / 625ZZ. |
| **Insertos Roscados de Latón** | $-0.10\text{ mm}$ cónico | Insertos M3 (agujero $\approx 4.0\text{ mm}$ entrada, $3.8\text{ mm}$ fondo). |

### 2.2. Resistencia Mecánica y Orientación de Capas
- Las piezas impresas en FDM tienen comportamiento **ortótropo**: la unión entre capas (eje $Z$ de impresión) tiene entre un $40\%$ y un $60\%$ menos de resistencia a tracción que las líneas en el plano $XY$.
- **Regla:** Orientar siempre las piezas en la base de la impresora de modo que los esfuerzos principales de tracción y flexión queden paralelos a las capas, nunca perpendiculares a la línea de fractura.
- Emplear chaflanes de $45^\circ$ en las aristas inferiores en lugar de redondeos (*fillets*) para prevenir el efecto "pata de elefante" (*elephant's foot*).

---

## 3. Plantilla Paramétrica en OpenSCAD: Soporte para NEMA 17

Código de partida en OpenSCAD para generar un soporte estructural de motor NEMA 17 para anclar a perfil 2020:

```openscad
// ========================================================
// Soporte NEMA 17 paramétrico para perfil de aluminio 2020
// ========================================================
$fn = 60;

// Parámetros NEMA 17
nema_width = 42.3;
hole_spacing = 31.0;
center_hole_dia = 23.0;
m3_hole_dia = 3.4;
plate_thickness = 6.0;

// Parámetros Perfil 2020
vslot_spacing = 20.0;
m5_hole_dia = 5.4;

module mount_nema17() {
    difference() {
        // Bloque principal con rigidizadores
        cube([nema_width + 10, nema_width + 10, plate_thickness], center = true);
        
        // Agujero central para cuello y eje
        cylinder(d = center_hole_dia, h = plate_thickness + 2, center = true);
        
        // 4 taladros de fijación M3
        for (dx = [-hole_spacing/2, hole_spacing/2]) {
            for (dy = [-hole_spacing/2, hole_spacing/2]) {
                translate([dx, dy, 0])
                    cylinder(d = m3_hole_dia, h = plate_thickness + 2, center = true);
            }
        }
        
        // Taladros para tornillos M5 a tuercas T del perfil
        translate([-(nema_width/2 + 2), 0, 0])
            cylinder(d = m5_hole_dia, h = plate_thickness + 2, center = true);
        translate([(nema_width/2 + 2), 0, 0])
            cylinder(d = m5_hole_dia, h = plate_thickness + 2, center = true);
    }
}

mount_nema17();
```

---

## 4. Guía de Selección de Tornillería y Elementos Comerciales

- **Tornillería estándar:** Tornillos de cabeza cilíndrica con hexágono interior (DIN 912 / ISO 4762) en acero inoxidable A2 o clase 8.8 (M3 para motores y sensores; M4 y M5 para perfiles de aluminio).
- **Tuercas de inserción en ranura (T-Nuts):** Tuercas tipo "martillo" (*drop-in hammer nuts*) para perfiles serie 20 con rosca M4 o M5.
- **Acoplamiento motor-husillo:** Acoplador flexible de mordaza de aluminio (*plum / spider coupling*) de $5\text{ mm}$ a $8\text{ mm}$ con araña de poliuretano para amortiguar vibraciones angulares.
