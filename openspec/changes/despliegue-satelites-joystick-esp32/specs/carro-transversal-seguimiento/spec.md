# Spec Delta: Carro Transversal de Seguimiento

## Purpose

Establece las especificaciones de guiado y desplazamiento del carro móvil motorizado en el eje transversal (izquierda a derecha) para corregir desviaciones laterales del hilo.

## ADDED Requirements

### Requirement: Desplazamiento Transversal Autónomo
El carro transversal SHALL montar un motor compacto que circule bidireccionalmente de izquierda a derecha a lo largo del perfil/puente móvil superior.

#### Scenario: Movimiento lateral hacia la izquierda o derecha
- **WHEN** el joystick detecta una desviación lateral $\theta_y \ne 0$ provocada por perturbación o balanceo transversal del panel
- **THEN** el motor transversal desplaza el carro en el sentido opuesto al error angular hasta devolver el hilo a la vertical

### Requirement: Sujeción y Desacoplo Mecánico del Joystick
El carro transversal SHALL incorporar la base de montaje para el sensor joystick comercial COTS y el punto de amarre de seguridad del cable suspendido.

#### Scenario: Retención del cable y guiado del joystick
- **WHEN** el cable experimenta la tensión axial del satélite suspendido
- **THEN** la tracción es absorbida por el soporte estructural del carro mientras que la palanca del joystick únicamente acompaña la inclinación angular libre de carga
