import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from deep_translator import GoogleTranslator
from utils import load_config, save_config, load_icon

# Create main window
win = tk.Tk()
win.geometry("900x600")
win.title("Real-Time Voice Translator 🔊")
load_icon(win)

# Load saved configuration
config = load_config()
dark_mode = config.get('dark_mode', False)

def toggle_theme():
    global dark_mode, config
    dark_mode = not dark_mode
    config['dark_mode'] = dark_mode
    save_config(config)
    
    bg_color = "#2E2E2E" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    button_bg = "#555555" if dark_mode else "#DDDDDD"
    text_bg = "#3E3E3E" if dark_mode else "white"
    text_fg = "white" if dark_mode else "black"
    
    # Update main window and frames
    win.config(bg=bg_color)
    main_frame.config(bg=bg_color)
    text_frame.config(bg=bg_color)
    lang_frame.config(bg=bg_color)
    button_frame.config(bg=bg_color)
    status_frame.config(bg=bg_color)
    
    # Update all widgets
    for widget in win.winfo_children():
        if isinstance(widget, (tk.Frame, tk.Label)):
            widget.config(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Button):
            widget.config(bg=button_bg, fg=fg_color)
        elif isinstance(widget, ttk.Combobox):
            widget.config(background=bg_color, foreground=fg_color)
        elif isinstance(widget, tk.Text):
            widget.config(bg=text_bg, fg=text_fg, insertbackground=fg_color)
    
    # Special case for status label
    status_label.config(bg=bg_color, fg=fg_color)

# Language dictionary
language_codes = {
    #"English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Urdu": "ur",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Main UI Layout
main_frame = tk.Frame(win, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Configure grid weights for main frame
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=0)
main_frame.rowconfigure(2, weight=0)
main_frame.rowconfigure(3, weight=0)
main_frame.rowconfigure(3, weight=0)

# Set minimum size only
win.minsize(800, 500)  # Minimum reasonable size

def on_resize(event):
    if win.state() == 'zoomed':
        # Maintain original size when maximized
        win.geometry("900x600")
    else:
        # Only allow resizing in windowed mode
        win.minsize(800, 500)
            
win.bind('<Configure>', on_resize)

# Text Areas Frame
text_frame = tk.Frame(main_frame)
text_frame.grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="nsew")

# Input/Output Labels
input_label = tk.Label(text_frame, text="Recognized Text ⮯", font=("Arial", 16, "bold"))
input_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")

output_label = tk.Label(text_frame, text="Translated Text ⮯", font=("Arial", 16, "bold"))
output_label.grid(row=0, column=1, padx=15, pady=5, sticky="w")

# Text Widgets
input_text = tk.Text(text_frame, font=("Arial", 16),
                    wrap=tk.WORD, padx=10, pady=10, bd=2, relief=tk.GROOVE)
input_text.grid(row=1, column=0, padx=15, sticky="nsew")

output_text = tk.Text(text_frame, font=("Arial", 16),
                     wrap=tk.WORD, padx=10, pady=10, bd=2, relief=tk.GROOVE)
output_text.grid(row=1, column=1, padx=15, sticky="nsew")

# Configure grid weights
text_frame.columnconfigure(0, weight=1)
text_frame.columnconfigure(1, weight=1)
text_frame.rowconfigure(1, weight=1)

# Language Selection Frame
lang_frame = tk.Frame(main_frame)
lang_frame.grid(row=1, column=0, columnspan=2, pady=(0,20), sticky="nsew")

# Input Language (Fixed to English)
input_lang_frame = tk.Frame(lang_frame)
input_lang_frame.grid(row=0, column=0, padx=15, sticky="w")
input_lang_label = tk.Label(input_lang_frame, text="Input Language:", font=("Arial", 14))
input_lang_label.pack(anchor="w")
input_lang_value = tk.Label(input_lang_frame, text="English", font=("Arial", 14))
input_lang_value.pack(anchor="w")

# Output Language 1 (Selectable)
output_lang_frame = tk.Frame(lang_frame)
output_lang_frame.grid(row=0, column=1, padx=15, sticky="w")
output_lang_label = tk.Label(output_lang_frame, text="Output Language 1:", font=("Arial", 14))
output_lang_label.pack(anchor="w")
output_lang = ttk.Combobox(output_lang_frame, values=language_names, 
                          font=("Arial", 14), width=20)
output_lang.set("Hindi")
output_lang.pack(anchor="w")

# Output Language 2 (Selectable)
output_lang_2_frame = tk.Frame(lang_frame)
output_lang_2_frame.grid(row=0, column=2, padx=15, sticky="w")
output_lang_2_label = tk.Label(output_lang_2_frame, text="Output Language 2:", font=("Arial", 14))
output_lang_2_label.pack(anchor="w")
output_lang_2 = ttk.Combobox(output_lang_2_frame, values=language_names, 
                            font=("Arial", 14), width=20)
output_lang_2.set("French")
output_lang_2.pack(anchor="w")

keep_running = False

# Status Bar
status_frame = tk.Frame(main_frame, bd=1, relief=tk.SUNKEN)
status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
status_label = tk.Label(status_frame, text="Status: Ready", 
                       font=("Arial", 12), anchor="w")
status_label.pack(fill=tk.X, padx=5, pady=2)

def update_status(message):
    status_label.config(text=f"Status: {message}")
    win.update()

# Voice Translator Function
def update_translation():
    global keep_running
    if not keep_running:
        return

    r = sr.Recognizer()
    r.energy_threshold = 4000  # Adjust for better recognition
    r.dynamic_energy_threshold = True
    
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=1)
            update_status("Listening... Speak now...")
            
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                update_status("Processing speech...")
                
                try:
                    speech_text = r.recognize_google(audio)
                    input_text.insert(tk.END, f"You: {speech_text}\n")
                    input_text.see(tk.END)

                    if speech_text.lower() in {"exit", "stop"}:
                        keep_running = False
                        update_status("Stopped")
                        return

                    source_lang_code = "en"  # Fixed to English
                    target_lang_code = language_codes.get(output_lang.get(), "en")
                    target_lang_code_2 = language_codes.get(output_lang_2.get(), "fr")

                    update_status("Translating...")
                    translated_text_1 = GoogleTranslator(source=source_lang_code, target=target_lang_code).translate(speech_text)
                    translated_text_2 = GoogleTranslator(source=source_lang_code, target=target_lang_code_2).translate(speech_text)

                    output_text.insert(tk.END, f"Translation 1: {translated_text_1}\nTranslation 2: {translated_text_2}\n")
                    output_text.see(tk.END)

                    update_status("Generating speech...")
                    try:
                        # Generate speech for first translation
                        tts1 = gTTS(translated_text_1, lang=target_lang_code)
                        tts1.save("voice1.mp3")
                        playsound("voice1.mp3")
                        os.remove("voice1.mp3")
                        
                        # Generate speech for second translation
                        tts2 = gTTS(translated_text_2, lang=target_lang_code_2)
                        tts2.save("voice2.mp3")
                        playsound("voice2.mp3")
                        os.remove("voice2.mp3")
                    except Exception as e:
                        output_text.insert(tk.END, f"Speech Error: {str(e)}\n")
                        update_status(f"Speech Error: {str(e)}")

                    update_status("Ready")

                except sr.UnknownValueError:
                    output_text.insert(tk.END, "Could not understand audio\n")
                    update_status("Error: Could not understand")
                except sr.RequestError as e:
                    output_text.insert(tk.END, f"API Error: {str(e)}\n")
                    update_status("Error: API Error")
                except Exception as e:
                    output_text.insert(tk.END, f"Error: {str(e)}\n")
                    update_status(f"Error: {str(e)}")

            except sr.WaitTimeoutError:
                output_text.insert(tk.END, "No speech detected\n")
                update_status("Error: No speech detected")
                
    except OSError as e:
        output_text.insert(tk.END, f"Microphone Error: {str(e)}\n")
        update_status("Error: No microphone")

    if keep_running:
        win.after(100, update_translation)

# Start Listening
def run_translator():
    global keep_running
    if not keep_running:
        keep_running = True
        update_status("Starting...")
        threading.Thread(target=update_translation, daemon=True).start()

# Stop Listening
def stop_translator():
    global keep_running
    if keep_running:
        keep_running = False
        update_status("Stopped")

# Clear text functions
def clear_input():
    input_text.delete(1.0, tk.END)
    
def clear_output():
    output_text.delete(1.0, tk.END)

# Button Frame
button_frame = tk.Frame(main_frame)
button_frame.grid(row=3, column=0, columnspan=2, pady=(0,10), sticky="nsew")

# Action Buttons
action_frame = tk.Frame(button_frame)
action_frame.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(action_frame, text="Start Listening 🎙", 
                        command=run_translator, font=("Arial", 14),
                        width=18, height=2)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = tk.Button(action_frame, text="Stop Listening ❌", 
                       command=stop_translator, font=("Arial", 14),
                       width=18, height=2)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

# New Button for Text to Voice Translation
def translate_text_to_voice():
    text = input_text.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Input Required", "Please enter text to translate and convert to voice.")
        return

    source_lang_code = "en"  # Fixed to English input
    target_lang_code = language_codes.get(output_lang.get(), "en")
    target_lang_code_2 = language_codes.get(output_lang_2.get(), "fr")

    update_status("Translating text...")
    try:
        translated_text_1 = GoogleTranslator(source=source_lang_code, target=target_lang_code).translate(text)
        translated_text_2 = GoogleTranslator(source=source_lang_code, target=target_lang_code_2).translate(text)

        output_text.insert(tk.END, f"Translation 1: {translated_text_1}\nTranslation 2: {translated_text_2}\n")
        output_text.see(tk.END)

        update_status("Generating speech...")
        try:
            tts1 = gTTS(translated_text_1, lang=target_lang_code)
            tts1.save("voice1.mp3")
            playsound("voice1.mp3")
            os.remove("voice1.mp3")

            tts2 = gTTS(translated_text_2, lang=target_lang_code_2)
            tts2.save("voice2.mp3")
            playsound("voice2.mp3")
            os.remove("voice2.mp3")
        except Exception as e:
            output_text.insert(tk.END, f"Speech Error: {str(e)}\n")
            update_status(f"Speech Error: {str(e)}")

        update_status("Ready")
    except Exception as e:
        output_text.insert(tk.END, f"Translation Error: {str(e)}\n")
        update_status(f"Translation Error: {str(e)}")

translate_text_button = tk.Button(action_frame, text="Translate Text to Voice 🔊",
                                  command=translate_text_to_voice, font=("Arial", 14),
                                  width=22, height=2)
translate_text_button.pack(side=tk.LEFT, padx=5, pady=5)

# Combined Clear Button and Theme Button
button_group_frame = tk.Frame(button_frame)
button_group_frame.pack(side=tk.LEFT, padx=10)

def clear_all():
    clear_input()
    clear_output()

clear_all_button = tk.Button(button_group_frame, text="Clear All ✖", 
                           command=clear_all, font=("Arial", 14),
                           width=18, height=2)
clear_all_button.pack(side=tk.LEFT, padx=5, pady=5)

theme_button = tk.Button(button_group_frame, text="Toggle Theme 🌗", 
                        command=toggle_theme, font=("Arial", 14),
                        width=18, height=2)
theme_button.pack(side=tk.LEFT, padx=5, pady=5)

# Tooltips
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = tk.Label(tooltip, text=text, bg="lightyellow", relief="solid", borderwidth=1)
    label.pack()
    widget.bind("<Enter>", lambda e: tooltip.deiconify())
    widget.bind("<Leave>", lambda e: tooltip.withdraw())

create_tooltip(start_button, "Start voice recognition and translation")
create_tooltip(stop_button, "Stop the current translation session")
create_tooltip(clear_all_button, "Clear both input and output text")
create_tooltip(theme_button, "Toggle between light/dark mode")

# Apply initial theme
if dark_mode:
    toggle_theme()

# Run the app
win.mainloop()
