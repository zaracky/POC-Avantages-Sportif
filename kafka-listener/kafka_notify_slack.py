import os
import requests
import psycopg2

def get_nom_prenom(id_salarie):
    try:
        conn = psycopg2.connect(
            dbname="sportdb",
            user="user",
            password="password",
            host="postgres",
            port=5432
        )
        with conn.cursor() as cur:
            cur.execute("SELECT prenom, nom FROM rh WHERE id_salarie = %s", (id_salarie,))
            result = cur.fetchone()
            return result if result else ("Quelqu’un", "")
    except Exception as e:
        print(f"❌ Erreur DB: {e}")
        return ("Quelqu’un", "")
    finally:
        conn.close()

def envoyer_message_slack(activity):
    payload = activity.get("payload", {}).get("after", {})
    if not payload:
        return

    id_salarie = payload.get("id_salarie")
    prenom, nom = get_nom_prenom(id_salarie)

    distance = int(payload.get("distance_m", 0)) / 1000
    duree = int(payload.get("duree_s", 0))
    type_activite = payload.get("type", "").lower()
    commentaire = payload.get("commentaire", "")

    minutes = duree // 60
    km = round(distance, 1)

    if type_activite == "course":
        msg = f"🔥 Bravo {prenom} {nom} ! Tu viens de courir {km} km en {minutes} min ! Quelle énergie ! 🏅"
    elif type_activite == "marche":
        msg = f"🚶 {prenom} {nom} a fait une belle marche de {km} km en {minutes} min ! Continue comme ça ! 💪"
    elif type_activite == "vélo":
        msg = f"🚴 {prenom} {nom} a pédalé sur {km} km en {minutes} min ! Super effort ! 🛤"
    elif type_activite == "yoga":
        msg = f"🧘 Sérénité et souplesse pour {prenom} {nom} avec une session de yoga de {minutes} minutes. Namaste 🙏"
    elif type_activite == "natation":
        msg = f"🏊 {prenom} {nom} a nagé {km} km en {minutes} min ! Comme un poisson dans l’eau 🐟"
    else:
        msg = f"🏃 {prenom} {nom} a pratiqué une activité ({type_activite}) sur {km} km en {minutes} min."

    if commentaire:
        msg += f' 🗨 "{commentaire}"'

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL non défini.")
        return

    response = requests.post(webhook_url, json={"text": msg})
    print(f"📤 Slack status: {response.status_code}")
