#!/usr/bin/env python3
import subprocess
from datetime import date
import sys

today = date.today()
weekday = today.weekday()
day_num = today.day

DIAS_ES = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
MESES_ES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

DEADLINES = {
    "UHU Huelva": date(2026,5,18),
    "UA Alicante": date(2026,6,26),
    "UVa Valladolid": date(2026,7,10),
    "UAB Barcelona": date(2026,7,15),
    "UB Barcelona": date(2026,7,20),
    "UPV Valencia": date(2026,6,30),
    "UdL Lleida": date(2026,7,5),
    "URV Tarragona": date(2026,7,12),
}

OPENS = {
    "UGR Granada": date(2026,6,17),
    "USC Santiago": date(2026,6,23),
    "MUCAII": date(2026,6,1),
    "UNED": date(2026,5,15),
    "UC3M": date(2026,5,20),
    "UAM": date(2026,6,5),
    "UCM": date(2026,6,10),
    "ULL": date(2026,6,15),
}

MANIFESTACIONES = [
    "Soy periodista brillante. Mi maestria es mi destino.",
    "Atraigo excelencia. Mi futuro es luminoso.",
    "Merezco las mejores universidades.",
    "Mi potencial es infinito. Las puertas se abren.",
    "Soy el cambio que el periodismo necesita.",
    "Cada accion construye mi maestria.",
    "Mi historia merece una universidad de elite.",
    "Tengo poder de crear mi futuro.",
    "Las mejores oportunidades vienen a mi.",
    "Mi maestria es mi realidad proxima.",
    "Brillo como la estrella que soy.",
    "Soy candidata excepcional.",
    "Mi vision periodistica es unica.",
    "Atraigo becas y reconocimiento.",
    "El universo conspira a mi favor.",
    "Cada obstaculo es un escalon.",
    "Soy inteligente, creativa y preparada.",
    "Mi futuro es tan brillante.",
    "Merezco lo mejor y lo atrae.",
    "Estoy exactamente donde debo estar.",
    "Mi maestria en Espana es inevitable.",
    "Creo en mi poder.",
    "Soy inversion segura.",
    "Mi pasion es mi superpoder.",
    "Atraigo oportunidades doradas.",
    "Cada deadline me acerca a mi sueno.",
    "Merezco educacion de clase mundial.",
    "Las barreras se disuelven.",
    "Mi maestria ya me espera.",
    "Agradezco al universo.",
    "Soy iman de oportunidades.",
    "Mi potencial asusta.",
    "Llevo excelencia en cada fibra.",
    "Mi futuro es glorioso.",
    "Atraigo mentores y becas.",
    "Soy exactamente lo que buscan.",
    "Mi periodismo cambiara el mundo.",
    "Creo en mi mas que nadie.",
    "Lo mejor sucede para mi.",
    "Mi maestria es mi decision hecha.",
    "Cada celula vibra con exito.",
    "El universo me ama.",
    "Soy digna y lista.",
]

def days_until(d):
    return (d - today).days

frase = MANIFESTACIONES[day_num % len(MANIFESTACIONES)]
urgent = None
min_d = 999
for uni, d in DEADLINES.items():
    days = days_until(d)
    if 0 < days < min_d:
        min_d = days
        urgent = uni

if urgent:
    if min_d <= 7:
        frase += f"\n[URGENTE {urgent}: {min_d} DIAS]"
    elif min_d <= 20:
        frase += f"\n[{urgent}: {min_d} dias]"

lines = []
for uni, d in DEADLINES.items():
    n = days_until(d)
    if 0 < n <= 40:
        emoji = "🔴" if n <= 7 else "🟠" if n <= 20 else "🟡"
        lines.append(f"{emoji} {uni}: {n}d")
for uni, d in OPENS.items():
    n = days_until(d)
    if 0 < n <= 40:
        lines.append(f"🟢 {uni}: +{n}d")

accion = "\n".join(lines) if lines else "Revisa tus aplicaciones"

tesis = ["Lee 2 papers APA","Escribe 300 palabras","Revisa indice","Intro capitulo","5 referencias","Revisa ayer","Conclusiones"][day_num % 7]

clase = " | CLASE 7PM" if weekday == 1 else " | CLASE 9AM" if weekday == 5 else ""
dia = f"{DIAS_ES[weekday]} {today.day} {MESES_ES[today.month-1]}"

msg = f"Aylin!\n{dia}\n{frase}\nTESIS: {tesis}\nMAESTRIAS:\n{accion}{clase}\nTu puedes!"

try:
    cmd = ['osascript', '-e', f'tell application "Messages" to send "{msg}" to buddy "7135132127"']
    subprocess.run(cmd, timeout=10, check=True)
    print("OK iMessage")
except:
    print("FAIL")
