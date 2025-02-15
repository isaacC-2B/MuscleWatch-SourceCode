/*
 * Copyright 2017, OYMotion Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
 * THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.

 * Code partially generated with the help of ChatGPT (OpenAI, 2025)
 * https://www.openai.com/chatgpt

 * Code partially generated with the help of CS50.ai (Harvard University, 2025)
 * https://www.cs50.ai/chat
*/

/*
 * Version 6C FinalArduinoCode
*/
#include <ArduinoBLE.h>
#include "EMGFilters.h"
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#define SensorInputPin0 A0
#define SensorInputPin1 A1

EMGFilters myFilter;
SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_1000HZ;
NOTCH_FREQUENCY humFreq = NOTCH_FREQ_60HZ;

const int windowSize = 4;  // Define the window size for RMS calculation

const int downsamplingFactor = 4;  // Downsampling factor (take every 4th sample) 4-8 works best: 4 for fast excercises & 8 for slower ones 
int downsampledData0[64];  // Array to store downsampled data for sensor 0
int downsampledData1[64];  // Array to store downsampled data for sensor 1
int dataIndex = 0;  // Index for storing downsampled data

int arr0[windowSize];  // Array to store samples for sensor 0
int arr1[windowSize];  // Array to store samples for sensor 1
int cumSqSum0 = 0;  // Cumulative sum for sensor 0
int cumSqSum1 = 0;  // Cumulative sum for sensor 1
const int Threshold = 120000; // 120000-140000 works best

BLEService hamstringService("12345678-1234-5678-1234-56789abcdef0");
BLEIntCharacteristic BFHamstringChar("12345678-1234-5678-1234-56789abcdef1", BLERead | BLENotify);
BLEIntCharacteristic STHamstringChar("12345678-1234-5678-1234-56789abcdef2", BLERead | BLENotify);

void setup() {
    myFilter.init(sampleRate, humFreq, true, false, true);  
    Serial.begin(115200);
    while (!Serial);  // Wait for serial to be ready

    if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
    }

    hamstringService.addCharacteristic(BFHamstringChar);
    hamstringService.addCharacteristic(STHamstringChar);
    BLE.addService(hamstringService);
    BLE.advertise();

    Serial.println("BLE device active, waiting for connections...");
}

void loop() {
  BLEDevice central = BLE.central();
    
  if (central) { 
    Serial.print("Connected to ");
    Serial.println(central.address());
  
  while (central.connected()){
    static int i = 0;  // Static variable to keep track of the current sample

    int Value0 = analogRead(SensorInputPin0);  // Read sensor 0
    int Value1 = analogRead(SensorInputPin1);  // Read sensor 1

    int envelope0 = sq(Value0);  // Apply the envelope logic (squared data after filtering)
    int envelope1 = sq(Value1);

    if (envelope0 < Threshold){
        envelope0 = 0;
    }

    if (envelope1 < Threshold){
        envelope1 = 0;
    }    

    arr0[i] = envelope0;  // Store the squared data for sensor 0
    arr1[i] = envelope1;  // Store the squared data for sensor 1

    // Update the cumulative sum for RMS calculation
    cumSqSum0 += arr0[i];
    cumSqSum1 += arr1[i];

    // Calculate RMS after collecting enough samples
    float rms0 = 0;
    float rms1 = 0;

    if (i == windowSize - 1) {
        rms0 = sqrt((float)cumSqSum0 / windowSize);  // Calculate RMS for sensor 0
        rms1 = sqrt((float)cumSqSum1 / windowSize);  // Calculate RMS for sensor 1

        // Perform downsampling by storing every nth sample (every 4th sample in this case)
        if (dataIndex < 64) {
            if (dataIndex % downsamplingFactor == 0) {  // Every 4th sample
                downsampledData0[dataIndex] = (int)rms0;  // Store the downsampled data for sensor 0
                downsampledData1[dataIndex] = (int)rms1;  // Store the downsampled data for sensor 1
                //Serial.print("DataIndex: ");
                //Serial.print(dataIndex);  // Print current data index
                // Print downsampled values
                //Serial.print(" Downsampled Sensor 0: ");
                BFHamstringChar.writeValue(downsampledData0[dataIndex]);
                STHamstringChar.writeValue(downsampledData1[dataIndex]);                
                Serial.print(downsampledData0[dataIndex]);
                Serial.print(" , ");
                Serial.println(downsampledData1[dataIndex]);
            }
        }

        // Increment dataIndex after storing a sample
        dataIndex++;

        // If dataIndex exceeds 64, shift the data to make room for new downsampled values
        if (dataIndex >= 64) {
            for (int j = 4; j < 64; j++) {
                downsampledData0[j - 4] = downsampledData0[j];  // Shift left by 4 or 8
                downsampledData1[j - 4] = downsampledData1[j];  // Shift left by 4 or 8
            }
            dataIndex = 60; // Reset dataIndex to 56 or 60 to allow for more downsampling
        }

        // Reset the cumulative sums for the next window
        cumSqSum0 = 0;
        cumSqSum1 = 0;
        i = 0;  // Reset sample index to start the next window of data
    } else {
        i++;  // Increment sample index to collect samples for the current window
     }
    }
  }
    delayMicroseconds(1000);  // Add a short delay to allow for serial output to be visible
}