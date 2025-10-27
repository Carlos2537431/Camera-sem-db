import cv2
import threading
import time
import re
import easyocr
import firebase_admin
from difflib import SequenceMatcher
from firebase_admin import credentials, db
# import winsound  # opcional: habilite se quiser som no Windows

# ===== Inicialização do Firebase =====
cred = credentials.Certificate('sitepm-f99ee-firebase-adminsdk-fbsvc-d73ac37b07.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sitepm-f99ee-default-rtdb.firebaseio.com/'
})

# ===== Função para buscar placas no Firebase =====
def verificar_placa_firebase():
    placas_banco = []
    ref1 = db.reference('ocorrencias')
    ocorrencias = ref1.get()
    if ocorrencias:
        for v in ocorrencias.values():
            p = v.get('licensePlate')
            if p:
                placas_banco.append(p.upper())

    ref2 = db.reference('denuncias')
    denuncias = ref2.get()
    if denuncias:
        for v in denuncias.values():
            p = v.get('placa')
            if p:
                placas_banco.append(p.upper())

    return placas_banco

# ===== OCR e regex =====
reader = easyocr.Reader(["en"])
regex_mercosul = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
regex_antigo = re.compile(r"^[A-Z]{3}[0-9]{4}$")

def validar_placa(placa):
    return bool(regex_mercosul.match(placa) or regex_antigo.match(placa))

# ===== Simulação de liberação de catraca =====
def liberar_catraca_simulada(placa):
    print(f"🚦 CATRACA LIBERADA para o veículo {placa}!")
    # Exibe alerta visual na tela
    global alerta_texto, alerta_tempo
    alerta_texto = f"✅ CATRACA LIBERADA: {placa}"
    alerta_tempo = time.time()
    # winsound.Beep(1200, 500)  # som opcional

# ===== Variáveis globais =====
ultimo_frame = None
bbox_detectadas = []  # caixas das placas detectadas
placas_banco = verificar_placa_firebase()
alerta_texto = ""
alerta_tempo = 0
fps = 0.0
lock = threading.Lock()

# ===== Thread da câmera =====
def camera_loop(fonte, nome_janela):
    global ultimo_frame, alerta_texto, alerta_tempo, fps, bbox_detectadas

    cap = cv2.VideoCapture(fonte, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("Erro: não foi possível abrir a câmera.")
        return

    tempo_anterior = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.GaussianBlur(frame, (3, 3), 0)

        # === Calcula FPS ===
        tempo_atual = time.time()
        fps = 1.0 / (tempo_atual - tempo_anterior)
        tempo_anterior = tempo_atual

        # salva o frame atual
        with lock:
            ultimo_frame = frame.copy()

        # === desenha caixas de OCR detectadas ===
        with lock:
            for bbox in bbox_detectadas:
                (top_left, bottom_right, texto) = bbox
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, texto, (top_left[0], top_left[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        # === alerta visual ===
        if time.time() - alerta_tempo < 3 and alerta_texto:
            cv2.putText(frame, alerta_texto, (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.rectangle(frame, (30, 30), (1250, 100),
                          (0, 0, 255), 4)

        # === exibe FPS ===
        cv2.putText(frame, f"FPS: {fps:.1f}", (30, 700),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # mostra vídeo
        cv2.imshow(nome_janela, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ===== Thread de OCR =====
def ocr_loop():
    global ultimo_frame, alerta_texto, alerta_tempo, bbox_detectadas

    while True:
        time.sleep(0.5)  # faz OCR a cada meio segundo

        with lock:
            if ultimo_frame is None:
                continue
            frame_ocr = ultimo_frame.copy()

        gray = cv2.cvtColor(frame_ocr, cv2.COLOR_BGR2GRAY)
        resultados = reader.readtext(gray, detail=1, paragraph=False)

        novas_bboxes = []
        for bbox, texto, conf in resultados:
            placa = texto.upper().replace(" ", "").replace("-", "")
            if validar_placa(placa):
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                novas_bboxes.append((top_left, bottom_right, placa))

                for placa_db in placas_banco:
                    similaridade = SequenceMatcher(None, placa, placa_db).ratio()
                    if similaridade >= 0.8:
                        liberar_catraca_simulada(placa)
                        break

        # atualiza as caixas detectadas
        with lock:
            bbox_detectadas = novas_bboxes

# ===== Execução =====
if __name__ == "__main__":
    t_cam = threading.Thread(target=camera_loop, args=(0, "Câmera AO VIVO"))
    t_ocr = threading.Thread(target=ocr_loop, daemon=True)

    t_cam.start()
    t_ocr.start()

    t_cam.join()
