"""
GUI Application for Speech-to-Text
Simple graphical interface using tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
from speech_recognizer import SpeechRecognizer
from audio_handler import AudioHandler
from utils import setup_logging, save_transcription

class SpeechToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech-to-Text System")
        self.root.geometry("800x600")
        
        self.logger = setup_logging()
        self.is_recording = False
        self.recognizer = None
        self.audio_handler = AudioHandler()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title_label = tk.Label(
            self.root,
            text="🎤 Speech-to-Text Recognition System",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Engine selection
        ttk.Label(settings_frame, text="Engine:").grid(row=0, column=0, sticky="w", padx=5)
        self.engine_var = tk.StringVar(value="google")
        engine_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.engine_var,
            values=["google", "sphinx", "wav2vec2"],
            state="readonly",
            width=15
        )
        engine_combo.grid(row=0, column=1, sticky="w", padx=5)
        
        # Language selection
        ttk.Label(settings_frame, text="Language:").grid(row=0, column=2, sticky="w", padx=5)
        self.language_var = tk.StringVar(value="en-US")
        language_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.language_var,
            values=["en-US", "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN"],
            state="readonly",
            width=10
        )
        language_combo.grid(row=0, column=3, sticky="w", padx=5)
        
        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Buttons
        self.record_btn = ttk.Button(
            control_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            width=20
        )
        self.record_btn.pack(side="left", padx=5)
        
        self.file_btn = ttk.Button(
            control_frame,
            text="📁 Load Audio File",
            command=self.load_file,
            width=20
        )
        self.file_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(
            control_frame,
            text="🗑️ Clear",
            command=self.clear_text,
            width=15
        )
        self.clear_btn.pack(side="left", padx=5)
        
        self.save_btn = ttk.Button(
            control_frame,
            text="💾 Save",
            command=self.save_text,
            width=15
        )
        self.save_btn.pack(side="left", padx=5)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        status_label.pack(pady=5)
        
        # Text Display
        text_frame = ttk.LabelFrame(self.root, text="Transcription", padding=10)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            height=15
        )
        self.text_display.pack(fill="both", expand=True)
        
    def toggle_recording(self):
        """Start or stop recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording from microphone"""
        self.is_recording = True
        self.record_btn.config(text="⏹️ Stop Recording")
        self.status_var.set("🔴 Recording...")
        
        # Run recording in separate thread
        thread = threading.Thread(target=self.record_audio)
        thread.daemon = True
        thread.start()
        
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        self.record_btn.config(text="🎤 Start Recording")
        self.status_var.set("Ready")
        
    def record_audio(self):
        """Record and transcribe audio"""
        try:
            # Initialize recognizer
            self.recognizer = SpeechRecognizer(
                engine=self.engine_var.get(),
                language=self.language_var.get()
            )
            
            # Record audio
            audio_data = self.audio_handler.record_from_microphone(duration=5)
            
            if not self.is_recording:
                return
                
            # Update status
            self.status_var.set("🔄 Processing...")
            
            # Recognize speech
            text = self.recognizer.recognize(audio_data)
            
            if text:
                # Update text display
                self.text_display.insert(tk.END, text + "\n\n")
                self.text_display.see(tk.END)
                self.status_var.set("✅ Transcription complete")
            else:
                self.status_var.set("❌ Could not understand audio")
                messagebox.showwarning("Recognition Failed", "Could not understand audio")
                
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
            self.status_var.set("❌ Error occurred")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.is_recording = False
            self.record_btn.config(text="🎤 Start Recording")
            
    def load_file(self):
        """Load and transcribe audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac *.ogg *.m4a"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            self.status_var.set("📁 Loading file...")
            
            # Initialize recognizer
            self.recognizer = SpeechRecognizer(
                engine=self.engine_var.get(),
                language=self.language_var.get()
            )
            
            # Load audio
            audio_data = self.audio_handler.load_audio_file(file_path)
            
            self.status_var.set("🔄 Processing...")
            
            # Recognize speech
            text = self.recognizer.recognize(audio_data)
            
            if text:
                self.text_display.insert(tk.END, f"[{file_path}]\n{text}\n\n")
                self.text_display.see(tk.END)
                self.status_var.set("✅ File transcribed")
            else:
                self.status_var.set("❌ Could not transcribe audio")
                messagebox.showwarning("Transcription Failed", "Could not transcribe audio")
                
        except Exception as e:
            self.logger.error(f"File loading error: {e}")
            self.status_var.set("❌ Error occurred")
            messagebox.showerror("Error", str(e))
            
    def clear_text(self):
        """Clear text display"""
        self.text_display.delete(1.0, tk.END)
        self.status_var.set("Ready")
        
    def save_text(self):
        """Save transcription to file"""
        text = self.text_display.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("No Content", "No text to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Transcription",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.status_var.set(f"💾 Saved to {file_path}")
                messagebox.showinfo("Success", "Transcription saved successfully")
            except Exception as e:
                self.logger.error(f"Save error: {e}")
                messagebox.showerror("Error", f"Failed to save file: {e}")

def main():
    root = tk.Tk()
    app = SpeechToTextGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()