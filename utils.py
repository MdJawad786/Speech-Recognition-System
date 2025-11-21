"""
Utility Functions
Helper functions for logging, file operations, etc.
"""

import logging
import os
from datetime import datetime

def setup_logging(log_file='speech_recognition.log', level=logging.INFO):
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
        level: Logging level
        
    Returns: 
        Logger instance
    """
    # Create logger
    logger = logging.getLogger('SpeechToText')
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def save_transcription(text, file_path, append=False):
    """
    Save transcription to file
    
    Args:
        text: Transcribed text
        file_path: Output file path
        append: Whether to append or overwrite
    """
    mode = 'a' if append else 'w'
    
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {text}\n")
            
        logger = setup_logging()
        logger.info(f"Transcription saved to: {file_path}")
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error saving transcription: {e}")
        raise

def format_timestamp(seconds):
    """
    Format seconds to MM:SS format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def check_dependencies():
    """Check if required dependencies are installed"""
    required = {
        'speech_recognition': 'SpeechRecognition',
        'pydub': 'pydub',
        'pyaudio': 'PyAudio'
    }
    
    missing = []
    
    for module, name in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(name)
            
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
        
    return True

def create_output_dir(dir_name='output'):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        logger = setup_logging()
        logger.info(f"Created output directory: {dir_name}")
    return dir_name