from ultralytics import YOLO
import os
import cv2

DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = os.path.join(DIR, "runs", "train-3", "weights", "best.pt")
IMAGE = os.path.join(
    DIR, "input-test.jpg"
)

def _test_picture(m, img):
    result = m(img)[0] 

    result.save(filename=os.path.join(DIR, "output-test-annotated.jpg"))
    result.show()

def _test_webcam(m, cam):
    cap = cv2.VideoCapture(cam)

    if not cap.isOpened():
        print(f"Kunne ikke åbne kamera {cam}. Prøv et andet tal i CAMERA øverst i scriptet,")
        print("og tjek at andre programmer (Teams, Zoom ...) ikke bruger kameraet.")
        raise SystemExit

    print("Tryk q i webcam-vinduet for at stoppe.")

    # Løkken læser ét billede (frame) ad gangen fra kameraet
    while True:
        success, frame = cap.read()
        if not success:
            print("Fik ikke noget billede fra kameraet.")
            break

        # Tracking: persist=True husker objekterne fra forrige billede, så de beholder deres ID
        results = m.track(frame, persist=True, verbose=False)

        # Tegn kasser, navne og ID'er på billedet og vis det
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO webcam", annotated_frame)

        # Stop, når der trykkes på q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Luk kameraet og vinduet igen
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if not os.path.exists(MODEL):
        print(f"Fandt ikke modellen: {MODEL}")
        print("Har du kørt model-train.py? Se i mappen runs/detect/, hvad din træning hedder.")
        raise SystemExit
    model = YOLO(MODEL)
    #_test_picture(model, IMAGE)
    _test_webcam(model, 0)



