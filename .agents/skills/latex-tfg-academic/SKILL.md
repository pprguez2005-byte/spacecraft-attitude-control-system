---
name: latex-tfg-academic
description: Redacción académica, maquetación y formateo en LaTeX para la memoria técnica del Trabajo de Fin de Grado (TFG/TFM) en Ingeniería. Usar para estructurar capítulos, redactar fórmulas y unidades (siunitx), tablas profesionales (booktabs), gestión de citas bibliográficas con BibTeX/BibLaTeX y presupuesto de ingeniería.
---

# Skill: Redacción Académica y Maquetación en LaTeX para Memorias de TFG

Esta habilidad establece las directrices de estilo formal, estructura modular de archivos y estándares tipográficos para la redacción de la memoria del Trabajo de Fin de Grado en Ingeniería Mecatrónica / Aeroespacial / Electrónica.

---

## 1. Estructura Modular Recomendada del Proyecto LaTeX

Para mantener el proyecto ordenado y evitar archivos monolíticos inmanejables:

```text
tfg_memoria/
├── main.tex                 # Archivo raíz con preámbulo y llamadas \input / \include
├── preambulo/
│   ├── paquetes.tex         # Paquetes y configuraciones
│   └── comandos.tex         # Macros personalizadas y glosario
├── capitulos/
│   ├── 01_introduccion.tex
│   ├── 02_estado_del_arte.tex
│   ├── 03_especificaciones.tex
│   ├── 04_modelado_teorico.tex
│   ├── 05_diseno_mecanico.tex
│   ├── 06_hardware_electronico.tex
│   ├── 07_firmware_y_control.tex
│   ├── 08_ensayos_y_resultados.tex
│   ├── 09_presupuesto.tex
│   └── 10_conclusiones.tex
├── anexos/
│   ├── anexo_planos.tex
│   └── anexo_codigo.tex
├── figuras/                 # Imágenes vectoriales (PDF/SVG) y esquemas
└── bibliografia/
    └── referencias.bib      # Base de datos BibTeX
```

---

## 2. Paquetes Imprescindibles y Configuración Tipográfica

En el archivo `paquetes.tex`, incluir:

```latex
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-tabla]{babel} % es-tabla para usar 'Tabla' en vez de 'Cuadro'
\usepackage{amsmath,amssymb,mathtools}
\usepackage{siunitx}                % Tipografía científica de unidades
\usepackage{booktabs}               % Tablas limpias sin líneas verticales
\usepackage{graphicx}
\usepackage{subcaption}             % Subfiguras (a), (b)...
\usepackage{listings}               % Código fuente con resaltado
\usepackage{microtype}              % Mejoras tipográficas y justificación
\usepackage[hidelinks]{hyperref}
\usepackage[capitalise,noabbrev]{cleveref} % Referencias automáticas (Fig. 1, Ec. 2)

% Configuración de siunitx para castellano
\sisetup{
    output-decimal-marker = {,},
    per-mode = symbol,
    range-phrase = { a },
    separate-uncertainty = true
}
```

---

## 3. Reglas de Estilo Científico y Notación

### 3.1. Uso de Unidades (`siunitx`)
- **Regla:** Nunca escribir unidades en modo texto normal (ej. `10 m/s^2` es incorrecto). Utilizar siempre `\SI`:
  - $\SI{9.81}{\meter\per\second\squared}$ $\to$ `\SI{9.81}{\meter\per\second\squared}`
  - $\SI{500}{\gram}$ $\to$ `\SI{500}{\gram}`
  - $\SI{8}{\milli\meter\per\revolution}$ $\to$ `\SI{8}{\milli\meter\per\revolution}`
  - $\SIrange{12}{24}{\volt}$ $\to$ `\SIrange{12}{24}{\volt}`

### 3.2. Formato Profesional de Tablas (`booktabs`)
- **Prohibido:** No utilizar líneas verticales en tablas (`|c|c|`). Los tribunales académicos penalizan las tablas recargadas.
- **Estructura correcta:** Usar exclusivamente `\toprule`, `\midrule` y `\bottomrule`:

```latex
\begin{table}[htbp]
    \centering
    \caption{Comparativa de parámetros de transmisión entre husillo T8 y correa GT2.}
    \label{tab:comparativa_transmision}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Parámetro} & \textbf{Husillo T8x8} & \textbf{Correa GT2} & \textbf{Unidad} \\
        \midrule
        Avance por vuelta & 8{,}0 & 40{,}0 & \si{\milli\meter} \\
        Resolución angular (200 pasos) & 0{,}040 & 0{,}200 & \si{\milli\meter\per\step} \\
        Elasticidad axial & Despreciable & Moderada & -- \\
        Autobloqueo en vertical & Parcial/Alto & Nulo & -- \\
        \bottomrule
    \end{tabular}
\end{table}
```

---

## 4. Estructura del Capítulo de Presupuesto (Exigencia Académica)

Un TFG de ingeniería debe desglosar el presupuesto en 4 categorías claras:

1. **Costes de Materiales y Componentes Comerciales:**
   - Perfiles de aluminio, tornillería, motores NEMA 17, drivers TMC2209, placa ARM, husillos, rodamientos y filamento 3D.
2. **Costes de Equipos y Fabricación:**
   - Horas de máquina (impresora 3D, consumo eléctrico amortizado).
3. **Costes de Personal (Honorarios de Ingeniería):**
   - Horas dedicadas por el alumno computadas como Ingeniero Junior (ej. $300\text{ h} \times 25\text{ \euro{}/h}$).
4. **Resumen Económico General e Impuestos:**
   - Base Imponible + Gastos Generales ($13\%$) + Beneficio Industrial ($6\%$) + IVA ($21\%$).

---

## 5. Tono de Redacción y Buenas Prácticas

- **Voz pasiva refleja o primera persona del plural:** Emplear preferentemente *"Se diseñó un mecanismo..."*, *"Se implementó el algoritmo..."* o *"Hemos analizado..."*, evitando la primera persona del singular (*"Yo hice..."*).
- **Justificación de decisiones:** Cada elección técnica (ej. descartar correas dentadas o descartar lazo cerrado en primera iteración) debe estar argumentada técnica y económicamente.
- **Referencias bibliográficas rigurosas:** Citar artículos indexados (IEEE, AIAA) y libros canónicos para el modelado de motores paso a paso (ej. Kenjo) y dinámica (ej. Meirovitch, Ogata).
