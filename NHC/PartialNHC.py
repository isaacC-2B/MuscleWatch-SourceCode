# Code partially generated with the help of ChatGPT (OpenAI, 2025)
# https://www.openai.com/chatgpt

# Code partially generated with the help of CS50.ai (Harvard University, 2025)
# https://www.cs50.ai/chat

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
left_hamstring_uuid = "12345678-1234-5678-1234-56789abcdef1"
right_hamstring_uuid = "12345678-1234-5678-1234-56789abcdef2"

model = tf.keras.models.load_model('lr0.1.keras')

bf_data = []
st_data = []

try:
    lcd.color = [0, 0, 100]
    lcd.message = "Connecting...\nPlease wait"
    print("Connecting to device...")
    device = btle.Peripheral(mac_address)
    print("Connected")

    lcd.message= ("Connected!\nMonitoring...")
    time.sleep(2)

    service = device.getServiceByUUID(service_uuid)
    left_hamstring = service.getCharacteristics(left_hamstring_uuid)[0]
    right_hamstring = service.getCharacteristics(right_hamstring_uuid)[0]
    
    rep_count = 0
    while True:
        try:
            left_value = int.from_bytes(left_hamstring.read(), byteorder='little')
            right_value = int.from_bytes(right_hamstring.read(), byteorder='little')

            bf_data.append(left_value)
            st_data.append(right_value)       

            if len(bf_data) >= 64 and len(st_data) >= 64:
                combined_data = bf_data[:64] + st_data[:64]
                print(f"Combined data length: {len(combined_data)}")
                
                model_input = np.array(combined_data).reshape(1, 128)
                prediction = model.predict(model_input)
                prediction_value = prediction[0][0]
                
                print(f"Predicted Class: {prediction_value}")
                
                if prediction_value >= 0.5:
                    lcd.clear()
                    lcd.color = [0, 100, 0]
                    lcd.message = (f"Proper NHC\nRep count: {rep_count}")
                    print("Proper NHC")
                    rep_count += 1
                    print(f"Rep Count: {rep_count}")
                else:
                    lcd.clear()
                    lcd.color = [100, 0, 0]
                    lcd.message = (f"Improper NHC\nRep count: {rep_count}")
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