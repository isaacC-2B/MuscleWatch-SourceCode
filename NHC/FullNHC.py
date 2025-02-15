import time
import board
import digitalio
import pwmio
from bluepy import btle
import adafruit_character_lcd.character_lcd as characterlcd
import numpy as np
import tensorflow as tf

lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_rw = digitalio.DigitalInOut(board.D4)

red = pwmio.PWMOut(board.D21)
green = pwmio.PWMOut(board.D12)
blue = pwmio.PWMOut(board.D18)

lcd = characterlcd.Character_LCD_RGB(
    lcd_rs,
    lcd_en,
    lcd_d4,
    lcd_d5,
    lcd_d6,
    lcd_d7,
    lcd_columns,
    lcd_rows,
    red,
    green,
    blue,
    lcd_rw,
)

mac_address = "f4:12:fa:68:ea:59"
service_uuid = "12345678-1234-5678-1234-56789abcdef0"
bf_uuid = "12345678-1234-5678-1234-56789abcdef1"
st_uuid = "12345678-1234-5678-1234-56789abcdef2"

model = tf.keras.models.load_model('lr0.1.keras')

bf_data = []
st_data = []

def categorize_sample(sample_data, max_value):
    avg_value = np.mean(sample_data)
    
    if avg_value == 0:
        return 0
    
    percentage = (avg_value / max_value) * 100
    
    if percentage < 10:
        return 1
    elif percentage < 20:
        return 2
    elif percentage < 30:
        return 3
    elif percentage < 40:
        return 4
    elif percentage < 50:
        return 5
    elif percentage < 60:
        return 6
    elif percentage < 70:
        return 7
    elif percentage < 80:
        return 8
    elif percentage < 90:
        return 9
    else:
        return 10

# Edit max_value to desired average
max_value = 65

try:
    lcd.color = [0, 0, 100]
    lcd.message = "Connecting...\nPlease wait"
    print("Connecting to device...")
    
    device = btle.Peripheral(mac_address)
    print("Connected")

    lcd.message = "Connected!\nMonitoring..."
    time.sleep(2)

    service = device.getServiceByUUID(service_uuid)
    bf = service.getCharacteristics(bf_uuid)[0]
    st = service.getCharacteristics(st_uuid)[0]
    
    rep_count = 0
    while True:
        try:
            bf_value = int.from_bytes(bf.read(), byteorder='little')
            st_value = int.from_bytes(st.read(), byteorder='little')

            bf_data.append(bf_value)
            st_data.append(st_value)

            if len(bf_data) >= 64 and len(st_data) >= 64:
                combined_data = bf_data[:64] + st_data[:64]  # Ensure we have exactly 128 elements
                rpe = categorize_sample(combined_data, max_value)
                print(f"Combined data length: {len(combined_data)}")
                
                model_input = np.array(combined_data).reshape(1, 128)
                prediction = model.predict(model_input)
                prediction_value = prediction[0][0]
                print(f"Predicted Class: {prediction_value}")
                print(f"Categorized into RPE: {rpe}")

                if rpe == 0:
                    lcd.clear()
                    lcd.color = [255, 255, 255]
                    lcd.message = f"No Activity\nRCT: {rep_count} RPE: {rpe}"
                    print("No Activity")
                    print(f"Rep count: {rep_count}")

                elif prediction_value >= 0.5:
                    lcd.clear()
                    rep_count += 1
                    lcd.color = [0, 100, 0]
                    lcd.message = f"Proper NHC\nRCT: {rep_count} RPE: {rpe}"
                    print("Proper NHC")
                    print(f"Rep Count: {rep_count}")
                else:
                    lcd.clear()
                    lcd.color = [100, 0, 0]
                    lcd.message = f"Improper NHC\nRCT: {rep_count} RPE: {rpe}"
                    print("Improper NHC")
                    print(f"Rep Count: {rep_count}")
                
                bf_data.clear()
                st_data.clear()

        except btle.BTLEException as e:
            print(f"Bluetooth error: {e}")
            break

        except Exception as e:
            print(f"An error occurred: {e}")
            lcd.clear()
            lcd.message = "Error occurred\nTry again"

except Exception as e:
    print(f"An error occurred: {e}")
    lcd.clear()
    lcd.message = "Error occurred\nTry again"