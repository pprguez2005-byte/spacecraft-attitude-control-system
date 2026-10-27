# 🤖 Manual Operativo del Agente (AGENTS.md)

> **Proyecto:** Sistema Embebido de Control de Posición Bidireccional para Orientación de Prototipos Espaciales en Microgravedad Simulada  
> **Titulación:** Trabajo de Fin de Grado (TFG)  
> **Directorio de Trabajo:** `27_10_26`  
> **Última Actualización:** 27/10/2026  

---

## 🛑 1. Reglas Primarias e Inviolables de Comportamiento

1. **PROHIBICIÓN ESTRICTA DE INVENTAR (CERO ALUCINACIONES) Y CONSULTA OBLIGATORIA:**
   - El agente **NO** debe inventar datos, requisitos, parámetros físicos, supuestos matemáticos, bibliografía, decisiones de diseño ni especificaciones que no hayan sido dadas o aprobadas por el usuario.
   - **CONSULTA OBLIGATORIA ANTE CUALQUIER INCERTIDUMBRE:** Es mandato expreso e inviolable **PREGUNTAR DIRECTAMENTE AL USUARIO** todo aquello que no se tenga 100% claro, ya sean **valores numéricos, medidas dimensionales, carreras, cargas, tolerancias, modelos de componentes, interfaces mecánicas o cinemáticas**. Jamás asumir, aproximar o inferir medidas sin confirmación previa.

2. **SUBORDINACIÓN Y CONTROL TOTAL DEL USUARIO:**
   - Todo lo que el agente haga está supeditado al control, supervisión y aprobación explícita del usuario.
   - No ejecutar cambios destructivos, modificaciones estructurales o giros de diseño sin previo consenso.
   - Proponer primero el plan de acción, explicar los motivos técnicos y esperar el visto bueno del usuario.

3. **METODOLOGÍA OPENSPEC OBLIGATORIA:**
   - Todo desarrollo, nueva propuesta o modificación sustancial se gestiona formalmente a través de OpenSpec (`openspec/changes/`).
   - Se generan primero los artefactos de planificación (`proposal.md`, `specs/`, `design.md`, `tasks.md`).
   - No se implementa código o diseño hasta que el usuario apruebe la propuesta.
   - Al finalizar, se archiva el cambio para preservar el contexto día a día.

4. **PROHIBICIÓN ESTRICTA DE TRABAJAR EN `main` (GIT BRANCHING OBLIGATORIO):**
   - **JAMÁS trabajar ni modificar código directamente sobre la rama `main`**.
   - Cada propuesta de OpenSpec debe contar **siempre e inexcusablemente** con su propia rama de Git nueva y dedicada (ej. `git checkout -b change/<nombre-cambio>` o `feature/<nombre>`).
   - Todo el trabajo, implementación y pruebas se ejecutan en esa rama.
   - La fusión (*merge*) con `main` solo se efectúa tras la validación final del usuario y el archivado del cambio.

5. **GESTIÓN Y PRESERVACIÓN DEL CONTEXTO:**
   - En [`openspec/context/CONTEXTO_GENERAL.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/openspec/context/CONTEXTO_GENERAL.md) se mantiene el resumen ejecutivo permanente con todo lo importante del proyecto.
   - Al cerrar o cambiar de etapa, se actualiza dicho archivo para conservar la memoria acumulada sesión a sesión.

6. **INFORME PROFESIONAL DE INGENIERÍA AL CIERRE DE CADA DÍA:**
   - Al término de cada jornada de trabajo, es **obligatorio** generar un informe técnico profesional en el directorio [`informes/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/informes/).
   - Debe detallar con rigor de nivel de TFG: objetivos cubiertos, justificación física/matemática, fragmentos de código comentados, esquemas, gráficas, diagramas (Mermaid/PNG), resultados de validación y conclusiones para la memoria.

7. **LECTURA OBLIGATORIA AL INICIAR CADA SESIÓN:**
   - El agente debe leer este archivo [`AGENTS.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/AGENTS.md) y [`openspec/context/CONTEXTO_GENERAL.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/openspec/context/CONTEXTO_GENERAL.md) al inicio de cada conversación para conocer el marco, el estado del proyecto y las restricciones vigentes.

8. **INTEGRIDAD TÉCNICA Y DOCUMENTAL:**
   - Mantener siempre la justificación matemática y física rigurosa de cada módulo.
   - Conservar comentarios técnicos y trazabilidad en el código.
   - Usar enlaces markdown con formato `file:///` con barras normales para referenciar ficheros y símbolos.

---

## 📌 2. Visión General del Proyecto (TFG)

### 2.1. Propósito
Desarrollo mecatrónico completo de un banco de ensayos cartesianos de 2 GDL ($X$ y $Z$) para simulación de microgravedad y orientación controlada de prototipos espaciales (CubeSat) suspendidos por cable, incorporando técnicas de control de vibración residual (*Input Shaping*).

### 2.2. Pilares de Desarrollo
1. **Modelado y Control Dinámico:** Ecuaciones dinámicas acopladas de Lagrange, análisis modal, atenuación de balanceo mediante filtros *Input Shaping* (ZV / ZVD) y perfiles de trayectoria en S.
2. **Ingeniería de Sistemas Basada en Modelos (MBSE):** Modelado formal en SysML v2 (Eclipse SysON) para trazabilidad de requisitos, diagrama de bloques, puertos y estados (FSM).
3. **Diseño Mecánico y Fabricación Aditiva:** Estructura con perfiles de aluminio estructural, guiado lineal, husillos T8, soportes impresos en 3D (FDM con tolerancias específicas) y cálculo de deflexión estructural.
4. **Firmware Embebido de Tiempo Real:** Código en C/C++ para microcontroladores ARM de 32 bits, temporizadores por interrupciones hardware (*Timer ISR*) con bajo *jitter*, drivers Trinamic TMC2209 vía UART y arquitectura no bloqueante.
5. **Memoria Académica Formal:** Redacción en LaTeX estructurada de forma modular, con tipografía técnica según normas UNE/ISO, gestión con `siunitx`, tablas `booktabs` y bibliografía científica contrastada.

---

## ⚙️ 3. Parámetros Físicos y Requisitos Base del Sistema

*(Cualquier modificación sobre estos valores requiere validación expresa del usuario)*

### 3.1. Parámetros Nominales del Péndulo Suspendido
- **Longitud del cable ($L$):** $0{,}60\text{ m}$ ($600\text{ mm}$)
- **Masa suspendida ($m_s$):** $0{,}35\text{ kg}$ ($350\text{ g}$)
- **Gravedad ($g$):** $9{,}81\text{ m/s}^2$
- **Frecuencia natural angular ($\omega_n$):** $\omega_n = \sqrt{g/L} \approx 4{,}0435\text{ rad/s}$
- **Período natural de oscilación ($T_n$):** $T_n = 2\pi / \omega_n \approx 1{,}5539\text{ s}$
- **Frecuencia natural cíclica ($f_n$):** $f_n \approx 0{,}6435\text{ Hz}$
- **Factor de amortiguamiento viscoso ($\zeta$):** $0{,}015$ (estimación aire)
- **Tiempo entre impulsos ZV ($\Delta t_{ZV}$):** $\frac{T_n}{2} \approx 0{,}777\text{ s}$

### 3.2. Criterios de Rendimiento y Seguridad
- **Desviación angular admisible:** $\phi \le 0{,}5^\circ$ en régimen dinámico.
- **Vibración residual objetivo:** $\phi_{residual} \le 0{,}05^\circ$ tras frenada (con Input Shaping ZV teóricamente $0{,}0^\circ$).
- **Carrera útil mínima:** Eje $X \ge 300\text{ mm}$, Eje $Z \ge 500\text{ mm}$.
- **Seguridad:** Finales de carrera normalmente cerrados (NC / *fail-safe*), parada de emergencia por interrupción prioritaria ($< 10\text{ ms}$).

---

## 🗂️ 4. Estructura del Espacio de Trabajo (`26_10_26`)

```text
26_10_26/
├── AGENTS.md                   # Manual operativo y de control del agente
├── informes/                   # Informes profesionales diarios de ingeniería (TFG)
│   └── INFORME_YYYY_MM_DD.md   # Informe diario de avance con código, diagramas y gráficas
├── openspec/                   # Gestión formal de especificaciones y control de cambios
│   ├── config.yaml             # Reglas operativas y contexto de OpenSpec
│   ├── context/                # Repositorio de contexto día a día
│   │   ├── README.md           # Índice del repositorio de contexto
│   │   └── CONTEXTO_GENERAL.md # Resumen técnico integral permanente
│   ├── specs/                  # Especificaciones principales consolidadas
│   └── changes/                # Propuestas activas y archivadas (archive/)
├── .agents/                    # Habilidades y flujos de trabajo OpenSpec
└── [Módulos a coordinar según indique el usuario]:
    ├── ESP32/                  # Módulos de comunicaciones y telemetría
    ├── simulacion/             # Modelado dinámico y cálculos Python
    ├── sysml/                  # Modelo MBSE SysML v2
    ├── firmware/               # Código ARM C/C++
    ├── cad/                    # Diseños mecánicos 3D
    └── memoria/                # Documento LaTeX del TFG
```

> **Nota de trazabilidad histórica:** Las versiones y avances de sesiones previas se encuentran archivadas en los directorios hermanos correspondientes (ej. `..\23_10_26`). Ningún archivo se copia o altera sin que el usuario lo solicite.

---

## 📋 5. Protocolo de Trabajo Sesión a Sesión

1. **Lectura y Sincronización:** Leer [`AGENTS.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/AGENTS.md) y [`CONTEXTO_GENERAL.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/openspec/context/CONTEXTO_GENERAL.md) al inicio.
2. **Definición del Objetivo:** Confirmar con el usuario el propósito concreto de la sesión.
3. **Propuesta Formal OpenSpec (`openspec new change <nombre>`):** Generar los artefactos de propuesta (`proposal.md`, `specs/`, `design.md`, `tasks.md`) sin tocar código de proyecto.
4. **Creación Obligatoria de Rama Git:** Crear y conmutar a una nueva rama dedicada (`git checkout -b change/<nombre-cambio>`). **Prohibido trabajar en `main`**.
5. **Validación y Aprobación del Usuario:** Esperar confirmación y visto bueno explícito antes de cualquier ejecución.
6. **Implementación de Tareas (`opsx apply`):** Desarrollar y verificar las tareas aprobadas paso a paso dentro de la rama.
7. **Consolidación, Archivado y Fusión:** Archivar el cambio (`openspec archive`), actualizar [`CONTEXTO_GENERAL.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/openspec/context/CONTEXTO_GENERAL.md) y fusionar a `main` bajo autorización expresa.
8. **Cierre de Jornada (Informe de Ingeniería):** Generar el informe profesional diario en [`informes/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/26_10_26/informes/) documentando los desarrollos con código, gráficas/imágenes, análisis matemático y lecciones aprendidas para la memoria final del TFG.

---

## 📝 6. Registro de Acuerdos y Decisiones

### Sesión 26/10/2026
- [x] **26/10/2026:** Creación de [`AGENTS.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/AGENTS.md) con la directiva innegociable de cero invención, control absoluto por parte del usuario y lectura obligatoria al iniciar.
- [x] **26/10/2026:** Adopción obligatoria de la metodología OpenSpec para cualquier propuesta de desarrollo y retención del contexto día a día.
- [x] **26/10/2026:** Creación de la carpeta [`openspec/context/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/openspec/context/README.md) y el archivo de síntesis permanente [`CONTEXTO_GENERAL.md`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/openspec/context/CONTEXTO_GENERAL.md).
- [x] **26/10/2026:** Establecimiento obligatorio de emisión de informe profesional diario de ingeniería en [`informes/`](file:///C:/Users/Usuario/Desktop/universidad/clase/TFG/27_10_26/informes/) con código, diagramas y resultados cuantitativos.
- [x] **26/10/2026:** Directiva obligatoria de Git: **Prohibición total de trabajar en `main`**. Cada cambio de OpenSpec debe tener su propia rama nueva dedicada (`change/<nombre>`).

### Sesión 27/10/2026
- [x] **27/10/2026:** Inicialización del repositorio Git local con rama base `main`.
- [x] **27/10/2026:** Incorporación en Regla 1 de la directiva expresa de **CONSULTA OBLIGATORIA ANTE CUALQUIER INCERTIDUMBRE (medidas, valores, parámetros)**.
- [x] **27/10/2026:** Adopción del concepto de simulación de despliegue tipo SpaceX (columna de paneles solares/satélites sostenidos por cable) con batería de perfiles superiores motorizados en avance longitudinal y carro móvil transversal.
- [x] **27/10/2026:** Decisión de adquisición COTS para el sensor/joystick de inclinación y lectura/control mediante microcontrolador ESP32.
