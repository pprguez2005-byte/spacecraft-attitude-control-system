# Propuesta: Sistema de Seguimiento Servoguiado y Batería de Perfiles para Simulación de Despliegue de Satélites tipo SpaceX

## Por qué (Why)

Para emular fielmente el entorno espacial y las condiciones de microgravedad durante la maniobra de eyección/despliegue de una columna de satélites planos (arquitectura similar al despliegue de paneles de satélites Starlink de SpaceX), es necesario que el punto de sujeción superior en la cámara acompañe activamente el movimiento cinemático del satélite en dos ejes espaciales (longitudinal y transversal). 

Al avanzar y desplegarse los paneles suspendidos por el hilo, este tiende a desviarse de la vertical ($90^\circ$ respecto a la horizontal), introduciendo fuerzas restauradoras pendulares indeseadas. Para neutralizar este ángulo en tiempo real y permitir un ensayo de gravedad nula planar representativo, se requiere:
1. Un sensor de inclinación en 2 ejes tipo joystick comercial COTS (sin muelles de centrado o con desacoplo de carga) leído por un microcontrolador ESP32.
2. Una estructura superior compuesta por una batería de perfiles de aluminio motorizados que avancen hacia delante coordinados con la suelta de los paneles.
3. Un carro móvil con un motor pequeño que circule de izquierda a derecha (eje transversal) a través del perfil para compensar el segundo eje de movimiento.

## Qué Cambia (What Changes)

- **Incorporación de Sensor COTS de Ángulo de Hilo:** Adquisición e integración de un joystick comercial de 2 ejes (gimbal / palanca de bajo rozamiento sin muelles de retorno) para medir la desviación angular ($\theta_x, \theta_y$) del hilo de suspensión sin soportar el peso axial del satélite.
- **Nodo de Telemetría y Control ESP32:** Integración del ESP32 para digitalización de las señales analógicas del joystick, cálculo del ángulo de inclinación y generación de consignas de seguimiento hacia los actuadores.
- **Extensión del Modelo CAD en Fusion 360:** Evolución del pórtico rectangular actual (`Ensamblaje_TFG.f3z`) para incorporar en la parte superior una batería de perfiles de guiado longitudinal y el carro motorizado transversal.
- **Actuación Biaxial Superior:**
  - Eje longitudinal (avance hacia adelante): motores de tracción para el avance de la batería de perfiles acompañando la columna de paneles.
  - Eje transversal (izquierda a derecha): micromotor/carro motorizado que circula a lo largo del perfil para anular la componente lateral del hilo.

## Capacidades (Capabilities)

### Nuevas Capacidades (New Capabilities)

- `deteccion-angular-hilo-joystick`: Captura y procesamiento en el ESP32 de la inclinación biaxial ($\theta_x, \theta_y$) del hilo de suspensión mediante joystick COTS.
- `bateria-perfiles-avance-longitudinal`: Diseño y dimensionamiento de la bancada superior de perfiles paralelos y sistema de tracción para avance sincronizado con la eyección de satélites.
- `carro-transversal-seguimiento`: Mecanismo de guiado y motorización del carro móvil transversal que porta el sensor de hilo para el centrado lateral.

### Capacidades Modificadas (Modified Capabilities)
*(Ninguna; es el primer conjunto formal de capacidades del banco de ensayos en OpenSpec).*

## Impacto (Impact)

- **CAD / Mecánica (`Fusion/`):** Modificación del ensamblaje marco para alojar la batería superior de perfiles 2020/2040, soportes de motor y carro transversal guiado.
- **Firmware / Electrónica (`ESP32/`):** Desarrollo del firmware de adquisición ADC para los ejes del joystick y generación de señales de control de motores (paso a paso o servo/DC según definición).
- **Control y Cinemática:** Algoritmo de control en bucle cerrado (control servoguiado $\theta \to 0$) para anular perturbaciones pendulares en microgravedad simulada.
