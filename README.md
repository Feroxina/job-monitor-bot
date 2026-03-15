# 🤖 Job Monitor Bot

Bot en Python que busca ofertas de empleo tech automáticamente, las guarda en Google Sheets y envía alertas por email cuando hay novedades.

## ¿Qué hace?

- Busca ofertas de empleo tech en Barcelona usando la API de Adzuna
- Filtra por keywords: Data Analyst, Python, Automatización, RPA
- Guarda las ofertas en Google Sheets evitando duplicados
- Envía un email resumen cuando encuentra ofertas nuevas

## Tecnologías usadas

- Python 3.14
- Google Sheets API + gspread
- Adzuna Jobs API
- smtplib (envío de emails)
- python-dotenv (gestión de credenciales)

## Estructura del proyecto
```
job-monitor-bot/
├── main.py           # Script principal
├── requirements.txt  # Dependencias
├── .env.example      # Variables de entorno necesarias
└── .gitignore
```

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Actívalo: `venv\Scripts\activate`
4. Instala dependencias: `pip install -r requirements.txt`
5. Configura las variables de entorno (ver `.env.example`)
6. Ejecuta: `python main.py`

## Variables de entorno necesarias
```
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_app_password
SHEET_NAME=Job Monitor
ADZUNA_APP_ID=tu_app_id
ADZUNA_APP_KEY=tu_app_key
```