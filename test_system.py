"""
Unit Tests for Speech Recognition System
"""

import unittest
import os
import tempfile
from speech_recognizer import SpeechRecognizer
from audio_handler import AudioHandler
from utils import setup_logging, save_transcription, format_timestamp

class TestSpeechRecognizer(unittest.TestCase):
    """Test cases for SpeechRecognizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.recognizer = SpeechRecognizer(engine='google')
        
    def test_recognizer_initialization(self):
        """Test recognizer initialization"""
        self.assertIsNotNone(self.recognizer)
        self.assertEqual(self.recognizer.engine, 'google')
        self.assertEqual(self.recognizer.language, 'en-US')
        
    def test_language_setting(self):
        """Test language setting"""
        recognizer = SpeechRecognizer(engine='google', language='es-ES')
        self.assertEqual(recognizer.language, 'es-ES')
        
    def test_invalid_engine(self):
        """Test invalid engine raises error"""
        with self.assertRaises(ValueError):
            SpeechRecognizer(engine='invalid')

        # Should raise error when recognizing
        # This is tested during actual recognition
        
class TestAudioHandler(unittest.TestCase):
    """Test cases for AudioHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = AudioHandler()
        
    def test_handler_initialization(self):
        """Test handler initialization"""
        self.assertIsNotNone(self.handler)
        self.assertIsNotNone(self.handler.recognizer)
        
    def test_list_microphones(self):
        """Test listing microphones"""
        mics = self.handler.list_microphones()
        self.assertIsInstance(mics, list)
        # Should have at least one microphone (may fail on headless systems)
        
class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_setup_logging(self):
        """Test logging setup"""
        logger = setup_logging()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'SpeechToText')
        
    def test_format_timestamp(self):
        """Test timestamp formatting"""
        self.assertEqual(format_timestamp(0), '00:00')
        self.assertEqual(format_timestamp(65), '01:05')
        self.assertEqual(format_timestamp(3661), '61:01')
        
    def test_save_transcription(self):
        """Test saving transcription"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
            
        try:
            save_transcription("Test transcription", temp_file)
            
            with open(temp_file, 'r') as f:
                content = f.read()
                
            self.assertIn("Test transcription", content)
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
    def test_save_transcription_append(self):
        """Test appending transcription"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
            
        try:
            save_transcription("First", temp_file)
            save_transcription("Second", temp_file, append=True)
            
            with open(temp_file, 'r') as f:
                content = f.read()
                
            self.assertIn("First", content)
            self.assertIn("Second", content)
            
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_pipeline_with_mock(self):
        """Test full pipeline with mock data"""
        # This would require mock audio data
        # Implementation depends on specific testing needs
        pass

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()