"""
Speech Recognition Engine Handler
Supports Google, Sphinx, and Wav2Vec2 recognition
"""

import speech_recognition as sr
import torch
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC
from config import ENGINE_CONFIG, MODEL_CONFIG
from utils import setup_logging


class SpeechRecognizer:
    """Speech Recognizer supporting multiple engines"""

    def __init__(self, engine="google", language="en-US"):
        """
        Initialize the recognizer.

        Args:
            engine (str): Recognition engine: google, sphinx, wav2vec2
            language (str): Language code
        """

        self.engine = engine.lower()
        self.language = language
        self.logger = setup_logging()
        self.recognizer = sr.Recognizer()

        if self.engine not in ENGINE_CONFIG:
            self.logger.error(f"Invalid engine selected: {self.engine}")
            raise ValueError(f"Unsupported engine '{self.engine}'")

        # Load Wav2Vec2 only when required
        if self.engine == "wav2vec2":
            self._load_wav2vec2_model()

    # -------------------------------------------------------
    # Wav2Vec2 Model Loader
    # -------------------------------------------------------
    def _load_wav2vec2_model(self):
        """Load Wav2Vec2 model (offline engine)"""

        config = MODEL_CONFIG["wav2vec2"]
        model_name = config["model_name"]

        # Select device automatically
        if config["device"] == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            device = config["device"]

        self.device = torch.device(device)
        self.logger.info(f"Loading Wav2Vec2 model on {self.device}...")

        try:
            self.tokenizer = Wav2Vec2Tokenizer.from_pretrained(
                model_name,
                cache_dir=config["cache_dir"]
            )
            self.model = Wav2Vec2ForCTC.from_pretrained(
                model_name,
                cache_dir=config["cache_dir"]
            ).to(self.device)

            self.logger.info("Wav2Vec2 model loaded successfully!")

        except Exception as e:
            self.logger.error(f"Error loading Wav2Vec2 model: {e}")
            raise

    # -------------------------------------------------------
    # Main Recognition Function
    # -------------------------------------------------------
    def recognize(self, audio_data):
        """
        Recognize speech from audio_data (AudioData object)
        """

        try:
            if self.engine == "google":
                return self._recognize_google(audio_data)

            elif self.engine == "sphinx":
                return self._recognize_sphinx(audio_data)

            elif self.engine == "wav2vec2":
                return self._recognize_wav2vec2(audio_data)

        except Exception as e:
            self.logger.error(f"Recognition error: {e}")
            return None

    # -------------------------------------------------------
    # Google Speech Recognition
    # -------------------------------------------------------
    def _recognize_google(self, audio_data):
        """Recognize using Google Web Speech API"""

        self.logger.info("Using Google Speech Recognition...")

        return self.recognizer.recognize_google(audio_data, language=self.language)

    # -------------------------------------------------------
    # CMU Sphinx (Offline)
    # -------------------------------------------------------
    def _recognize_sphinx(self, audio_data):
        """Recognize using CMU Sphinx (offline)"""

        self.logger.info("Using CMU Sphinx Engine...")

        try:
            return self.recognizer.recognize_sphinx(audio_data, language=self.language)
        except Exception:
            return "Sphinx engine unavailable — install pocketsphinx"

    # -------------------------------------------------------
    # Wav2Vec2 Speech Recognition (Offline)
    # -------------------------------------------------------
    def _recognize_wav2vec2(self, audio_data):
        """Recognize speech using Wav2Vec2 transformer model"""

        self.logger.info("Running inference with Wav2Vec2...")

        # Convert audio bytes to tensor
        wav_bytes = audio_data.get_wav_data()
        waveform = torch.tensor(
            list(wav_bytes),
            dtype=torch.float32
        ).to(self.device)

        # Normalize and reshape
        waveform = waveform / 32768.0
        waveform = waveform.unsqueeze(0)

        # Tokenize and run inference
        logits = self.model(waveform).logits
        predicted_ids = torch.argmax(logits, dim=-1)

        # Decode transcription
        transcription = self.tokenizer.decode(predicted_ids[0])

        return transcription.replace("|", " ").strip()
