"""
Configuration Settings
Centralized configuration for the speech recognition system
"""

import os

# Audio Settings
AUDIO_CONFIG = {
    'sample_rate': 16000,
    'channels': 1,
    'chunk_size': 1024,
    'format': 'int16',
    'default_duration': 5,  # seconds
}

# Recognition Engine Settings
ENGINE_CONFIG = {
    'google': {
        'name': 'Google Speech Recognition',
        'requires_internet': True,
        'languages': ['en-US', 'es-ES', 'fr-FR', 'de-DE', 'ja-JP', 'zh-CN'],
        'default_language': 'en-US'
    },
    'sphinx': {
        'name': 'CMU Sphinx',
        'requires_internet': False,
        'languages': ['en-US'],
        'default_language': 'en-US'
    },
    'wav2vec2': {
        'name': 'Wav2Vec2',
        'requires_internet': False,  # After model download
        'model': 'facebook/wav2vec2-base-960h',
        'languages': ['en'],
        'default_language': 'en'
    }
}

# Model Settings
MODEL_CONFIG = {
    'wav2vec2': {
        'model_name': 'facebook/wav2vec2-base-960h',
        'cache_dir': './models',
        'device': 'auto',  # 'auto', 'cpu', or 'cuda'
    }
}

# File Paths
PATHS = {
    'output_dir': './output',
    'logs_dir': './logs',
    'models_dir': './models',
    'temp_dir': './temp',
    'log_file': './logs/speech_recognition.log'
}

# Create directories if they don't exist
for path in PATHS.values():
    if path.endswith(('.log', '.txt')):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': PATHS['log_file'],
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Supported Audio Formats
SUPPORTED_FORMATS = [
    '.wav', '.mp3', '.flac', '.ogg', 
    '.m4a', '.wma', '.aac', '.opus'
]

# Language Codes
LANGUAGE_CODES = {
    'English (US)': 'en-US',
    'English (UK)': 'en-GB',
    'Spanish': 'es-ES',
    'French': 'fr-FR',
    'German': 'de-DE',
    'Italian': 'it-IT',
    'Japanese': 'ja-JP',
    'Chinese (Simplified)': 'zh-CN',
    'Korean': 'ko-KR',
    'Portuguese': 'pt-BR',
    'Russian': 'ru-RU',
    'Arabic': 'ar-SA'
}

# Performance Settings
PERFORMANCE = {
    'max_file_size_mb': 100,
    'timeout_seconds': 30,
    'max_audio_length_seconds': 300,
    'energy_threshold': 4000,
    'dynamic_energy_threshold': True,
    'pause_threshold': 0.8
}