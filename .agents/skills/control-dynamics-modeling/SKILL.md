---
name: control-dynamics-modeling
description: Modelado matemático, simulación dinámica y técnicas de mitigación de oscilaciones (Input Shaping, curvas S, perfiles trapezoidales) para sistemas mecatrónicos con cargas suspendidas y péndulos de base móvil. Usar al derivar ecuaciones de movimiento, simular en Python/MATLAB, calcular frecuencias naturales o diseñar perfiles de aceleración sin vibración.
---

# Skill: Modelado Dinámico y Mitigación de Vibraciones en Sistemas Mecatrónicos

Esta habilidad proporciona directrices, formulaciones rigurosas y plantillas de código para el modelado físico-matemático, análisis dinámico y simulación de bancos de ensayo con cargas suspendidas (péndulos con carro móvil), transmisiones por husillo y perfiles de movimiento suave.

---

## 1. Fundamentos Teóricos: Péndulo Suspendido con Carro Móvil

### 1.1. Cinemática y Derivación de Lagrange
Para un satélite/carga de masa $m_s$ suspendido de un cable inextensible de longitud $L$, unido a un carro de masa $m_c$ con desplazamiento horizontal $x(t)$ y vertical $z(t)$:

- **Posición de la masa suspendida:**
  $$x_s(t) = x(t) + L \sin\phi(t)$$
  $$z_s(t) = z(t) - L \cos\phi(t)$$

- **Velocidades:**
  $$\dot{x}_s(t) = \dot{x}(t) + L \dot{\phi}(t) \cos\phi(t)$$
  $$\dot{z}_s(t) = \dot{z}(t) + L \dot{\phi}(t) \sin\phi(t)$$

- **Energía Cinética ($T$) y Potencial ($V$):**
  $$T = \frac{1}{2} m_s (\dot{x}_s^2 + \dot{z}_s^2)$$
  $$V = m_s g z_s = m_s g (z(t) - L \cos\phi(t))$$

- **Ecuación de Movimiento no lineal (coordenada generalizada $\phi$):**
  $$\ddot{\phi}(t) + \frac{c}{m_s L} \dot{\phi}(t) + \frac{g + \ddot{z}(t)}{L} \sin\phi(t) = -\frac{\ddot{x}(t)}{L} \cos\phi(t)$$
  *donde $c$ es el coeficiente de amortiguamiento viscoso aerodinámico (típicamente $\zeta \approx 0.005 - 0.02$).*

### 1.2. Linealización para Pequeñas Oscilaciones
Para ángulos pequeños ($\sin\phi \approx \phi$, $\cos\phi \approx 1$) y aceleración vertical despreciable ($\ddot{z} \ll g$):
$$\ddot{\phi}(t) + 2\zeta\omega_n \dot{\phi}(t) + \omega_n^2 \phi(t) = -\frac{a_x(t)}{L}$$
donde:
- **Frecuencia natural no amortiguada:** $\omega_n = \sqrt{\frac{g}{L}} \quad [\text{rad/s}]$
- **Período natural:** $T_n = \frac{2\pi}{\omega_n} = 2\pi \sqrt{\frac{L}{g}} \quad [\text{s}]$

---

## 2. Técnicas de Mitigación de Oscilaciones en Lazo Abierto

### 2.1. Límite Cuasi-estático de Aceleración
La deflexión angular instantánea máxima en régimen sostenido de aceleración constante $a_{max}$ es:
$$\phi_{max} \approx \frac{a_{max}}{g} \quad [\text{rad}] \approx \frac{a_{max}}{g} \cdot \frac{180^\circ}{\pi}$$
*Regla de diseño:* Para mantener el ángulo en $\phi \le 0.5^\circ$ ($0.0087\text{ rad}$), la aceleración máxima no debe superar:
$$a_{max} \le 0.0087 \cdot 9.81 \approx 0.085 \text{ m/s}^2$$

### 2.2. Input Shaping (Moldeado de Entrada)
El *Input Shaping* convoluciona la señal de mando con un tren de impulsos que interfieren destructivamente con la frecuencia natural del péndulo:

#### A. Shaper ZV (Zero Vibration) - 2 Impulsos:
- Tiempos de impulso: $t_1 = 0$, $t_2 = \frac{T_n}{2} = \frac{\pi}{\omega_n}$
- Amplitudes:
  $$K = e^{-\frac{\zeta \pi}{\sqrt{1-\zeta^2}}}$$
  $$A_1 = \frac{1}{1 + K}, \quad A_2 = \frac{K}{1 + K}$$
  *(Para amortiguamiento nulo $\zeta \approx 0$: $A_1 = 0.5$, $A_2 = 0.5$)*

#### B. Shaper ZVD (Zero Vibration and Derivative) - 3 Impulsos:
Mayor robustez frente a errores en la estimación de la longitud del cable $L$ ($\pm 20\%$ de tolerancia):
- Tiempos: $t_1 = 0$, $t_2 = \frac{T_n}{2}$, $t_3 = T_n$
- Amplitudes:
  $$A_1 = \frac{1}{(1+K)^2}, \quad A_2 = \frac{2K}{(1+K)^2}, \quad A_3 = \frac{K^2}{(1+K)^2}$$

### 2.3. Perfiles en Curva S (S-Curve / Jerk Controlado)
La aceleración no conmuta bruscamente, sino que tiene una derivada finita (*Jerk* $J = \frac{da}{dt}$):
- Fase 1: Rampa de aceleración ($0 \to a_{max}$ con $+J$)
- Fase 2: Aceleración constante ($a_{max}$)
- Fase 3: Rampa de deceleración de aceleración ($a_{max} \to 0$ con $-J$)
- Fase 4: Velocidad de crucero constante ($v_{max}$)
- Fases 5-7: Frenado simétrico.

---

## 3. Dinámica del Husillo y Acoplamiento con el Motor

- **Avance lineal por paso de motor:**
  $$\Delta x = \frac{p}{N_{pasos} \cdot \mu_{step}}$$
  *Ejemplo:* Con husillo T8 ($p = 8\text{ mm/rev}$), motor de 200 pasos ($1.8^\circ$) y 16 micropasos:
  $$\Delta x = \frac{8\text{ mm}}{200 \times 16} = 0.0025\text{ mm} = 2.5\,\mu\text{m/micropaso}$$

- **Inercia equivalente reflejada en el eje del motor:**
  $$J_{eq} = J_{rotor} + J_{acoplamiento} + J_{husillo} + m_{total} \left(\frac{p}{2\pi}\right)^2$$
  *donde:*
  $$J_{husillo} = \frac{1}{2} M_{h} R_h^2 = \frac{1}{2} (\rho \pi R_h^2 L_h) R_h^2$$

- **Par motor requerido:**
  $$T_{req} = T_{aceleracion} + T_{friccion} + T_{gravedad}$$
  $$T_{req} = J_{eq} \cdot \alpha_{motor} + \frac{F_{friccion} \cdot p}{2\pi \eta} + \frac{m_{elevada} \cdot g \cdot p}{2\pi \eta}$$

---

## 4. Script Estándar de Simulación en Python (SciPy)

Al ejecutar simulaciones para el TFG, utiliza esta estructura de referencia con `solve_ivp`:

```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def simular_pendulo_base_movil(L, ms, a_perfil, t_span, t_eval):
    """
    Simula el ángulo phi(t) y velocidad angular dphi(t)
    L: Longitud del cable (m)
    ms: Masa suspendida (kg)
    a_perfil: Función que devuelve ax(t) en m/s^2
    """
    g = 9.81
    zeta = 0.01  # Coeficiente de amortiguamiento ligero
    wn = np.sqrt(g / L)
    
    def derivadas(t, y):
        phi, dphi = y
        ax = a_perfil(t)
        # Ecuación no lineal completa
        ddphi = -(g / L) * np.sin(phi) - 2 * zeta * wn * dphi - (ax / L) * np.cos(phi)
        return [dphi, ddphi]
    
    sol = solve_ivp(derivadas, t_span, [0.0, 0.0], t_eval=t_eval, rtol=1e-8, atol=1e-10)
    return sol
```

---

## 5. Directrices de Presentación para la Memoria

1. Incluir siempre comparativa entre perfil rectangular (aceleración instantánea) vs. trapezoidal vs. S-curve vs. Input Shaping.
2. Presentar la gráfica de **Oscilación Residual vs. Tiempo de Maniobra** para justificar la elección de la frecuencia y tiempos de aceleración.
3. Contrastar el par motor teórico demandado con la curva característica par-velocidad del fabricante del motor NEMA 17.
