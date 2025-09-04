import cv2
import sqlite3
import easyocr
import threading
import re
import firebase_admin
from difflib import SequenceMatcher
from firebase_admin import credentials, db

# ===== banco de dados =====
def verificar_placa_firebase(placa):
    placas_banco = []
    # Placas do caminho 'ocorrencias' (campo 'licensePlate')
    ref_ocorrencias = db.reference('ocorrencias')
    ocorrencias = ref_ocorrencias.get()
    if ocorrencias:
        for key, value in ocorrencias.items():
            placa_db = value.get('licensePlate')
            if placa_db:
                placas_banco.append(placa_db.upper())
    # Placas do caminho 'denuncias' (campo 'placa')
    ref_denuncias = db.reference('denuncias')
    denuncias = ref_denuncias.get()
    if denuncias:
        for key, value in denuncias.items():
            placa_db = value.get('placa')
            if placa_db:
                placas_banco.append(placa_db.upper())
    return placas_banco

# ===== OCR =====
reader = easyocr.Reader(["en"])  # Ingles funciona bem para OCR de placas por isso ingles (eu tentei portugues, tentei ate mais do que gostaria)

# ===== regex para validar formato mercosul, pra nao pegar qualquer coisa, afinal placa tem padrao =====
regex_mercosul = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
regex_antigo = re.compile(r"^[A-Z]{3}[0-9]{4}$")

def validar_placa(placa):
    """Retorna True se a placa segue o padrão Mercosul ou antigo"""
    return bool(regex_mercosul.match(placa) or regex_antigo.match(placa))

# ===== integração com Firebase =====
cred = credentials.Certificate('sitepm-f99ee-firebase-adminsdk-fbsvc-d73ac37b07.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sitepm-f99ee-default-rtdb.firebaseio.com/'
})

# ===== loop de camera =====
def camera_loop(fonte, nome_janela):
    cap = cv2.VideoCapture(fonte)

    # verifica se a camera/arquivo abriu corretamente
    if not cap.isOpened():
        print(f"Erro: não foi possível abrir a fonte {fonte}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Fim da fonte {fonte}")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resultados = reader.readtext(gray)

        placas_banco = verificar_placa_firebase("")

        for bbox, texto, conf in resultados:
            placa = texto.upper().replace(" ", "").replace("-", "")

            if validar_placa(placa):
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))

                # desenha a caixa da placa
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, placa, (top_left[0], top_left[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # Verifica similaridade com placas do banco
                for placa_db in placas_banco:
                    similaridade = SequenceMatcher(None, placa, placa_db).ratio()
                    if similaridade >= 0.8:  # 80% ou mais de similaridade
                        print(f"ALERTA: Placa parecida encontrada! {placa} ≈ {placa_db}")
                        cv2.putText(frame, f"⚠ ALERTA: PLACA PARECIDA ({placa_db}) ⚠",
                                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 3)
                        # Aqui você pode acionar um alarme real (som, GPIO, etc)
                        break

        cv2.imshow(nome_janela, frame)

        # pressione Q para sair
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()  # fecha todas as janelas de forma segura

# ===== execução =====
if __name__ == "__main__":
    fontes = [
        0,                 # webcam padrão do pc
        # "video.mp4",     # arquivo local (descomente se quiser usar video[descomente so video mp4])
    ]

    threads = []
    for i, fonte in enumerate(fontes):
        t = threading.Thread(target=camera_loop, args=(fonte, f"Camera {i+1}"))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
