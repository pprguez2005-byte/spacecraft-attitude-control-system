# 📑 Informe Técnico Profesional de Ingeniería - 03/11/2026 (En Progreso)

> **Proyecto:** Sistema Embebido de Control de Posición Bidireccional para Orientación de Prototipos Espaciales en Microgravedad Simulada  
> **Titulación:** Trabajo de Fin de Grado (TFG)  
> **Directorio de Trabajo Oficial:** [`DESARROLLO_TFG/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/)  
> **Fecha de Inicio de Sesión:** 3 de noviembre de 2026  
> **Modalidad Documental:** Informe Vivo Continuo e Incremental (actualizado en tiempo real)  
> **Documento:** `INFORME_2026_11_03_DISENO_TRANSMISION_MOTOR_ESP32.md`

---

## 1. Resumen Ejecutivo y Objetivos de la Sesión

En la sesión del 03/11/2026 se aborda el subsistema mecatrónico de tracción y control embebido:
1. **Definición del Accionamiento Bidireccional:** Carro guiado por correa GT2 sobre perfil 2020 accionado por motor paso a paso con inversión de giro horario/antihorario (CW/CCW).
2. **Selección del Driver de Potencia:** Evaluación técnica comparativa entre TMC2209, TMC2208, A4988 y DRV8825 frente a la excitación modal del péndulo ($f_n = 0{,}6435\text{ Hz}$).
3. **Cálculo y Parametrización del Tren de Engranajes en Autodesk Fusion 360:**
   - Corrección de la anomalía de escala imperial en la utilidad *Spur Gear* de Fusion 360 (módulo por defecto $12{,}70\text{ mm} \to D_p = 304{,}8\text{ mm}$).
   - Dimensionamiento formal de engranajes rectos de evolvente para eje de motor NEMA 17 ($\varnothing 5\text{ mm}$) y transmisión hacia el eje de la correa.
   - Distinción funcional crítica entre engranaje recto (involute spur gear) y polea síncrona curvilínea GT2.

---

## 2. Parámetros de Diseño de Engranajes Rectos en Fusion 360

### 2.1. Corrección Dimensional
El valor por defecto de Fusion 360 (`Module = 12.70 mm`) corresponde a la conversión de $0{,}5\text{ pulg}$, generando un diámetro primitivo de $304{,}8\text{ mm}$ inviable para un banco de $500\text{ mm}$.

Para fabricación aditiva (FDM) y acoplamiento con NEMA 17:
* **Módulo recomendado:** $m = 1{,}0\text{ mm}$ (dientes finos) o $m = 1{,}5\text{ mm}$ (dientes reforzados para impresión 3D).
* **Diámetro de eje (Hole Dia.):** $\varnothing 5{,}00\text{ mm}$ (eje de NEMA 17).
* **Juego entre dientes (Backlash):** $0{,}20\text{ mm}$ a $0{,}25\text{ mm}$ para compensar la expansión térmica del filamento PLA/PETG.

### 2.2. Opciones de Relación de Transmisión

$$\text{Diámetro Primitivo } D_p = m \cdot Z, \quad \text{Distancia entre centros } a = \frac{D_{p1} + D_{p2}}{2}$$

* **Relación 1:1 ($Z_1 = 20, Z_2 = 20$, $m = 1{,}0\text{ mm}$):**
  - $D_{p1} = 20\text{ mm}$, $D_{p2} = 20\text{ mm}$, $a = 20\text{ mm}$ (coincide con el ancho del perfil 2020).
* **Relación 2:1 ($Z_1 = 16, Z_2 = 32$, $m = 1{,}0\text{ mm}$):**
  - $D_{p1} = 16\text{ mm}$, $D_{p2} = 32\text{ mm}$, $a = 24\text{ mm}$. Duplica el par disponible.

---

## 3. Dinámica Cinemática y Par para Velocidad Lineal de 0,5 m/s

### 3.1. Estimación del Motor y Cinemática
* **Motor base estimado:** NEMA 17 estándar (42x42 mm, ej. 17HS4401).
  - Par de retención nominal ($T_H$): $\approx 0{,}40 - 0{,}45\text{ N}\cdot\text{m}$ ($40 - 45\text{ N}\cdot\text{cm}$).
  - Corriente: $1{,}2 - 1{,}5\text{ A}$.
  - Ángulo de paso: $1{,}8^\circ$ (200 pasos/rev).
* **Polea GT2 de 20 dientes ($Z = 20$, paso $p = 2\text{ mm}$):**
  - Avance lineal por revolución:
    $$Avance = 20 \times 2\text{ mm} = 40\text{ mm/vuelta} = 0{,}04\text{ m/vuelta}$$
  - Régimen de giro de la polea para $v = 0{,}5\text{ m/s}$ ($500\text{ mm/s}$):
    $$n = \frac{500\text{ mm/s}}{40\text{ mm/vuelta}} = 12{,}5\text{ rev/s} = 750\text{ rpm}$$

### 3.2. Verificación Dinámica del Par Requerido
* **Masa móvil del carro:** $m_{carro} \approx 0{,}25\text{ kg}$ (ruedas POM, gantry plate, sensor).
* **Aceleración requerida:** $a = 2{,}0\text{ m/s}^2$ ($t_{acc} = 0{,}25\text{ s}$, distancia de rampa $s = 62{,}5\text{ mm}$).
* **Fuerza total sobre la correa:**
  $$F_{total} = m_{carro} \cdot a + F_{friccion} \approx (0{,}25 \times 2{,}0) + 3{,}0\text{ N} \approx 3{,}5\text{ N}$$
* **Par resistente en el eje de la polea ($D_p = 12{,}73\text{ mm}$, radio $R = 0{,}00637\text{ m}$):**
  $$\tau_{resistente} = F_{total} \cdot R = 3{,}5\text{ N} \times 0{,}00637\text{ m} \approx 0{,}022\text{ N}\cdot\text{m} \quad (2{,}2\text{ N}\cdot\text{cm})$$

### 3.3. Conclusión de Diseño: Selección de Relación 1:1
* A $750\text{ rpm}$, un NEMA 17 alimentado a 12V/24V entrega aproximadamente $0{,}10 - 0{,}16\text{ N}\cdot\text{m}$, muy superior a los $0{,}022\text{ N}\cdot\text{m}$ requeridos (factor de seguridad $> 4$).
* **Prohibición de reductores reductores ($> 1:1$):** Si se utilizara una reducción $2:1$, el motor tendría que girar a $1500\text{ rpm}$, entrando en zona de pérdida de par y *stalling*.
* **Decisión:** Relación directa **1:1** ($Z_1 = 20, Z_2 = 20, m = 1{,}0\text{ mm}$) para operar a $750\text{ rpm}$ y frecuencia de pulsos en ESP32 de $40\text{ kHz}$ a 16 micropasos.

---

## 4. Parámetros Finales Consolidados en Autodesk Fusion 360

Tras el cálculo dinámico y la validación con el usuario, se fijan los parámetros en la herramienta *Spur Gear*:

| Parámetro | Valor Piñón 1 (Motor) | Valor Rueda 2 (Eje Correa) | Justificación de Ingeniería |
| :--- | :---: | :---: | :--- |
| **Standard** | `Metric` | `Metric` | Sistema métrico internacional. |
| **Pressure Angle** | `20 deg` | `20 deg` | Ángulo de presión industrial estándar (mayor rigidez de base). |
| **Module ($m$)** | `1.00 mm` | `1.00 mm` | Tamaño ideal de diente para FDM con boquilla de $0{,}4\text{ mm}$. |
| **Number of Teeth ($Z$)** | `20` | `20` | Relación 1:1, diámetro primitivo $D_p = 20{,}0\text{ mm}$. |
| **Backlash** | `0.20 mm` | `0.20 mm` | Holgura entre flancos para evitar trabado por dilatación térmica en FDM. |
| **Root Fillet Radius** | `0.30 mm` | `0.30 mm` | Alivio de tensiones en el fondo del diente ($0{,}3 \cdot m$). |
| **Gear Thickness ($b$)** | **`7.00 mm`** | **`7.00 mm`** | Espesor adoptado por el usuario: óptimo para anclaje a eje y resistencia a flexión. |
| **Hole Diameter** | `5.00 mm` | `5.00 mm` (o según eje) | Ajuste nominal con eje motor NEMA 17 ($\varnothing 5\text{ mm}$). |
| **Distancia entre centros ($a$)** | **`20.00 mm`** | **`20.00 mm`** | $a = (D_{p1} + D_{p2}) / 2 = 20\text{ mm}$ (enrasado con ranura perfil 2020). |

---

## 5. Automatización de Modelado 3D de la Correa GT2 Sólida

Para resolver las dificultades de contornos no cerrados en la interfaz gráfica de Fusion 360, se ha programado e integrado un script de generación paramétrica automatizada:
1. **Script Oficial de Fusion 360 ([`APPDATA/.../API/Scripts/GenerarCorreaGT2/GenerarCorreaGT2.py`](file:///C:/Users/Usuario/AppData/Roaming/Autodesk/Autodesk%20Fusion%20360/API/Scripts/GenerarCorreaGT2/GenerarCorreaGT2.py)):**
   - Construcción de curvas semicirculares y rectas tangentes mediante `arcs.addByThreePoints` y `lines.addByTwoPoints` garantizando coincidencia estricta y perfil estanco sin holguras.
   - Extrusión automática del perfil anular cerrado con espesor $1{,}40\text{ mm}$ y ancho $6{,}00\text{ mm}$ en el plano frontal del bastidor.
   - Acceso instantáneo en Fusion 360 mediante el atajo `Shift + S`.
2. **Modelo 3D Exportado ([`Fusion/Correa_GT2_Solida.obj`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion/Correa_GT2_Solida.obj)):**
   - Geometría mallada 1:1 de la correa cerrada completa lista para inserción directa en el espacio de trabajo.

---

## 6. Próximos Pasos Inmediatos
1. Modelado o ensamblado del soporte bi-eje (distancia entre centros $20\text{ mm}$) para motor NEMA 17 y eje secundario con polea GT2.
2. Definición del patillaje GPIO en el ESP32 Super Mini para control `STEP`, `DIR` y `ENABLE` hacia el driver TMC2209.
3. Desarrollo del firmware modular no bloqueante en `ESP32/` para generar las rampas de aceleración suaves hasta $500\text{ mm/s}$.



