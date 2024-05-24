import cv2
import time
import sqlite3


# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
)
''')

qrCode = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("no se puede acceder a la camara")
    exit()

while True:
    leido = False
    ret, frame = cap.read()

    if ret:
        ret_qr, decoded_info, points, _ = qrCode.detectAndDecodeMulti(frame)
        if ret_qr:
            for info, point in zip(decoded_info, points):
                if info:
                    color = (0,255,0)
                    if not leido: 
                        print(info, type(info))
                        data = info
                        leido = True
                        time.sleep(2)
                        cursor.execute('''INSERT INTO votes (nombre) VALUES(?)''',(data,))
                        conn.commit()
                else:
                    color = (0,0,255)
                frame = cv2.polylines(frame,[point.astype(int)], True,color,8)
    else:
        print("No se pudo leer el fotograma")
        break
    
    
    cv2.imshow("lector de qr", frame)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()