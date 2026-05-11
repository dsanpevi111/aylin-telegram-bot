#!/usr/bin/env python3
"""
Mensaje diario de Aylin — GitHub Actions
Calcula la fecha, construye el mensaje y lo envía por Telegram.
"""

import urllib.request
import urllib.parse
import json
from datetime import date

# ─── CONFIGURACIÓN ────────────────────────────────────────────────
BOT_TOKEN = "8743339704:AAHqexQ36eKx9SAXEkLLWGi_WJGK4mzrN38"
CHAT_ID   = "7135132127"

# ─── FECHA DE HOY ─────────────────────────────────────────────────
today    = date.today()
weekday  = today.weekday()   # 0=lunes … 6=domingo
day_num  = today.day         # para par/impar

DIAS_ES  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
MESES_ES = ["enero","febrero","marzo","abril","mayo","junio",
            "julio","agosto","septiembre","octubre","noviembre","diciembre"]

# ─── DEADLINES ────────────────────────────────────────────────────
DEADLINES = {
    "UHU Huelva":      date(2026,  5, 18),
    "UA Alicante":     date(2026,  6, 26),
    "UVa Valladolid":  date(2026,  7, 10),
}
OPENS = {
    "UGR Granada":      date(2026,  6, 17),
    "USC Santiago":     date(2026,  6, 23),
    "MUCAII Salamanca": date(2026,  6,  1),
}
PORTALES = {
    "UHU Huelva":      ("dua.us.es",             "apostilla del título + formulario DUA"),
    "UA Alicante":     ("UACloud",                "equivalencia nota media + contactar acces.master@ua.es"),
    "UVa Valladolid":  ("admisionmaster.uva.es",  "portfolio audiovisual + carta de motivación"),
    "UGR Granada":     ("DUA Andalucía",          "carta de motivación con líneas de investigación"),
    "USC Santiago":    ("matricula.usc.es",       "solicitud (puedes pedir 2 másteres a la vez)"),
    "MUCAII Salamanca":("usal.es",                "2 cartas de recomendación + preinscripción"),
}

def days_until(d):
    return (d - today).days

# ─── FRASE DEL DÍA ────────────────────────────────────────────────
FRASES = {
    0: "Soy una periodista peruana brillante. Mi maestría en España ya me está esperando. 🔮",
    1: "Cada acción de hoy me acerca un kilómetro más a mi ciudad europea. ✨",
    2: "Mi historia — ese es mi equipaje perfecto. 💫",
    3: "No necesito verlo todo. Solo dar el siguiente paso. Y hoy lo doy. 🦋",
    4: "Soy capaz, estoy preparada, y me lo merezco. El universo tiene mi nombre escrito. 🌸",
    5: "Cada documento apostillado es energía que el universo registra a mi favor. 🌺",
    6: "Descanso hoy para avanzar mañana con más fuerza. Me lo merezco. 🌙",
}

# ─── TESIS ────────────────────────────────────────────────────────
tesis = ("📖 Lee 2 papers sobre tu tema y anota sus citas en APA 7."
         if day_num % 2 == 0
         else "✍️ Escribe mínimo 300 palabras del marco teórico o metodología hoy.")

# ─── ACCIÓN DE MAESTRÍAS ──────────────────────────────────────────
def get_maestria_accion():
    lines = []
    # Urgente: ≤7 días (deadlines abiertos)
    for uni, d in DEADLINES.items():
        n = days_until(d)
        if 0 < n <= 7:
            portal, doc = PORTALES[uni]
            lines.append(
                f"🚨 <b>URGENTE — {uni} cierra en {n} día{'s' if n>1 else ''}.</b> "
                f"Entra AHORA a {portal} y completa tu solicitud ({doc}). ¡No lo dejes para mañana!"
            )
    # Prioritario: 8-20 días
    for uni, d in DEADLINES.items():
        n = days_until(d)
        if 8 <= n <= 20:
            portal, doc = PORTALES[uni]
            lines.append(
                f"⚡ <b>{uni} cierra en {n} días ({d.strftime('%d/%m')}).</b> "
                f"Hoy: revisa que tengas <i>{doc}</i> listo y envía tu solicitud en {portal}."
            )
    # Preparación: 21-40 días
    for uni, d in DEADLINES.items():
        n = days_until(d)
        if 21 <= n <= 40:
            portal, doc = PORTALES[uni]
            lines.append(
                f"📋 <b>{uni} cierra en {n} días.</b> Hoy prepara: {doc} ({portal})."
            )
    # Anticipación: abre pronto (≤30 días)
    for uni, d in OPENS.items():
        n = days_until(d)
        if 0 < n <= 30:
            _, doc = PORTALES[uni]
            lines.append(
                f"🟢 <b>{uni}</b> abre inscripciones en ~{n} días (~{d.strftime('%d/%m')}). "
                f"Prepara ya: {doc}."
            )
    if not lines:
        # Fallback genérico
        lines.append("📚 Revisa el estado de tus aplicaciones y avanza en el documento más urgente.")
    return "\n".join(lines)

# ─── ESTADO DE DEADLINES ──────────────────────────────────────────
def deadline_status():
    rows = []
    for uni, d in DEADLINES.items():
        n = days_until(d)
        if n <= 0:
            rows.append(f"⛔ {uni} → CERRADO")
        elif n <= 7:
            rows.append(f"🔴 {uni} → {n} días ⚠️ URGENTE")
        else:
            rows.append(f"🟠 {uni} → {n} días")
    for uni, d in OPENS.items():
        n = days_until(d)
        if n <= 0:
            rows.append(f"🟢 {uni} → ABIERTO")
        else:
            rows.append(f"🟢 {uni} → abre en ~{n} días")
    return "\n".join(rows)

# ─── CLASE HOY ────────────────────────────────────────────────────
clase_bloque = ""
if weekday == 1:  # martes
    clase_bloque = "\n━━━━━━━━━━━━━\n⏰ <b>CLASE HOY a las 7PM</b> 📚 ¡No olvides!\n"
elif weekday == 5:  # sábado
    clase_bloque = "\n━━━━━━━━━━━━━\n⏰ <b>CLASE HOY a las 9AM</b> 📚 ¡No olvides!\n"

# ─── CONSTRUIR MENSAJE ────────────────────────────────────────────
dia_str  = f"{DIAS_ES[weekday]} {today.day} de {MESES_ES[today.month - 1]}"
frase    = FRASES[weekday]
accion   = get_maestria_accion()
estado   = deadline_status()

mensaje = f"""🌸 <b>Buenos días, Aylin!</b>
📅 {dia_str}

━━━━━━━━━━━━━
✨ <b>FRASE DEL DÍA</b>
{frase}

━━━━━━━━━━━━━
📓 <b>TESIS HOY</b>
👉 {tesis}

━━━━━━━━━━━━━
🎓 <b>MAESTRÍAS HOY</b>
{accion}

📊 <b>Estado de deadlines:</b>
{estado}{clase_bloque}
━━━━━━━━━━━━━
💪 <i>Un paso a la vez, Aylin. Tú puedes. 🌸</i>"""

# ─── ENVIAR A TELEGRAM ────────────────────────────────────────────
def send_telegram(text):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id":    CHAT_ID,
        "parse_mode": "HTML",
        "text":       text,
    }).encode()
    req  = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    return result

if __name__ == "__main__":
    print("Enviando mensaje para:", dia_str)
    print("─" * 40)
    print(mensaje)
    print("─" * 40)
    result = send_telegram(mensaje)
    if result.get("ok"):
        print("✅ Mensaje enviado exitosamente!")
    else:
        print("❌ Error:", result)
        raise SystemExit(1)
