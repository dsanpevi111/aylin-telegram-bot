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

def days_until(d): 
    return (d - today).days

def get_frase_principal():
    urgent_deadline = None
    urgent_uni = None
    min_days = float('inf')
    
    for uni, deadline in DEADLINES.items():
        days = days_until(deadline)
        if days > 0 and days < min_days:
            min_days = days
            urgent_deadline = deadline
            urgent_uni = uni
    
    if urgent_uni:
        if min_days <= 7:
            frases = [
                f"🚨 {urgent_uni} CIERRA EN {min_days} DÍAS. ¡ACCIÓN AHORA!",
                f"⚡ Mi maestría en {urgent_uni} no espera. Hoy envío mis documentos.",
                f"🔴 {min_days} días para {urgent_uni}. No procrastino más. 💪",
                f"⏰ {urgent_uni}: {min_days} días. Cada minuto cuenta hoy. ⚡",
                f"🎯 {min_days} días para mi futuro en {urgent_uni}. Actúo YA. 🔥",
            ]
            return frases[day_num % len(frases)]
        elif min_days <= 20:
            frases = [
                f"💫 {urgent_uni} en {min_days} días. Estoy lista, preparada y motivada. ✨",
                f"🌟 Mi maestría en {urgent_uni} está cada vez más cerca. Avanzo firme.",
                f"🎓 {min_days} días para {urgent_uni}. Cada paso me acerca a mi sueño. 🌸",
                f"💖 Voy a lograrlo en {urgent_uni}. Mi esfuerzo vale la pena. 🦋",
                f"✨ {min_days} días. Mi historia me lleva a {urgent_uni}. Sigo adelante.",
            ]
            return frases[day_num % len(frases)]
        elif min_days <= 40:
            frases = [
                f"📋 {min_days} días para {urgent_uni}. Preparo todo con calma y seguridad.",
                f"🌱 Mi preparación para {urgent_uni} florece cada día. Voy bien. 🌸",
                f"✍️ {min_days} días. Documento a documento, me acerco a {urgent_uni}.",
                f"🏗️ Construyo mi candidatura para {urgent_uni}. Un paso a la vez. 💪",
                f"📚 {min_days} días. Tengo tiempo para brillar en {urgent_uni}. 🌟",
            ]
            return frases[day_num % len(frases)]
    
    closest_open_uni = None
    min_open_days = float('inf')
    for uni, open_date in OPENS.items():
        days = days_until(open_date)
        if 0 < days <= 40 and days < min_open_days:
            min_open_days = days
            closest_open_uni = uni
    
    if closest_open_uni:
        frases = [
            f"🟢 ¡{closest_open_uni} abre en {min_open_days} días! Me preparo emocionada. 🎉",
            f"🚀 {min_open_days} días para que {closest_open_uni} se abra. ¡Lo espero! ✨",
            f"💝 Próximamente: {closest_open_uni} en {min_open_days} días. Estoy lista. 🌟",
            f"🎊 {closest_open_uni} casi aquí. Estos {min_open_days} días son para brillar. 💫",
            f"🌈 {min_open_days} días para {closest_open_uni}. Mi corazón está listo. 💖",
        ]
        return frases[day_num % len(frases)]
    
    frases_default = [
        "Soy una periodista peruana brillante. Mi maestría en España ya me está esperando. 🔮",
        "Cada acción de hoy me acerca un kilómetro más a mi ciudad europea. ✨",
        "Mi historia es mi equipaje perfecto. 💫",
        "No necesito verlo todo. Solo el siguiente paso. Y hoy lo doy. 🦋",
        "Soy capaz. Estoy lista. Me lo merezco. 🌸",
    ]
    return frases_default[day_num % len(frases_default)]

def get_accion():
    lines=[]
    for uni,d in DEADLINES.items():
        n=days_until(d)
        portal,doc=PORTALES[uni]
        if 0<n<=7: 
            lines.append(f"🚨 URGENTE {uni} en {n} días: {doc}")
        elif 8<=n<=20: 
            lines.append(f"⚡ {uni} en {n} días: revisa {doc}")
        elif 21<=n<=40: 
            lines.append(f"📋 {uni} en {n} días: prepara {doc}")
    
    for uni,d in OPENS.items():
        n=days_until(d)
        _,doc=PORTALES[uni]
        if 0<n<=40: 
            lines.append(f"🟢 {uni} abre en {n} días: {doc}")
    
    return "\n".join(lines) if lines else "Revisa tus aplicaciones."

def get_estado():
    rows=[]
    for uni,d in DEADLINES.items():
        n=days_until(d)
        emoji="⛔" if n<=0 else "🔴" if n<=7 else "🟠" if n<=20 else "🟡"
        rows.append(f"{emoji} {uni} → {n} días")
    for uni,d in OPENS.items():
        n=days_until(d)
        emoji="🟢" if n<=0 else "🟢"
        rows.append(f"{emoji} {uni} → abre {n} días")
    return "\n".join(rows)

acciones_tesis = [
    "📖 Lee 2 papers sobre tu tema y anota sus citas en APA 7.",
    "✍️ Escribe 300 palabras del marco teórico o metodología.",
    "🔍 Revisa tu índice y ajusta según feedback.",
    "📝 Escribe la introducción de uno de tus capítulos.",
    "📚 Busca 5 nuevas referencias académicas.",
    "✅ Revisa y corrige lo que escribiste ayer.",
    "💭 Reflexiona: ¿qué conclusión quiero para el lector?",
]
tesis = acciones_tesis[day_num % len(acciones_tesis)]

clase=""
if weekday==1: clase="\n⏰ CLASE HOY 7PM"
elif weekday==5: clase="\n⏰ CLASE HOY 9AM"

dia_str=f"{DIAS_ES[weekday]} {today.day} de {MESES_ES[today.month-1]}"

mensaje=f"""🌸 Buenos días, Aylin!
{dia_str}

{get_frase_principal()}

{tesis}

{get_accion()}

{get_estado()}{clase}

💪 Un paso a la vez. Tú puedes."""

url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data=urllib.parse.urlencode({"chat_id":CHAT_ID,"parse_mode":"HTML","text":mensaje}).encode()
req=urllib.request.Request(url,data=data,method="POST")

try:
    with urllib.request.urlopen(req,timeout=15) as resp:
        r=json.loads(resp.read())
    print("✅ Enviado!" if r.get("ok") else f"❌ Error: {r.get('description')}")
except Exception as e:
    print(f"❌ Error: {e}")
    raise SystemExit(1)
