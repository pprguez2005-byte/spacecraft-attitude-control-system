# Spec Delta: Detección Angular de Hilo con Joystick COTS

## Purpose

Permite capturar en tiempo real la inclinación angular bidireccional del hilo de suspensión respecto a la vertical mediante un joystick comercial COTS conectado al microcontrolador ESP32.

## ADDED Requirements

### Requirement: Adquisición de Señal Biaxial de Inclinación
El sistema SHALL adquirir de forma continua mediante las entradas analógicas ADC del ESP32 las dos tensiones de salida ($V_x$, $V_y$) del joystick comercial correspondientes a las desviaciones angulares ($\theta_x$, $\theta_y$) del hilo.

#### Scenario: Lectura en reposo vertical
- **WHEN** el hilo de suspensión se encuentra exactamente a 90 grados respecto a la horizontal ($\theta = 0^\circ$)
- **THEN** el ESP32 digitaliza los valores de tensión nominal de centrado y reporta desviación nula $\theta_x = 0^\circ, \theta_y = 0^\circ$ dentro del margen de tolerancia de calibración

#### Scenario: Deflexión angular del hilo por avance del satélite
- **WHEN** el panel o satélite se desplaza provocando una inclinación del hilo superior al umbral mínimo
- **THEN** el ESP32 calcula el ángulo instantáneo en grados y lo pone a disposición del lazo de control de seguimiento

### Requirement: Calibración y Compensación de Cero
El sistema SHALL permitir la calibración del punto cero vertical en el inicio del ensayo para compensar tolerancias de montaje o desalineaciones del joystick COTS.

#### Scenario: Procedimiento de puesta a cero
- **WHEN** se ejecuta la rutina de calibración con el hilo estático y en reposo
- **THEN** el ESP32 registra el offset de ambos canales analógicos y lo sustrae en las lecturas posteriores
