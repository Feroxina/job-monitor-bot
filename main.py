import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
SHEET_NAME = os.getenv("SHEET_NAME")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

KEYWORDS = ["data analyst", "python", "automatizacion", "RPA"]


def conectar_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    google_credentials = os.getenv("GOOGLE_CREDENTIALS")
    if google_credentials:
        import json
        from oauth2client.service_account import ServiceAccountCredentials
        creds_dict = json.loads(google_credentials)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet


def obtener_ofertas_adzuna():
    ofertas = []
    for keyword in KEYWORDS:
        url = (
            f"https://api.adzuna.com/v1/api/jobs/es/search/1"
            f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
            f"&what={keyword}&where=Barcelona&results_per_page=5"
        )
        response = requests.get(url)
        data = response.json()
        for resultado in data.get("results", []):
            ofertas.append({
                "titulo": resultado.get("title", "Sin titulo"),
                "empresa": resultado.get("company", {}).get("display_name", "Sin empresa"),
                "ubicacion": resultado.get("location", {}).get("display_name", "Sin ubicacion"),
                "salario": str(resultado.get("salary_min", "No especificado")),
                "url": resultado.get("redirect_url", ""),
                "fecha": datetime.now().strftime("%d/%m/%Y")
            })
    return ofertas


def guardar_en_sheets(sheet, ofertas):
    try:
        urls_existentes = sheet.col_values(5)
    except Exception:
        urls_existentes = []
    nuevas = []
    for oferta in ofertas:
        if oferta["url"] not in urls_existentes:
            sheet.append_row([
                oferta["titulo"],
                oferta["empresa"],
                oferta["ubicacion"],
                oferta["salario"],
                oferta["url"],
                oferta["fecha"],
                "No"
            ])
            nuevas.append(oferta)
    return nuevas


def enviar_email(nuevas_ofertas):
    if not nuevas_ofertas:
        print("No hay ofertas nuevas. No se envia email.")
        return
    cuerpo = "Nuevas ofertas de empleo encontradas:\n\n"
    for o in nuevas_ofertas:
        cuerpo += f"- {o['titulo']}\n"
        cuerpo += f"  Empresa: {o['empresa']}\n"
        cuerpo += f"  URL: {o['url']}\n\n"
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER
    msg["Subject"] = f"Job Monitor - {len(nuevas_ofertas)} nuevas ofertas ({datetime.now().strftime('%d/%m/%Y')})"
    msg.attach(MIMEText(cuerpo, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email enviado con {len(nuevas_ofertas)} ofertas nuevas.")
    except Exception as e:
        print(f"Error enviando email: {e}")


def main():
    print("Buscando ofertas en Adzuna...")
    ofertas = obtener_ofertas_adzuna()
    print(f"Encontradas: {len(ofertas)} ofertas")
    print("Conectando con Google Sheets...")
    sheet = conectar_sheets()
    print("Guardando ofertas nuevas...")
    nuevas = guardar_en_sheets(sheet, ofertas)
    print(f"Nuevas guardadas: {len(nuevas)}")
    print("Enviando email resumen...")
    enviar_email(nuevas)
    print("Bot ejecutado correctamente.")


if __name__ == "__main__":
    main()