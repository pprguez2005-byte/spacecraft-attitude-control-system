# Tareas (Tasks): Implementación del Sistema de Despliegue y Seguimiento con Joystick y ESP32

## 1. Selección de Componentes y Firmware ESP32

- [ ] 1.1 Especificar el modelo comercial COTS de joystick/gimbal analógico y definir el conexionado con los pines ADC del ESP32 Super Mini
- [ ] 1.2 Desarrollar el firmware en `ESP32/` para lectura continua, filtrado por software y calibración de offset del punto vertical nulo ($\theta_x = 0, \theta_y = 0$)
- [ ] 1.3 Implementar en el ESP32 el lazo de control servoguiado para generar las consignas de velocidad/paso hacia los motores de los ejes longitudinal y transversal

## 2. Modelado Mecánico, Transición a Autodesk Inventor y Ensamblajes

- [x] 2.1 Acordar con el usuario las medidas dimensionales de la cámara (perfil V-Slot 2020, marco 500x500 mm interior, 540 mm exterior y escuadras de 90°)
- [x] 2.2 Modelado de la batería de perfiles superiores de avance longitudinal (5 perfiles de 600 mm espaciados 120 mm)
- [x] 2.3 Diseñar el carro transversal móvil accionado por correa síncrona GT2 y motor paso a paso, con ruedas V-Wheel, mordazas de correa y soporte de desacoplo de carga para el sensor joystick
- [x] 2.4 Dimensionar y parametrizar el tren de engranajes rectos 1:1 ($Z=20, m=1{,}0\text{ mm}, b=7{,}0\text{ mm}$) para acoplamiento de motor NEMA 17 y eje de polea GT2 a $0{,}5\text{ m/s}$ ($750\text{ rpm}$)
- [x] 2.5 Configuración y activación del proyecto oficial de Autodesk Inventor (`Banco_Mecatronico_TFG.ipj`) mediante script Python automatizado
- [x] 2.6 Creación del catálogo completo de piezas paramétricas nativas (`.ipt`): perfiles 2020 L500/L540/L600, escuadra de 90°, tornillo M5 DIN 912, rueda V-Wheel, carro gantry, motor NEMA 17, engranaje 1:1, polea GT2 20T y soporte de motor
- [x] 2.7 Generación modular de subensamblajes y ensamblaje maestro (`.iam`): bastidor base, carro móvil, tracción GT2, batería SpaceX y ensamblaje general abierto en Inventor (`Banco_Mecatronico_TFG_Principal.iam`)


## 3. Integración, Pruebas y Documentación

- [ ] 3.1 Validar la simulación cinemática del movimiento combinado (avance de paneles + centrado lateral de hilo)
- [ ] 3.2 Generar y mantener en tiempo real el informe profesional diario de ingeniería en `informes/` con esquemas, cálculos dinámicos y avances para la memoria del TFG
