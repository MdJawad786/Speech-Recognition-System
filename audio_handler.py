"""
Audio Handler
Manages audio input from microphone and files
"""

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import os
from utils import setup_logging

class AudioHandler:
    def __init__(self):
        """Initialize audio handler"""
        self.recognizer = sr.Recognizer()
        self.logger = setup_logging()
        
        # Set ffmpeg path if available
        AudioSegment.converter = which("ffmpeg")
        
    def record_from_microphone(self, duration=5, sample_rate=16000):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate in Hz
            
        Returns:
            AudioData object
        """
        try:
            with sr.Microphone(sample_rate=sample_rate) as source:
                self.logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                self.logger.info(f"Recording for {duration} seconds...")
                audio_data = self.recognizer.listen(source, timeout=duration+2, phrase_time_limit=duration)
                
                self.logger.info("Recording complete")
                return audio_data
                
        except Exception as e:
            self.logger.error(f"Microphone recording error: {e}")
            raise
            
    def record_continuous(self, callback, phrase_time_limit=5):
        """
        Record audio continuously and call callback for each phrase
        
        Args:
            callback: Function to call with each audio chunk
            phrase_time_limit: Max seconds for each phrase
        """
        with sr.Microphone() as source:
            self.logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            self.logger.info("Starting continuous recording...")
            
            while True:
                try:
                    audio_data = self.recognizer.listen(
                        source,
                        phrase_time_limit=phrase_time_limit
                    )
                    callback(audio_data)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"Error in continuous recording: {e}")
                    
    def load_audio_file(self, file_path):
        """
        Load audio from file
        
        Args:
            file_path: Path to audio file
            
        Returns:
            AudioData object
        """
        try:
            # Get file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.wav':
                with sr.AudioFile(file_path) as source:
                    audio_data = self.recognizer.record(source)
                    self.logger.info(f"Loaded WAV file: {file_path}")
                    return audio_data
            else:
                # Convert to WAV using pydub
                self.logger.info(f"Converting {ext} to WAV format...")
                audio = AudioSegment.from_file(file_path)
                
                # Convert to mono and set sample rate
                audio = audio.set_channels(1)
                audio = audio.set_frame_rate(16000)
                
                # Export to temporary WAV file
                temp_wav = "temp_audio.wav"
                audio.export(temp_wav, format="wav")
                
                with sr.AudioFile(temp_wav) as source:
                    audio_data = self.recognizer.record(source)
                    
                # Clean up temp file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
                    
                self.logger.info(f"Loaded and converted file: {file_path}")
                return audio_data
                
        except Exception as e:
            self.logger.error(f"Error loading audio file: {e}")
            raise
            
    def save_audio(self, audio_data, file_path):
        """
        Save audio data to file
        
        Args:
            audio_data: AudioData object
            file_path: Output file path
        """
        try:
            with open(file_path, "wb") as f:
                f.write(audio_data.get_wav_data())
            self.logger.info(f"Audio saved to: {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving audio: {e}")
            raise
            
    def list_microphones(self):
        """List available microphone devices"""
        mics = sr.Microphone.list_microphone_names()
        self.logger.info(f"Available microphones: {len(mics)}")
        return mics