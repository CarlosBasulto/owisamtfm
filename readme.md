# OwisamTFM

Herramienta desarrollada en Python para la **auditoría de seguridad en redes inalámbricas** siguiendo la metodología **OWISAM** (adaptada y ampliada), ejecutada sobre una **Raspberry Pi con Kali Linux**.

Desarrollada como contribución software del TFM *"Diseño e implementación de una herramienta de auditoría Wi-Fi basada en Kali Linux bajo la metodología OWISAM"* — Máster Universitario en Ciberseguridad, UNIR.

---

## Descripción

WiFiAuditKit actúa como **orquestador de herramientas de auditoría inalámbrica** disponibles en Kali Linux. Guía al auditor a través de las fases de la metodología OWISAM adaptada, invoca automáticamente las herramientas necesarias en cada control, y genera un informe estructurado de hallazgos.

Está orientado tanto a **uso profesional** (auditorías controladas) como a **uso educativo** en ciclos de especialización en ciberseguridad.

---

## Funcionalidades

* Descubrimiento de redes Wi-Fi en 2,4 GHz y 5 GHz
* Identificación de clientes asociados a puntos de acceso
* Evaluación del tipo de cifrado (OPN, WEP, WPA2, WPA3-SAE)
* Detección de ausencia de PMF (Protected Management Frames / 802.11w)
* Captura de handshake WPA2 (4-way) y captura de PMKID
* Detección de configuraciones de degradación WPA3 → WPA2 (downgrade)
* Evaluación de exposición de interfaz de administración del AP
* Generación de informe de resultados en JSON y texto plano con valoración de riesgo por red

---

## Tecnologías

* Python 3
* Kali Linux (Raspberry Pi 4 — ARM)
* Adaptador Wi-Fi con chipset RTL8812AU (modo monitor + inyección, 2,4/5 GHz)
* Herramientas externas orquestadas: `airmon-ng`, `airodump-ng`, `aireplay-ng`, `hcxdumptool`, `hcxpcapngtool`, `Kismet`, `Scapy`, `Nmap`

---

##  Uso

### Requisitos previos

```bash
# En Kali Linux (Raspberry Pi)
sudo apt install aircrack-ng hcxdumptool hcxtools kismet nmap
pip3 install scapy requests
```

### Instalación

```bash
git clone https://github.com/cbasulto/wifiauditkit.git
cd wifiauditkit
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Ejecución

```bash
# Auditoría completa sobre la interfaz wlan1
sudo python main.py --interface wlan1

# Solo fase de descubrimiento
sudo python main.py --interface wlan1 --module discovery

# Sobre un objetivo concreto (BSSID)
sudo python main.py --interface wlan1 --bssid AA:BB:CC:DD:EE:FF --channel 6
```

### En VS Code (tarea configurada)

```
Ctrl + Shift + P → Tasks: Run Task → Run WiFiAuditKit
```

---

## Estructura del proyecto

```
wifiauditkit/
│
├── main.py                      # Punto de entrada y parsing de argumentos
├── config/
│   └── settings.py              # Configuración global (timeouts, rutas, etc.)
│
├── core/                        # Núcleo del sistema
│   ├── engine.py                # Orquestador de módulos OWISAM
│   ├── pipeline.py              # Flujo de ejecución por fases
│   ├── base_module.py           # Clase base para módulos de auditoría
│   └── exceptions.py
│
├── modules/                     # Módulos de auditoría (uno por control OWISAM)
│   ├── discovery/
│   │   ├── network_scan.py      # OWISAM-DI-001: descubrimiento de redes
│   │   └── client_enum.py       # OWISAM-DI-002: enumeración de clientes
│   │
│   ├── encryption/
│   │   ├── cipher_check.py      # OWISAM-TS-001: evaluación del tipo de cifrado
│   │   ├── handshake_capture.py # OWISAM-TS-002: captura de handshake WPA2
│   │   └── pmkid_capture.py     # OWISAM-TS-002: captura de PMKID (hcxdumptool)
│   │
│   ├── mgmt_frames/
│   │   └── pmf_check.py         # OWISAM-TS-003: verificación de PMF (802.11w)
│   │
│   ├── open_networks/
│   │   └── open_ap_detect.py    # OWISAM-TS-004: detección de redes abiertas
│   │
│   ├── downgrade/
│   │   └── wpa3_downgrade.py    # OWISAM-TS-005: detección de downgrade WPA3→WPA2
│   │
│   └── ap_config/
│       └── admin_exposure.py    # OWISAM-AP-001: exposición de interfaz de admin
│
├── models/                      # Estructuras de datos
│   ├── network.py               # Modelo de red Wi-Fi auditada
│   ├── client.py                # Modelo de cliente asociado
│   ├── finding.py               # Modelo de hallazgo (control + resultado + riesgo)
│   └── report.py                # Modelo de informe final
│
├── utils/
│   ├── logger.py
│   ├── interface.py             # Gestión del adaptador y modo monitor
│   ├── subprocess_runner.py     # Invocación segura de herramientas externas
│   └── validators.py
│
├── input/
│   └── targets.json             # Objetivos definidos (BSSIDs / ESSIDs)
│
├── output/
│   ├── results.json             # Informe de resultados (JSON)
│   └── results.txt              # Informe de resultados (texto plano)
│
├── tests/
│
└── requirements.txt
```

---

## Controles OWISAM implementados

| ID | Descripción | Estado | Herramienta |
|----|-------------|--------|-------------|
| OWISAM-DI-001 | Descubrimiento de redes (2,4 / 5 GHz) | Mantenido | airodump-ng |
| OWISAM-DI-002 | Enumeración de clientes asociados | Mantenido | airodump-ng |
| OWISAM-TS-001 | Evaluación del tipo de cifrado (incl. WPA3) | Adaptado | airodump-ng + beacon analysis |
| OWISAM-TS-002 | Captura de handshake WPA2 y PMKID | Adaptado | aireplay-ng + hcxdumptool |
| OWISAM-TS-003 | Verificación de PMF / 802.11w | **Nuevo** | Scapy |
| OWISAM-TS-004 | Detección de redes abiertas | Mantenido | airodump-ng |
| OWISAM-TS-005 | Detección de downgrade WPA3 → WPA2 | **Nuevo** | airodump-ng + RSN IE analysis |
| OWISAM-AP-001 | Exposición de interfaz de administración | Adaptado | Nmap |

---

## Aviso legal

Este proyecto es únicamente para **fines educativos y de investigación**.
No debe utilizarse contra sistemas sin autorización expresa del propietario.
El uso indebido es responsabilidad exclusiva del usuario.

---

##  Autor

Carlos Basulto — TFM Máster Universitario en Ciberseguridad, UNIR (2026)

## Licencia

Este proyecto se distribuye bajo licencia MIT.
