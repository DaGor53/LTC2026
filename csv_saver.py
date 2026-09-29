import serial
import csv
import time

PORT = "COM8" #меняется в зависимости от того, куда подключено ардуино

# должно совпадать с Serial.begin() 
BAUDRATE = 500000

FILENAME = "measurement.csv"

ser = serial.Serial(
    PORT,
    BAUDRATE,
    timeout=1
)

time.sleep(2)
ser.reset_input_buffer()

print("Запись началась")
print("Ctrl+C для остановки")
print()


with open(FILENAME, "w", newline="") as file:

    writer = csv.writer(file)
    writer.writerow(["time_us", "A0", "A1"])
    measurements = 0
    skipped = 0

    try:

        while True:
            raw_line = ser.readline()

            if not raw_line:
                continue

            line = raw_line.decode(
                "ascii",
                errors="ignore"
            ).strip()

            if not line:
                continue

            if line == "time_us,A0,A1":
                continue

            parts = line.split(",")
            if len(parts) != 3:
                skipped += 1
                print(f"[SKIP] {line}")
                continue
            
            try:
                time_us = int(parts[0])
                a0 = int(parts[1])
                a1 = int(parts[2])

            except ValueError:
                skipped += 1
                print(f"[SKIP] {line}")
                continue

            if not (0 <= a0 <= 1023):
                skipped += 1
                print(f"[SKIP] неверный A0: {line}")
                continue

            if not (0 <= a1 <= 1023):
                skipped += 1
                print(f"[SKIP] неверный A1: {line}")
                continue

            writer.writerow([
                time_us,
                a0,
                a1
            ])

            measurements += 1
            file.flush()

            print(
                f"#{measurements:6d}  "
                f"t={time_us:8d} us   "
                f"A0={a0:4d}   "
                f"A1={a1:4d}"
            )

    except KeyboardInterrupt:

        print()
        print("Запись остановлена")

    finally:

        ser.close()

print()
print(f"Корректных измерений: {measurements}")
print(f"Пропущено строк:      {skipped}")
print(f"Файл сохранён:        {FILENAME}")