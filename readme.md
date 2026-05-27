# Attack Surface Lab

Ejecutar sctipt:
Ctrl + Shift + P
Tasks: Run Task
FIN


https://chatgpt.com/c/69f32c29-660c-83eb-af73-4112eb6590fc

pip3 install requests

python -m venv venv
.\venv\Scripts\Activate.ps1
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

python main.py


Herramienta desarrollada en Python para el **descubrimiento de activos** y el **análisis de superficie de ataque** en entornos de red.

## 📌 Descripción

Este proyecto tiene como objetivo identificar activos expuestos (hosts, dominios, servicios) y analizar posibles puntos de entrada desde una perspectiva de ciberseguridad.

Está orientado tanto a uso educativo como a pruebas básicas de reconocimiento (reconnaissance).

## 🚀 Funcionalidades

* Descubrimiento de hosts en red
* Enumeración de servicios
* Identificación de puertos abiertos
* Análisis básico de superficie de ataque
* Generación de resultados en consola

## 🛠️ Tecnologías

* Python 3
* Librerías estándar (y opcionalmente externas según evolución)

## ▶️ Uso

Clona el repositorio:

```bash
git clone https://github.com/tuusuario/attack-surface-lab.git
cd attack-surface-lab
pip3 install requests
```

Ejecuta el script principal:

```bash
python main.py
```

## 📂 Estructura del proyecto



```
attack-surface-lab/
│
├── main.py                  # Punto de entrada
├── config/
│   └── settings.py         # Configuración global
│
├── core/                   # Núcleo del sistema
│   ├── engine.py           # Orquestador de módulos
│   ├── pipeline.py         # Flujo de ejecución
│   ├── base_module.py      # Clase base para módulos
│   └── exceptions.py
│
├── modules/                # Módulos independientes
│   ├── domain/
│   │   ├── domain_info.py
│   │   └── subdomain_enum.py
│   │
│   ├── network/
│   │   ├── ip_resolver.py
│   │   ├── subnet_scan.py
│   │   └── port_scanner.py
│   │
│   ├── services/
│   │   └── service_detector.py
│   │
│   ├── osint/
│   │   ├── whois_lookup.py
│   │   └── provider_info.py
│   │
│   └── enrichment/
│       └── geoip.py
│
├── models/                 # Estructuras de datos
│   ├── asset.py
│   ├── domain.py
│   ├── ip.py
│   └── service.py
│
├── utils/
│   ├── logger.py
│   ├── helpers.py
│   └── validators.py
│
├── input/
│   └── targets.json        # Entrada (dominios/IPs)
│
├── output/
│   └── results.json        # Salida final
│
├── tests/
│
└── requirements.txt
```



## ⚠️ Aviso legal

Este proyecto es únicamente para **fines educativos**.
No se debe utilizar contra sistemas sin autorización.

## 👨‍💻 Autor

Carlos Basulto

## 📄 Licencia

Este proyecto se distribuye bajo licencia MIT.
