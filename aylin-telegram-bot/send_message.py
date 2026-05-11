#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
from datetime import date

BOT_TOKEN = "8743339704:AAHqexQ36eKx9SAXEkLLWGi_WJGK4mzrN38"
CHAT_ID   = "7135132127"

today    = date.today()
weekday  = today.weekday()
day_num  = today.day

DIAS_ES  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
MESES_ES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

DEADLINES = {
    "UHU Huelva":     date(2026,5,18),
    "UA Alicante":    date(2026,6,26),
    "UVa Valladolid": date(2026,7,10),
}
OPENS = {
    "UGR Granada":      date(2026,6,17),
    "USC Santiago":     date(2026,6,23),
    "MUCAII Salamanca": date(2026,6,1),
}
PORTALES = {
    "UHU Huelva":      ("dua.us.es","apostilla del título + formulario DUA"),
    "UA Alicante":     ("UACloud","equivalencia nota media + contactar acces.master@ua.es"),
    "UVa Valladolid":  ("admisionmaster.uva.es","portfolio audiovisual + carta de motivación"),
    "UGR Granada":     ("DUA Andalucía","carta de motivación con líneas de investigación"),
    "USC Santiago":    ("matricula.usc.es","solicitud (puedes pedir 2 másteres a la vez)"),
    "MUCAII Salamanca":("usal.es","2 cartas de recomendación + preinscripción"),
}

def days_until(d): return (d - today).days

FRASES = {
    0:"Soy una periodista peruana brillante. Mi maestría en España ya me está esperando. 🔮",
    1:"Cada acción de hoy me acerca un kilómetro más a mi ciudad europea. ✨",
    2:"Mi historia — ese es mi equipaje perfecto. 💫",
    3:"No necesito verlo todo. Solo dar el siguiente paso. Y hoy lo doy. 🦋",
    4:"Soy capaz, estoy preparada, y me lo merezco. El universo tiene mi nombre escrito. 🌸",
    5:"Cada documento apostillado es energía que el universo registra a mi favor. 🌺",
    6:"Descanso hoy para avanzar mañana con más fuerza. Me lo merezco. 🌙",
}

tesis = "📖 Lee 2 papers sobre tu tema y anota sus citas en APA 7." if day_num%2==0 else "✍️ Escribe mínimo 300 palabras del marco teórico o metodología hoy."

def get_accion():
    lines=[]
    for uni,d in DEADLINES.items():
        n=days_until(d)
        portal,doc=PORTALES[uni]
        if 0<n<=7: lines.append(f"🚨 <b>URGENTE — {uni} cierra en {n} días.</b> Entra AHORA a {portal} ({doc}). ¡No lo dejes para mañana!")
        elif 8<=n<=20: lines.append(f"⚡ <b>{uni} cierra en {n} días.</b> Hoy revisa: {doc} en {portal}.")
        elif 21<=n<=40: lines.append(f"📋 <b>{uni} cierra en {n} días.</b> Prepara: {doc}.")
    for uni,d in OPENS.items():
        n=days_until(d)
        _,doc=PORTALES[uni]
        if 0<n<=30: lines.append(f"🟢 <b>{uni}</b> abre en ~{n} días. Prepara: {doc}.")
    return "\n".join(lines) if lines else "📚 Revisa tus aplicaciones y avanza en el documento más urgente."

def get_estado():
    rows=[]
    for uni,d in DEADLINES.items():
        n=days_until(d)
        rows.append(f"⛔ {uni} → CERRADO" if n<=0 else f"🔴 {uni} → {n} días ⚠️" if n<=7 else f"🟠 {uni} → {n} días")
    for uni,d in OPENS.items():
        n=days_until(d)
        rows.append(f"🟢 {uni} → ABIERTO" if n<=0 else f"🟢 {uni} → abre en ~{n} días")
    return "\n".join(rows)

clase=""
if weekday==1: clase="\n━━━━━━━━━━━━━\n⏰ <b>CLASE HOY a las 7PM</b> 📚 ¡No olvides!\n"
elif weekday==5: clase="\n━━━━━━━━━━━━━\n⏰ <b>CLASE HOY a las 9AM</b> 📚 ¡No olvides!\n"

dia_str=f"{DIAS_ES[weekday]} {today.day} de {MESES_ES[today.month-1]}"

mensaje=f"""🌸 <b>Buenos días, Aylin!</b>
📅 {dia_str}

━━━━━━━━━━━━━
✨ <b>FRASE DEL DÍA</b>
{FRASES[weekday]}

━━━━━━━━━━━━━
📓 <b>TESIS HOY</b>
👉 {tesis}

━━━━━━━━━━━━━
🎓 <b>MAESTRÍAS HOY</b>
{get_accion()}

📊 <b>Estado de deadlines:</b>
{get_estado()}{clase}
━━━━━━━━━━━━━
💪 <i>Un paso a la vez, Aylin. Tú puedes. 🌸</i>"""

url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data=urllib.parse.urlencode({"chat_id":CHAT_ID,"parse_mode":"HTML","text":mensaje}).encode()
req=urllib.request.Request(url,data=data,method="POST")
with urllib.request.urlopen(req,timeout=15) as resp:
    r=json.loads(resp.read())
print("✅ Enviado!" if r.get("ok") else f"❌ Error: {r}")
if not r.get("ok"): raise SystemExit(1)
