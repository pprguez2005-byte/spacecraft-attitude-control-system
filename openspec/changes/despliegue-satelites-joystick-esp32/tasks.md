# Tareas (Tasks): Implementación del Sistema de Despliegue y Seguimiento con Joystick y ESP32

## 1. Selección de Componentes y Firmware ESP32

- [ ] 1.1 Especificar el modelo comercial COTS de joystick/gimbal analógico y definir el conexionado con los pines ADC del ESP32 Super Mini
- [ ] 1.2 Desarrollar el firmware en `ESP32/` para lectura continua, filtrado por software y calibración de offset del punto vertical nulo ($\theta_x = 0, \theta_y = 0$)
- [ ] 1.3 Implementar en el ESP32 el lazo de control servoguiado para generar las consignas de velocidad/paso hacia los motores de los ejes longitudinal y transversal

## 2. Modelado Mecánico y Batería de Perfiles en Fusion 360

- [ ] 2.1 Acordar con el usuario las medidas dimensionales de la cámara: longitud longitudinal de avance, ancho transversal y separación entre perfiles de la batería
- [ ] 2.2 Extender el modelo de Fusion 360 (`Ensamblaje_TFG`) incorporando la batería de perfiles superiores y escuadras estructurales de anclaje
- [ ] 2.3 Diseñar el carro transversal móvil (eje izquierda-derecha) con acoplamiento para el micromotor y soporte de desacoplo de carga para el sensor joystick

## 3. Integración, Pruebas y Documentación

- [ ] 3.1 Validar la simulación cinemática del movimiento combinado (avance de paneles + centrado lateral de hilo)
- [ ] 3.2 Generar el informe profesional diario de ingeniería en `informes/INFORME_2026_10_27.md` con esquemas, cálculos dinámicos y avances para la memoria del TFG
