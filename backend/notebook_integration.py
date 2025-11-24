"""
Integration module to use notebook functions directly.
This allows the backend to use all functions from LipNet.ipynb
"""
import sys
import os

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Import from our consolidated utilities
from backend.lipnet_utils import (
    load_video,
    load_alignments,
    load_data,
    build_model,
    CTCLoss,
    scheduler,
    decode_prediction,
    process_video_for_prediction,
    char_to_num,
    num_to_char,
    vocab,
    mappable_function
)

# Also import from existing app utilities if they exist
try:
    import sys
    sys.path.append(os.path.join(BASE_DIR, 'app'))
    from utils import load_data as app_load_data
    from modelutil import load_model as app_load_model
except ImportError:
    # If app utilities don't exist, that's okay
    pass

__all__ = [
    'load_video',
    'load_alignments', 
    'load_data',
    'build_model',
    'CTCLoss',
    'scheduler',
    'decode_prediction',
    'process_video_for_prediction',
    'char_to_num',
    'num_to_char',
    'vocab',
    'mappable_function'
]

