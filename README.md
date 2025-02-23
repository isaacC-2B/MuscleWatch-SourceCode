# “MuscleWatch Source Code”

This is the source code for my “MuscleWatch device” which aims to prevent hamstring injury along with the Neuromuscular Training (NMT) warm up program developed by researchers at the University of Calgary.

Each of the 3 folders contains the machine learning model for each NMT warm up exercise, code, and EMG data used to train it. The arduino code is run on the leg sleeve of the physical device and is used to filter and relay the EMG data to either of the 3 machine learning models (found in folders: APB, NHC, and SQJ). If you find any errors, feel free to open up an “issue” or send a “pull request”! 

Deployment Date: February 14, 2025

# Credits:

Code partially generated with the help of:
ChatGPT (OpenAI, 2025)
https://www.openai.com/chatgpt

CS50.ai (Harvard University, 2025)
https://www.cs50.ai/chat

# Special Thanks to:

"Tensorflow Tutorial for Python in 10 Minutes" (Nicholas Renotte, 2020)
https://www.youtube.com/watch?v=6_2hzRopPbQ
For teaching me how to use Tensorflow as a tool to create binary classification machine learning models from data in CSV files.

An Emphasis on the Minimization of False Negatives & False Positives in Binary Classification (Sanskriti Singh, 2025)
https://medium.com/@Sanskriti.Singh/an-emphasis-on-the-minimization-of-false-negatives-false-positives-in-binary-classification-9c22f3f9f73
For inspiring the idea to modify the threshold line at which the result of my machine learning model is considered a positive or a negative. This helped me increase the accuracy of my model when tested on the validation and testing data sets. 

Keras (François Chollet, 2017)
https://keras.io/
For developing the Keras deep-learning library and providing it, along with examples and use cases for free! 

# Copyright:
MIT License

Copyright (c) 2017 François Chollet

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


Version number 1, Version date: February 23, 2025 
