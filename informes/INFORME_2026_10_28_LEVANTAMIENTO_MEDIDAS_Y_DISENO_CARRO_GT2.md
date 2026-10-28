# 📑 Informe Técnico Profesional de Ingeniería - 28/10/2026 (En Progreso)

> **Proyecto:** Sistema Embebido de Control de Posición Bidireccional para Orientación de Prototipos Espaciales en Microgravedad Simulada  
> **Titulación:** Trabajo de Fin de Grado (TFG)  
> **Directorio de Trabajo Oficial:** [`DESARROLLO_TFG/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/)  
> **Fecha de Inicio de Sesión:** 28 de octubre de 2026  
> **Modalidad Documental:** Informe Vivo Continuo e Incremental (actualizado en tiempo real)  
> **Documento:** `INFORME_2026_10_28_LEVANTAMIENTO_MEDIDAS_Y_DISENO_CARRO_GT2.md`

---

## 1. Resumen Ejecutivo y Objetivos de la Sesión

En la sesión de trabajo del 28/10/2026 se han alcanzado los siguientes hitos de ingeniería:

1. **Recepción y Procesamiento del Levantamiento Métrico Real:**
   - Análisis visual y geométrico de las 8 imágenes reales y croquis manuscrito aportados por el usuario en el directorio [`fotos medidas/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/fotos%20medidas/).
   - Verificación de la sección de perfil de aluminio estructural: **V-Slot / T-Slot 2020** ($20\text{ mm} \times 20\text{ mm}$).
   - Determinación de las dimensiones nominales del portal base: altura de montantes $500\text{ mm}$, luz interior entre columnas $500\text{ mm}$, y ancho exterior total $540\text{ mm}$ con escuadras de fundición de aluminio de $90^\circ$.
2. **Definición de la Transmisión Cinemática del Carro Móvil Transversal:**
   - Especificación técnica solicitada por el usuario: accionamiento por **cinta síncrona tipo impresora 3D (Correa GT2)** mediante **motor paso a paso**, tanto para arrastrar la correa como para desplazar el carro que circulará a lo largo del perfil/varilla de la bancada superior.
3. **Actualización de Artefactos OpenSpec y Memoria Técnica:**
   - Actualización de [`design.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/openspec/changes/despliegue-satelites-joystick-esp32/design.md) y [`tasks.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/openspec/changes/despliegue-satelites-joystick-esp32/tasks.md) en la rama activa `change/despliegue-satelites-joystick-seguimiento`, superando la validación estricta con cero discrepancias.

---

## 2. Levantamiento Dimensional y Análisis Estructural

A partir de las imágenes de taller y el cuaderno de notas técnico (`28-10-26`), se tabulan los datos geométricos del bastidor:

| Elemento Estructural | Magnitud / Tipo | Valor Medido | Tolerancia / Observaciones |
| :--- | :--- | :--- | :--- |
| **Sección del Perfil** | Perfilería de aluminio ranurado | $20 \times 20\text{ mm}$ | Ranura estándar de $6\text{ mm}$ (serie 20) |
| **Montantes Verticales ($Z$)** | Longitud de corte de perfiles | $500\text{ mm}$ ($50\text{ cm}$) | 2 unidades idénticas |
| **Luz Horizontal Interior ($Y_{int}$)** | Distancia entre caras internas | $500\text{ mm}$ ($50\text{ cm}$) | Determina la carrera útil del carro |
| **Ancho Total Exterior ($Y_{ext}$)** | Extremo a extremo de la estructura | $540\text{ mm}$ ($54\text{ cm}$) | $20\text{ mm} + 500\text{ mm} + 20\text{ mm}$ |
| **Escuadras de Unión** | Escuadras triangulares de 90° | Fundición de aluminio | Fijación con tornillos y tuercas T M4/M5 |

```mermaid
flowchart TD
    subgraph Bastidor_Real_540x500["Bastidor Medido (Perfil 2020)"]
        Top["Perfil Superior (500 mm int / 540 mm ext)"]
        Left["Columna Izquierda (500 mm)"]
        Right["Columna Derecha (500 mm)"]
        Bottom["Perfil Inferior (500 mm int / 540 mm ext)"]
        Esc1["Escuadra 90°"]
        Esc2["Escuadra 90°"]
        Esc3["Escuadra 90°"]
        Esc4["Escuadra 90°"]

        Top --- Esc1 --- Left
        Top --- Esc2 --- Right
        Bottom --- Esc3 --- Left
        Bottom --- Esc4 --- Right
    end
```

---

## 3. Ingeniería de la Transmisión por Correa GT2 (Carro Transversal)

### 3.1. Selección de Componentes de la Transmisión
Siguiendo las directrices del usuario:
- **Correa Síncrona:** Tipo **GT2** de neopreno reforzado con fibra de vidrio ($2\text{ mm}$ de paso entre dientes, $6\text{ mm}$ de ancho de banda). Presenta perfil curvilíneo que elimina el juego angular y minimiza el estiramiento elástico.
- **Polea Motriz:** Polea GT2 de 20 dientes ($Z = 20$), diámetro primitivo:
  $$D_p = \frac{Z \cdot p}{\pi} = \frac{20 \cdot 2\text{ mm}}{\pi} \approx 12{,}73\text{ mm}$$
- **Avance Lineal por Revolución:**
  $$Avance = Z \cdot p = 20 \times 2\text{ mm} = 40\text{ mm/vuelta}$$
- **Actuador:** Motor paso a paso NEMA 17 (ángulo de paso $\alpha = 1{,}8^\circ \to 200\text{ pasos/rev}$).
- **Resolución Cinemática con Driver a 16 Micropasos:**
  $$\delta_y = \frac{40\text{ mm}}{200 \times 16} = \frac{40}{3200} = 0{,}0125\text{ mm/micropaso} \quad (12{,}5\,\mu\text{m})$$

### 3.2. Dinámica de Seguimiento del Péndulo
Para cancelar el balanceo pendular natural ($\omega_n = 4{,}0435\text{ rad/s}$, período $T_n \approx 1{,}5539\text{ s}$), el carro superior debe ser capaz de acelerar y alcanzar velocidades acordes a la velocidad tangencial máxima del satélite.

La velocidad lineal del carro transversal con el motor girando a $10\text{ rps}$ ($600\text{ rpm}$):
$$v_{max} = 10\text{ rev/s} \times 40\text{ mm/rev} = 400\text{ mm/s}$$

Esta velocidad supera ampliamente la velocidad máxima del péndulo para oscilaciones admisibles ($\le 0{,}5^\circ$), garantizando que el carro no sufra retraso de fase en el seguimiento servoguiado.

```mermaid
flowchart LR
    NEMA["Motor Paso a Paso (NEMA 17)"] -->|Eje 5 mm| Pulley["Polea GT2 20T (Dp = 12.73 mm)"]
    Pulley --> Belt["Correa GT2 (Paso 2 mm, Ancho 6 mm)"]
    Belt --> Clamp["Mordaza de Sujeción"]
    Clamp --> Carriage["Carro Móvil sobre Perfil 2020"]
    Idler["Polea Loca GT2 (Tensora)"] --- Belt
    Carriage --> Sensor["Soporte Joystick COTS + Ojal de Hilo"]
```

---

## 4. Decisiones de Diseño Aprobadas (Sesión 28/10/2026)

Tras la consulta formal, el usuario ha validado las siguientes especificaciones mecánicas:

1. **Guiado del Carrito Móvil (Opción A - Ruedas V-Wheel):**
   - El carro transversal se desplazará directamente sobre las ranuras en V del perfil de aluminio 2020 mediante ruedas **V-Wheel de POM** con rodamientos 625ZZ.
   - Incorporará tuercas espaciadoras excéntricas para eliminar cualquier holgura o juego mecánico en las pistas.
2. **Ubicación del Motor Paso a Paso Transversal:**
   - Montaje del motor paso a paso (NEMA 17) **fijo en el extremo lateral del perfil** mediante soporte estructural impreso en 3D / pletina de aluminio.
   - En el extremo opuesto se sitúa el tensor con polea loca idler GT2.
   - El carro móvil resulta ultraligero al no cargar el peso del motor, permitiendo mayores aceleraciones y una respuesta dinámica óptima para el lazo servoguiado.
3. **Batería Superior de Avance Longitudinal:**
   - Estructura superior formada por una **batería de 5 perfiles de aluminio paralelos**.
   - Longitud nominal seleccionada: **$600\text{ mm}$** (superior a los $500\text{ mm}$ del marco base para proporcionar mayor carrera útil de eyección).
   - **Distribución geométrica transversal:**  
     Para una luz interior de $500\text{ mm}$, distribuyendo los 5 perfiles de $20\text{ mm}$:
     $$\text{Espaciado entre centros} = \frac{500\text{ mm} - 20\text{ mm}}{5 - 1} = \frac{480\text{ mm}}{4} = 120\text{ mm}$$
     Se obtienen 4 vanos de $100\text{ mm}$ libres entre caras de perfiles y $120\text{ mm}$ entre ejes, garantizando un emparrillado simétrico de gran rigidez torsional.

```mermaid
flowchart TD
    subgraph Parrilla_Superior["Batería Superior (5 Perfiles de 600 mm - Espaciado 120 mm)"]
        P1["Perfil Longitudinal 1 (x = 0 mm)"]
        P2["Perfil Longitudinal 2 (x = 120 mm)"]
        P3["Perfil Longitudinal 3 (x = 240 mm - Centro)"]
        P4["Perfil Longitudinal 4 (x = 360 mm)"]
        P5["Perfil Longitudinal 5 (x = 480 mm)"]
    end
    MarcoBase["Marco Frontal 540x500 mm"] --- Parrilla_Superior
    Parrilla_Superior --> PuenteTransversal["Eje Transversal (Perfil 2020 con Correa GT2)"]
    PuenteTransversal --> CarroVWheel["Carro V-Wheel (Ruedas POM + Sensor Joystick)"]
```

---

## 5. Estado de los Módulos y Próximos Pasos Inmediatos

1. **Modelado CAD en Fusion 360:**
   - Incorporar en el ensamblaje superior la batería de 5 perfiles longitudinales de $600\text{ mm}$ apoyados sobre el pórtico de $540\text{ mm}$ con separación entre centros de $120\text{ mm}$.
   - Modelar el soporte para el motor NEMA 17 en el extremo del perfil transversal.
   - Modelar el soporte de la polea tensora GT2 en el extremo opuesto.
   - Diseñar la placa del carro deslizante con ruedas V-Wheel, mordazas de correa y anclaje desacoplado del joystick COTS.
2. **Generación de Archivos Paramétricos y Scripts:**
   - Generar el script Python para Fusion 360 / archivos OpenSCAD para fabricar los soportes en impresión 3D FDM con tolerancias ensayadas (+0.35 mm pasantes, +0.15 mm rodamientos).
3. **Firmware ESP32:**
   - Implementar el lazo de control servoguiado en el microcontrolador ESP32 para excitar el driver del motor NEMA 17 a partir de las tensiones analógicas del joystick.
