# Spacecraft Attitude Control System (SACS) & Microgravity Testbed

[![Platform: ESP32](https://img.shields.io/badge/Platform-ESP32-red.svg?logo=espressif)](https://www.espressif.com/)
[![CAD: Autodesk Inventor](https://img.shields.io/badge/CAD-Autodesk%20Inventor%202027-orange.svg?logo=autodesk)](https://www.autodesk.com/products/inventor)
[![Python: API Automation](https://img.shields.io/badge/Python-3.10%2B%20API%20adsk.inventor-blue.svg?logo=python)](https://python.org)
[![Control: Input Shaping](https://img.shields.io/badge/Control-ZV%20%2F%20ZVD%20Input%20Shaping-brightgreen.svg)]()
[![Status: In Active Development](https://img.shields.io/badge/Status-Active%20Development-yellow.svg)]()

> **Undergraduate Thesis (Trabajo de Fin de Grado - TFG)**  
> *Sistema Embebido de Control de Posición Bidireccional para Orientación de Prototipos Espaciales en Microgravedad Simulada*  
> **Author:** Pablo Rodríguez ([@pprguez2005-byte](https://github.com/pprguez2005-byte))

---

## 🛰️ Project Overview

This project focuses on the end-to-end mechatronic design, dynamic modeling, and embedded real-time control of a **Cartesian 2-DOF testbed** combined with a cable-suspended orientation system. The primary purpose is to simulate microgravity dynamics on Earth to test and validate **Attitude Determination and Control Systems (ADCS)** for small satellite prototypes (e.g., **CubeSats**).

During translational maneuvers, cable-suspended payloads experience residual pendular swing. This platform integrates **Input Shaping (Zero Vibration / Zero Vibration Derivative)** algorithms and S-curve trajectory profiling within an embedded real-time microcontroller environment to eliminate residual oscillations and achieve precise target pointing and trajectory tracking.

```
       [ Joystick / Manual Target ]
                   │ (WiFi / Telemetry)
                   ▼
     ┌────────────────────────────┐
     │      ESP32 Controller      │ ◄─── Attitude / Inertial Feedback
     │  (Input Shaping & Kinematics)
     └─────────────┬──────────────┘
                   │ Step / Dir (Timer ISRs)
                   ▼
     ┌────────────────────────────┐
     │ Trinamic Stepper Drivers   │
     └─────────────┬──────────────┘
                   │ Precise Actuation
                   ▼
  ┌──────────────────────────────────┐
  │   2020 V-Slot Aluminum Frame     │
  │   50 x 54 cm Cartesian Gantry    │
  │  (Timing Belt & Spur Gear Drive) │
  └────────────────┬─────────────────┘
                   │ Cable Suspension
                   ▼
       [ CubeSat / Space Payload ] (Zero Residual Vibration)
```

---

## 🚀 Key Features

* **Advanced Residual Vibration Mitigation:**
  * Coupled Lagrange equations of motion for cable-suspended multi-body dynamics.
  * Real-time **Input Shaping filters (ZV, ZVD)** implemented directly into stepper pulse generator ISRs.
  * S-curve jerk-limited trajectory generator for smooth accelerations.
* **100% Parametric CAD Automation:**
  * Fully automated 3D modeling using Autodesk Inventor's native API via Python (`adsk.inventor`).
  * Structural chassis built from 2020 V-slot aluminum extrusions (50x54 cm) with cast aluminum corner brackets and M5 DIN 912 hardware.
  * Internal timing belt system with 1:1 spur gear transmission for zero-backlash drive.
* **Deterministic Embedded Firmware:**
  * **ESP32 SuperMini** handling WiFi/WebSockets telemetry and trajectory tracking.
  * Hardware interrupt service routines (`Timer ISR`) for microsecond-precise, jitter-free stepper pulse generation.
  * Support for Trinamic TMC2209 drivers via UART (SilentStepStick & StallGuard).
* **Model-Based Systems Engineering (MBSE):**
  * Requirements traceability and architecture modeled using SysML v2.
  * Strict OpenSpec change management methodology.

---

## 📂 Repository Layout

```text
├── .agents/                    # Multi-agent operations and configuration
├── COMPRAS/                    # Bill of Materials (BOM) & procurement assets
│   ├── ListaCompra.xlsx        # Component procurement and supplier breakdown
│   └── CARRILERA.png           # Rail specification diagram
├── informes/                   # Daily technical engineering logs & academic notes
│   ├── INFORME_*.md            # Comprehensive daily cumulative engineering reports
│   └── README.md               # Guidelines for technical report authoring
├── openspec/                   # OpenSpec framework specification & change tracking
│   ├── changes/                # Active and archived change proposals
│   └── context/                # High-level architecture and project context
├── parte electrica/            # Embedded firmware, electrical diagrams & electronics
│   └── ESP32/
│       └── supermini_wifi/     # ESP32 SuperMini Arduino/C++ firmware
│           └── supermini_wifi.ino
├── Parte mecanica/             # Mechanical CAD, 3D printing & Inventor automation
│   ├── Inventor/
│   │   ├── scripts/            # Python scripts automating Autodesk Inventor 2027
│   │   │   ├── inventor_core.py
│   │   │   ├── generar_piezas_ipt.py
│   │   │   ├── generar_cubo_con_cintas.py
│   │   │   ├── actualizar_modelo_completo.py
│   │   │   └── ejecutar_todo_inventor.py
│   │   └── *.ipt / *.iam       # Parametric Inventor parts and assemblies
│   ├── cad/                    # Exported STEP and universal exchange models
│   ├── fotos medidas/          # Physical verification and measurement archives
│   └── historico_fusion/       # Legacy Autodesk Fusion 360 models
├── AGENTS.md                   # Operational engineering manual and coding rules
└── README.md                   # This file
```

---

## 🛠️ Hardware & Bill of Materials (BOM)

| Subsystem | Component / Specification | Role |
| :--- | :--- | :--- |
| **Structural Frame** | 2020 V-Slot Aluminum Extrusions | Modular 500 × 540 mm cuboid chassis |
| **Corner Brackets** | Cast aluminum 90° angle brackets + M5 Allen DIN 912 | Rigid structural nodes |
| **Linear Motion** | GT2 Timing Belts & Pulleys (1:1 spur drive) | High-precision Cartesian axes transmission |
| **Microcontroller** | ESP32 SuperMini (Xtensa 32-bit dual-core, WiFi/BLE) | Real-time motion control & telemetry |
| **Motor Drivers** | Trinamic TMC2209 Stepper Drivers (UART) | Low-noise, microstepping current control |
| **Actuators** | NEMA 17 Stepper Motors (1.8° step angle) | Primary kinematic drive |
| **Payload Interface** | Micro-filament braided line with balance swivel | Low-friction simulated microgravity suspension |

---

## 💻 Getting Started

### 1. Embedded Firmware Setup (ESP32)

1. Open [`parte electrica/ESP32/supermini_wifi/supermini_wifi.ino`](file:///parte%20electrica/ESP32/supermini_wifi/supermini_wifi.ino) in the Arduino IDE or PlatformIO.
2. Select target board: `ESP32C3 Dev Module` or `Generic ESP32`.
3. Configure WiFi SSID and credentials in the firmware.
4. Compile and flash via USB-C.

### 2. Autodesk Inventor Parametric CAD Generation

All mechanical models are generated programmatically via Python scripts interfacing with the Autodesk Inventor 2027 API:

```powershell
# Navigate to the Inventor scripts directory
cd "Parte mecanica\Inventor\scripts"

# Run the complete automated generation pipeline
python ejecutar_todo_inventor.py
```

* This regenerates all `.ipt` parts, assembles the 50x54 cm gantry in `.iam`, applies realistic finishes (Gold, Matte Black, Polished Aluminum), and exports updated STEP files to `cad/`.

---

## 📖 Academic Documentation

Detailed engineering justifications, mathematical derivations (Lagrangian dynamics, natural frequency calculations, damping ratio estimations, and Input Shaper convolution integrals) are documented chronologically in the [`informes/`](file:///informes/) directory:

* [`informes/`](file:///informes/): Cumulative daily technical reports tracking structural, electronic, and software milestones.
* [`openspec/context/CONTEXTO_GENERAL.md`](file:///openspec/context/CONTEXTO_GENERAL.md): High-level architectural context and project state.

---

## 📜 License

This project is developed as part of an official university Undergraduate Thesis (TFG). All rights reserved. Refer to academic citation guidelines before utilizing source code, CAD assets, or documentation.
