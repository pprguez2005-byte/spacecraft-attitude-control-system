# Diseño Técnico: Sistema Mecatrónico de Despliegue y Seguimiento Angular con Joystick y ESP32

## Contexto

Ver motivación y objetivos funcionales en [`proposal.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/openspec/changes/despliegue-satelites-joystick-esp32/proposal.md).
El modelo mecánico actual en Autodesk Fusion 360 ([`Ensamblaje_TFG.f3z`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/Fusion/Ensamblaje_TFG.f3z)) consta de un único marco vertical cerrado formado por perfiles de aluminio V-Slot/T-Slot (dimensiones base según modelo). Para emular la eyección secuencial de paneles/satélites en despliegue espacial tipo SpaceX, la estructura superior debe evolucionar a un puente/batería de perfiles bidireccional cartesianos gobernados por un microcontrolador ESP32.

---

## Objetivos / No Objetivos (Goals / Non-Goals)

**Objetivos:**
- Diseñar la arquitectura mecatrónica de la bancada superior en Fusion 360 incorporando:
  1. Una batería de perfiles longitudinales en la parte superior que avancen coordinados con la suelta de paneles.
  2. Un carro transversal compacto con micromotor que se mueva de izquierda a derecha a lo largo del perfil.
- Implementar en el ESP32 la adquisición continua del sensor joystick comercial COTS para medir la deflexión angular ($\theta_x, \theta_y$) del hilo de sujeción.
- Asegurar el desacoplo estructural de carga para que el peso del satélite ($m_s = 0{,}35\text{ kg}$, $P \approx 3{,}43\text{ N}$) no dañe ni sobrecargue los pivotes del joystick comercial.

**No Objetivos:**
- Modificar el diseño aerodinámico o estructural interno del CubeSat.
- Sustituir la electrónica principal de potencia del banco sin antes consensuar interfaces eléctricas y drivers.

---

## Fundamento Físico y Matemático del Control

```mermaid
flowchart LR
    A["Desplazamiento Panel / Satélite"] -->|Provoca inclinación| B["Ángulo del Hilo theta_x, theta_y"]
    B -->|Palanca sin muelle| C["Joystick COTS (Tensiones Vx, Vy)"]
    C -->|Muestreo ADC| D["ESP32 (Cálculo de error de ángulo)"]
    D -->|Lazo de Control e = theta| E["Controlador Servoguiado"]
    E -->|Pulsos Motor Avance| F["Batería de Perfiles (Avance X)"]
    E -->|Pulsos Motor Lateral| G["Carro Transversal (Eje Y)"]
    F -.->|Compensa theta_x -> 0| B
    G -.->|Compensa theta_y -> 0| B
```

### Relación Cinemática y Fuerza Perturbadora
Si el satélite se desplaza respecto a la vertical una distancia $\Delta x$, con una longitud de cable $L = 0{,}60\text{ m}$:
$$\sin\theta \approx \theta = \frac{x_{sat} - x_{carro}}{L}$$

La fuerza perturbadora en el plano horizontal es:
$$F_x = m_s g \sin\theta \approx m_s g \cdot \frac{x_{sat} - x_{carro}}{L}$$

Para mantener la microgravedad emulada sin aceleraciones ficticias ($F_x \to 0$), la ley de control busca hacer $x_{carro} = x_{sat}$, anulando el error angular:
$$e(t) = \theta(t) \to 0$$

---

## Decisiones de Diseño

### Decisión 1: Joystick Comercial COTS de Bajo Rozamiento
- **Opción seleccionada:** Módulo joystick comercial analógico COTS (o gimbal miniatura de 2 ejes).
- **Justificación:** Rapidez de integración y bajo coste.
- **Detalle de integración:** Para evitar que la fuerza del muelle de retorno falsee la caída del hilo ($F_{muelle} \gg F_{hilo}$), se retirará el muelle interno de centrado o se utilizará un gimbal tipo radiocontrol con tornillo de ajuste de fricción a cero.
- **Alternativas consideradas:**
  - Mecanismo 3D propio con rodamientos y sensores magnéticos AS5600 (descartado temporalmente por preferencia del usuario de comprarlo comercial).

### Decisión 2: Desacoplo Mecánico de Carga del Cable
- **Solución:** El hilo no cuelga de la palanca del joystick. El hilo se fija rígidamente a una pieza estructural del carro transversal. Inmediatamente debajo, el hilo atraviesa un anillo/ojal solidario a la palanca del joystick. Al inclinarse el hilo, empuja suavemente el anillo sin transferir tracción axial.

### Decisión 3: Arquitectura de la Batería Superior en Fusion 360
- **Estructura:** Sobre el marco vertical existente, se añaden 2 o más perfiles longitudinales superiores (batería de perfiles) en voladizo o sustentados en pórtico, sirviendo de raíles guía para el avance sincronizado con la eyección de satélites.
- **Carro transversal:** Carro rodante sobre ruedas V-wheel o guía lineal con micromotor acoplado por polea/correa o cremallera para el movimiento izquierda-derecha.

---

## Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
| :--- | :--- | :--- |
| **Zona muerta o fricción en el joystick COTS** | El carro no detecta inclinaciones muy leves ($< 0{,}2^\circ$) | Calibrar filtrado paso bajo en ESP32 y seleccionar joystick con potenciómetros lineales de baja resistencia mecánica o efecto Hall |
| **Pérdida de pasos en el motor transversal** | Desalineación del carro | Incluir finales de carrera de referencia (*homing*) en los extremos del perfil |
| **Flexión de los perfiles en voladizo** | Desviación del plano horizontal | Escuadras trianguladas de refuerzo en los nodos de unión con el marco |

---

## ⏸️ Estado: Proceso Pausado por el Usuario (Cuestionario Pendiente)

> **Nota de activación:** Este proceso queda formalmente suspendido hasta que el usuario indique reactivarlo con la orden: *"seguir con el proceso de los perfiles de fusion"* (o similar).  
> A continuación se preservan las preguntas técnicas pendientes para definir dimensiones exactas y componentes:

### 1. Dimensiones Mecánicas para Fusion 360
1. **Longitud de los perfiles de la batería superior:**  
   ¿De qué longitud deben ser los perfiles que avanzan hacia adelante? (Ej. $500\text{ mm}$, $600\text{ mm}$, $800\text{ mm}$ u otra medida según la carrera de eyección).
2. **Tipo y sección de perfil de aluminio:**  
   ¿Se utiliza perfil V-Slot/T-Slot **2020** ($20\times 20\text{ mm}$) o **2040** ($20\times 40\text{ mm}$)?
3. **Número de perfiles en la batería superior:**  
   ¿Cuántos perfiles paralelos conformarán el conjunto superior? (¿2 perfiles formando un raíl de soporte, 3, o una parrilla mayor?).

### 2. Selección del Joystick Comercial COTS
- **Opción A (Recomendada comercial):** Gimbal miniatura de Efecto Hall (tipo FrSky M9 / RadioMaster). Rodamientos de bolas, fricción nula, muelles desacoplables con tornillo sin abrir la carcasa.
- **Opción B:** Módulo joystick analógico clásico tipo Arduino / KY-023. Requiere retirar el muelle manualmente.
- Modelo exacto adquirido o previsto por el usuario.

### 3. Motorización y Transmisión
1. **Motor de avance longitudinal:** ¿Tipo de motor para el avance hacia delante de la batería de perfiles? (NEMA 17 con correa GT2, husillo T8...).
2. **Micromotor del carro transversal (izquierda a derecha):** ¿Tipo de motor para el carrito móvil que circula a lo largo del perfil? (NEMA 14/17 compacto, micromotorreductor N20 con encoder, servo/paso a paso 28BYJ-48).
3. **Tipo de transmisión transversal:** ¿Motor montado en el carro moviéndose por tracción en correa/cremallera, o fijo en un extremo del perfil tirando del carro con poleas?

### 4. Columna de Paneles (Satélites SpaceX)
- ¿Cuántos paneles forman la columna y cuál es la masa total aproximada suspendida del hilo?

