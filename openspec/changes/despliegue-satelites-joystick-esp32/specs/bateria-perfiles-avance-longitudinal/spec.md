# Spec Delta: Batería de Perfiles y Avance Longitudinal

## Purpose

Define los requisitos funcionales de la bancada superior de perfiles paralelos en batería y su sistema de tracción para el avance del soporte de sujeción coordinado con el despliegue del satélite.

## ADDED Requirements

### Requirement: Guiado Longitudinal por Batería de Perfiles
La bancada superior SHALL estructurarse mediante una batería de perfiles de aluminio estructural paralelos montados sobre el pórtico principal, garantizando el soporte del carro superior y minimizando la deflexión mecánica.

#### Scenario: Distribución de carga en la batería
- **WHEN** el conjunto superior sostiene el carro móvil y la carga suspendida del satélite
- **THEN** la estructura de perfiles mantiene la alineación longitudinal sin flecha apreciable ni interferencia mecánica

### Requirement: Avance Sincronizado Longitudinal
El mecanismo de avance longitudinal SHALL desplazar el punto de sujeción superior hacia adelante a lo largo de la batería de perfiles para anular el ángulo de inclinación $\theta_x$ detectado por el joystick.

#### Scenario: Compensación de avance
- **WHEN** el ESP32 detecta una desviación positiva en el eje longitudinal $\theta_x > 0$
- **THEN** el motor de avance acciona el carro superior hacia adelante hasta restituir la perpendicularidad del hilo ($\theta_x \le 0{,}05^\circ$)
