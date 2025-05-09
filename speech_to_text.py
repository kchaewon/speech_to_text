# -*- coding: utf-8 -*-
"""Speech_to_Text.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10PpNL4WqLg8tNsqTmrBUUjwpx71XBIV6
"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import librosa
import IPython
import transformers

fileName = '/content/drive/MyDrive/Colab Notebooks/10 Years Later.wav'

IPython.display.Audio(fileName, rate=16000)

# Load audio file
inputAudio, _ = librosa.load(fileName)

# Load Pretrained hubert model
hubertSample = "facebook/hubert-large-ls960-ft"
hubertTokenizer = transformers.Wav2Vec2Processor.from_pretrained(hubertSample)
hubertModel = transformers.HubertForCTC.from_pretrained(hubertSample)

# Load Pretrained wav2vec2 model
wav2vec2Sample = "facebook/wav2vec2-base-960h"
wav2vec2Tokenizer = transformers.Wav2Vec2Processor.from_pretrained(wav2vec2Sample)
wav2vec2Model = transformers.Wav2Vec2ForCTC.from_pretrained(wav2vec2Sample)

# Return PyTorch torch.Tensor for hubert
hubertInputValues = hubertTokenizer(inputAudio, sampling_rate=16000, return_tensors="pt").input_values

# Return PyTorch torch.Tensor for wav2vec2
wav2vec2InputValues = wav2vec2Tokenizer(inputAudio, sampling_rate=16000, return_tensors="pt").input_values

# Get logits & prediction for hubert
hubertLogits = hubertModel(hubertInputValues).logits
hubertPrediction = torch.argmax(hubertLogits, dim=-1)

# Get logits & prediction for wav2vec2
wav2vec2Logits = wav2vec2Model(wav2vec2InputValues).logits
wav2vec2Prediction = torch.argmax(wav2vec2Logits, dim=-1)

# Decode the predictions
hubertTranscript = hubertTokenizer.batch_decode(hubertPrediction)[0].lower()
wav2vec2Transcript = wav2vec2Tokenizer.batch_decode(wav2vec2Prediction)[0].lower()

# Print the transcript for hubert
print(hubertTranscript)

# Print the transcript for wav2vec2
print(wav2vec2Transcript)

"""**Original transcript for comparison:**

I'm reporting live from Newfoundland, for BBC

CBC

CTV

Al Jazeera

For Rogers TV, I'm Janice Mosher

On September 11th, 2011, the town is again filled with come from aways.

On the tenth anniversary, from all around the world, we welcome back: The Plane People!
"""