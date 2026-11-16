from ultralytics import YOLO
import os
import cv2
import time
import game_computer as gc
import game_logic as gl

DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(DIR, "runs", "train-3", "weights", "best.pt")
CAMERA = 0
ROWS = COLS = 3
CONFIDENCE_THRESHOLD = 0.90

def _parse_board(b):
    pb = []
    for row in range(ROWS):
        line = ""
        for col in range(COLS):
            if (row, col) in b:
                name = b[(row, col)][0]
                line += f"{name} "
            else:
                line += "- "
        pb.append(line)
    return ["" if i == "-" else i for i in "".join(pb).split()]

def _update_board(results):
    outb = {}
    for result in results:
        for box in result.boxes:
            name = result.names[int(box.cls)] 
            conf = float(box.conf) 
            coords = box.xywhn.tolist()
            if len(coords) > 0:
                x, y, w, h = coords[0]
                
                row = min( int(y * ROWS), ROWS - 1 ) 
                col = min( int(x * COLS), COLS - 1 )
                
                if (row, col) not in outb or conf > outb[(row, col)][1]:
                    outb[(row, col)] = (name, conf)
    return outb

def main():
    if not os.path.exists(MODEL):
        print(f"Fandt ikke modellen: {MODEL}")
        raise SystemExit
    
    model = YOLO(MODEL)
    cap = cv2.VideoCapture(CAMERA)

    if not cap.isOpened():
        print(f"Kunne ikke åbne kamera {CAMERA}.")
        raise SystemExit
    
    print("\n--- SPILLET ER LIVE ---")
    print("Klik på OpenCV-vinduet og tryk på 1, 2 eller 3 for at lave computertræk.")
    print("Tryk på 'q' for at afslutte.\n")

    while True:
        success, frame = cap.read()
        if not success:
            print("Fik ikke noget billede fra kameraet.")
            break
            
        frame = cv2.flip(frame, 0)
        
        results = model.track(frame, persist=True, verbose=False, conf=CONFIDENCE_THRESHOLD)
        annotated_frame = results[0].plot()
        
        cv2.putText(annotated_frame, "Tryk 1, 2 el. 3 for computertræk. Q for afslut.", 
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 0), 2)
        cv2.imshow("YOLO webcam", annotated_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break
            
        elif key in [ord("1"), ord("2"), ord("3")]:
            diff = chr(key)
            print(f"\n[Valgt svaerhedsgrad: {diff}] Analyserer bræt nu...")
            
            board = _update_board(results)
            parsed_board = _parse_board(board)
            print("Parsed bræt fra livebillede:", parsed_board)

            if gl.check_winner(parsed_board, "X"):
                gl.display_board(parsed_board)
                print("Spiller (X) vandt spillet!")
                continue
            if gl.check_winner(parsed_board, "O"):
                gl.display_board(parsed_board)
                print("Spiller (O) vandt spillet!")
                continue
            if not gl.get_available_moves(parsed_board):
                gl.display_board(parsed_board)
                print("Det blev uafgjort!")
                continue

            
            cmove = ""
            match diff:
                case "1": cmove = gc.easy_move(parsed_board)
                case "2": cmove = gc.medium_move(parsed_board)
                case "3": cmove = gc.hard_move(parsed_board)
                
            parsed_board[cmove] = f"*{gl.get_player_turn(parsed_board)}"
            print(f"Computer move (to index {cmove+1}) marked with star:")
            print(gl.display_board(parsed_board))

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
