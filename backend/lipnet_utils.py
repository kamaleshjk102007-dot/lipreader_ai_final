"""LipNet Utilities - Consolidated from notebook and scripts"""
import os
import cv2
import tensorflow as tf
import numpy as np
from typing import List, Tuple

# Setup vocabulary (from notebook)
vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
num_to_char = tf.keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

def load_video(path: str) -> tf.Tensor:
    """
    Load video from path and preprocess frames.
    From notebook cell 9 - enhanced with error handling.
    """
    cap = cv2.VideoCapture(path)
    frames = []
    
    if not cap.isOpened():
        return tf.zeros((75, 46, 140, 1), dtype=tf.float32)
    
    for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
        if not ret:
            break
        frame = tf.image.rgb_to_grayscale(frame)
        frames.append(frame[190:236, 80:220, :])
    cap.release()
    
    if len(frames) == 0:
        return tf.zeros((75, 46, 140, 1), dtype=tf.float32)
    
    mean = tf.math.reduce_mean(frames)
    std = tf.math.reduce_std(tf.cast(frames, tf.float32))
    return tf.cast((frames - mean), tf.float32) / (std + 1e-8)

def load_alignments(path: str) -> tf.Tensor:
    """
    Load alignment file and convert to tokens.
    From notebook cell 15 - enhanced with error handling.
    """
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        tokens = []
        for line in lines:
            line = line.split()
            if len(line) > 2 and line[2] != 'sil':
                tokens = [*tokens, ' ', line[2]]
        return char_to_num(tf.reshape(tf.strings.unicode_split(tokens, input_encoding='UTF-8'), (-1)))[1:]
    except Exception as e:
        print(f"Error loading alignments: {e}")
        return tf.constant([], dtype=tf.int64)

def load_data(path: str) -> Tuple[tf.Tensor, tf.Tensor]:
    """
    Load video and alignments for a given path.
    From notebook cell 16 - enhanced for both tensor and string paths.
    """
    # Handle both tensor and string paths
    if hasattr(path, 'numpy'):
        path = bytes.decode(path.numpy())
    elif isinstance(path, bytes):
        path = path.decode('utf-8')
    
    # Extract file name (Windows compatible)
    file_name = path.split('\\')[-1].split('.')[0]
    if '/' in file_name:
        file_name = file_name.split('/')[-1]
    
    video_path = os.path.join('data', 's1', f'{file_name}.mpg')
    alignment_path = os.path.join('data', 'alignments', 's1', f'{file_name}.align')
    
    frames = load_video(video_path)
    alignments = load_alignments(alignment_path)
    
    return frames, alignments

def mappable_function(path: str):
    """
    Mappable function for TensorFlow dataset.
    From notebook cell 23.
    """
    result = tf.py_function(load_data, [path], (tf.float32, tf.int64))
    return result

def build_model():
    """
    Build LipNet model architecture.
    From notebook cell 38.
    """
    try:
        from tensorflow.keras.models import Sequential  # type: ignore[reportMissingImports]
        from tensorflow.keras.layers import (  # type: ignore[reportMissingImports]
            Conv3D, LSTM, Dense, Dropout, Bidirectional, MaxPool3D,
            Activation, TimeDistributed, Flatten
        )
    except ImportError:
        from keras.models import Sequential
        from keras.layers import (
            Conv3D, LSTM, Dense, Dropout, Bidirectional, MaxPool3D,
            Activation, TimeDistributed, Flatten
        )
    
    model = Sequential()
    model.add(Conv3D(128, 3, input_shape=(75, 46, 140, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1, 2, 2)))
    
    model.add(Conv3D(256, 3, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1, 2, 2)))
    
    model.add(Conv3D(75, 3, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1, 2, 2)))
    
    model.add(TimeDistributed(Flatten()))
    
    model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))
    model.add(Dropout(.5))
    
    model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))
    model.add(Dropout(.5))
    
    model.add(Dense(char_to_num.vocabulary_size() + 1, kernel_initializer='he_normal', activation='softmax'))
    
    return model

def CTCLoss(y_true, y_pred):
    """
    CTC Loss function for training.
    From notebook cell 48.
    """
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")
    
    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    
    loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss

def scheduler(epoch, lr):
    """
    Learning rate scheduler.
    From notebook cell 47.
    """
    if epoch < 30:
        return lr
    else:
        return lr * tf.math.exp(-0.1)

def decode_prediction(yhat, input_length=75):
    """
    Decode model prediction to text.
    From notebook cells 62, 68.
    """
    decoded = tf.keras.backend.ctc_decode(yhat, input_length=[input_length], greedy=True)[0][0].numpy()
    predicted_text = tf.strings.reduce_join([num_to_char(word) for word in decoded[0]]).numpy().decode('utf-8')
    return predicted_text.strip()

def process_video_for_prediction(video_path: str, model):
    """
    Complete pipeline: load video, make prediction, return text.
    Combines notebook functions.
    """
    frames = load_video(video_path)
    video_batch = tf.expand_dims(frames, axis=0)
    yhat = model.predict(video_batch, verbose=0)
    predicted_text = decode_prediction(yhat, input_length=int(frames.shape[0]))
    return predicted_text, frames

# Export all utilities
__all__ = [
    'load_video',
    'load_alignments',
    'load_data',
    'mappable_function',
    'build_model',
    'CTCLoss',
    'scheduler',
    'decode_prediction',
    'process_video_for_prediction',
    'char_to_num',
    'num_to_char',
    'vocab'
]

