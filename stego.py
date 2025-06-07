import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk, UnidentifiedImageError
import stepic
import soundfile as sf
import numpy as np
import os
import sounddevice as sd
import cv2
import ffmpeg
from scipy.io.wavfile import write
import wave
from tempfile import NamedTemporaryFile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from pydub import AudioSegment
from mutagen.wavpack import WavPack


# Key creation
def create_key():
    key = Fernet.generate_key()

    save_path = filedialog.asksaveasfilename(
        defaultextension=".key",
        filetypes=[("Key Files", "*.key")]
    )

    if save_path:
        with open(save_path, 'wb') as f:
            f.write(key)
        messagebox.showinfo("Success", f"Key saved to {save_path}")


#Select Key
def select_key():
    file_path = filedialog.askopenfilename(
        title="Select Key File",
        filetypes=[("Key Files", "*.key")]
    )


    if file_path:
        key_file_var.set(file_path)
        messagebox.showinfo("Key Selected", f"Key file: {file_path}")


#Select Picture
def select_picture():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )


        if file_path:
            image_path_var.set(file_path)
        
            img = Image.open(file_path)
            img.thumbnail((300, 300))
        
            photo = ImageTk.PhotoImage(img)
            
            current_tab = window.index(window.select())
            if current_tab == 3:
                image_label.config(image=photo)
                image_label.image = photo
            elif current_tab == 4:
                decrypt_image_label.config(image=photo)
                decrypt_image_label.image = photo
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Invalid image file")
    except Exception as e:
        messagebox.showerror("Error", str(e))


#Encrypt text
def encrypt_text():
    try:
        with open(key_file_var.get(), "rb") as file:
            key = file.read()


        fernet = Fernet(key)
        encrypted_text = fernet.encrypt(text_encrypt_entry.get().encode())
        
        #Copy to Clipboard
        root.clipboard_clear()
        root.clipboard_append(encrypted_text.decode())
        
        messagebox.showinfo("Success", "Text encrypted and copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


#Derypt text
def decrypt_text():
    try:
        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(text_decrypt_entry.get().encode()).decode()

        messagebox.showinfo("Success","Message Decrypted Successfully")
        decrypted_text_label = tk.Label(text_mode_out,text=f"Decrypted Test: {str(decrypted_text)}",font=("Times new Roman",12)).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))



#Encrypt text and Hide inside Image
def hide_in_image():
    try:
        if not text_hide_entry.get() or not image_path_var.get():
            messagebox.showwarning("Warning", "Please enter text and select an image")
            return

        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(text_hide_entry.get().encode())

        img = Image.open(image_path_var.get())
        encoded_image = stepic.encode(img, encrypted_message)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if save_path:
            encoded_image.save(save_path)
            messagebox.showinfo("Success", f"Message hidden in {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


#unhide Encrypted text from Image and Decode
def unhide_from_image():
    try:
        if not key_file_var.get() or not image_path_var.get():
            messagebox.showwarning("Warning", "Please select key and image")
            return

        image = Image.open(image_path_var.get())
        encrypted_text = stepic.decode(image)

        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text).decode()

        messagebox.showinfo("Success!","Text Extracted From the Image and Decrypted")
        text_decrypted_label = tk.Label(picture_mode_out,text=f"Decrypted Text From the Image is: {str(decrypted_text)}").pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))

#Audio Selection
def select_audio():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac *.ogg *.aiff *.au"),
                ("WAV", "*.wav"),
                ("MP3", "*.mp3"),
                ("FLAC", "*.flac"),
                ("OGG", "*.ogg"),
                ("AIFF", "*.aiff"),
                ("AU", "*.au")
            ]
        )

        if file_path:
            audio_path_var.set(file_path)
            messagebox.showinfo("Audio Selected", f"Audio file: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

#Hide Message in Audio
def convert_to_wav(input_path, output_path):
    data, samplerate = sf.read(input_path)
    
    # Convert to mono if stereo
    if data.ndim > 1:
        data = data.mean(axis=1)
    
    sf.write(output_path, data, samplerate, subtype='PCM_16')
    return output_path

def hide_in_audio():
    try:
        if not text_hide_audio_entry.get() or not audio_path_var.get():
            messagebox.showwarning("Warning", "Please enter text and select an audio file")
            return

        # Read the encryption key
        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(text_hide_audio_entry.get().encode())

        # Convert the message to binary bits
        message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)
        message_length = len(message_bits)

        # Convert audio to WAV if necessary
        temp_wav_path = audio_path_var.get()
        if not temp_wav_path.endswith('.wav'):
            temp_wav_path = convert_to_wav(audio_path_var.get(), os.path.splitext(audio_path_var.get())[0] + '_temp.wav')

        # Read audio file
        data, samplerate = sf.read(temp_wav_path, dtype='int16')
        
        # Ensure mono audio for simplicity
        if data.ndim > 1:
            data = data.mean(axis=1).astype('int16')

        # Check capacity
        max_capacity = len(data)
        if message_length > max_capacity:
            messagebox.showerror("Error", "Message is too large to fit in the selected audio file")
            return

        # Hide the message in the LSB of audio samples
        modified_data = data.copy()
        bit_index = 0
        for i in range(len(modified_data)):
            if bit_index < message_length:
                modified_data[i] = (modified_data[i] & ~1) | int(message_bits[bit_index])
                bit_index += 1

        # Save modified audio
        save_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
        if save_path:
            sf.write(save_path, modified_data, samplerate)
            messagebox.showinfo("Success", f"Message hidden in {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


#Extract Message from Audio
def unhide_from_audio():
    try:
        if not key_file_var.get() or not audio_path_var.get():
            messagebox.showwarning("Warning", "Please select key and audio file")
            return

        # Read audio file
        data, _ = sf.read(audio_path_var.get())
        
        # Convert to mono if stereo
        if data.ndim > 1:
            data = data.mean(axis=1)

        # Extract message bits
        message_bits = ''
        for sample in data:
            # Convert sample to integer and extract LSB
            lsb = int(round(sample * 32767)) & 1
            message_bits += str(lsb)
            if len(message_bits) >= 256 * 8:  # Reasonable max message length
                break

        # Convert bits to bytes
        encrypted_bytes = bytes(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8))

        # Decrypt message
        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_bytes).decode()

        messagebox.showinfo("Success!", "Message Extracted From Audio")
        text_decrypted_audio_label = tk.Label(audio_mode_out, text=f"Decrypted Text From Audio: {str(decrypted_text)}").pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Select Video Function
def select_video():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                ("MP4", "*.mp4"),
                ("AVI", "*.avi"),
                ("MOV", "*.mov"),
                ("MKV", "*.mkv")
            ]
        )

        if file_path:
            video_path_var.set(file_path)
            messagebox.showinfo("Video Selected", f"Video file: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def hide_in_video():
    try:
        if not text_hide_video_entry.get() or not video_path_var.get():
            messagebox.showwarning("Warning", "Please enter text and select a video")
            return

        # Read encryption key
        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        # Encrypt the message
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(text_hide_video_entry.get().encode())

        # Convert message to binary
        message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)

        # Extract audio from video
        temp_audio_path = "temp_audio.wav"
        (
            ffmpeg
            .input(video_path_var.get())
            .output(temp_audio_path, format='wav', acodec='pcm_s16le', ac=1)
            .run(overwrite_output=True)
        )

        # Read audio file
        data, samplerate = sf.read(temp_audio_path, dtype='int16')

        # Hide message in LSB
        modified_data = data.copy()
        for i in range(len(message_bits)):
            modified_data[i] = (modified_data[i] & ~1) | int(message_bits[i])

        # Save modified audio
        modified_audio_path = "modified_audio.wav"
        sf.write(modified_audio_path, modified_data, samplerate)

        # Merge modified audio back into video
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if save_path:
            (
                ffmpeg
                .input(video_path_var.get())
                .input(modified_audio_path)
                .output(save_path, vcodec='copy', acodec='aac')
                .run(overwrite_output=True)
            )

            os.remove(temp_audio_path)
            os.remove(modified_audio_path)

            messagebox.showinfo("Success", f"Message hidden in {save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def unhide_from_video():
    try:
        if not video_path_var.get() or not key_file_var.get():
            messagebox.showwarning("Warning", "Please select a video and encryption key file")
            return

        # Read encryption key
        with open(key_file_var.get(), "rb") as file:
            key = file.read()

        fernet = Fernet(key)

        # Extract audio from video
        temp_audio_path = "extracted_audio.wav"
        (
            ffmpeg
            .input(video_path_var.get())
            .output(temp_audio_path, format='wav', acodec='pcm_s16le', ac=1)
            .run(overwrite_output=True)
        )

        # Read the audio file
        data, samplerate = sf.read(temp_audio_path, dtype='int16')

        # Extract LSB message
        extracted_bits = ''.join(str(sample & 1) for sample in data[:8000])  # Adjust length as needed

        # Convert binary to bytes
        byte_array = bytearray()
        for i in range(0, len(extracted_bits), 8):
            byte_array.append(int(extracted_bits[i:i+8], 2))

        # Decrypt message
        decrypted_message = fernet.decrypt(bytes(byte_array)).decode()

        messagebox.showinfo("Recovered Message", decrypted_message)

        os.remove(temp_audio_path)

    except Exception as e:
        messagebox.showerror("Error", str(e))


#Root Window
root = tk.Tk()
root.title("CipherHide")
root.geometry("800x700")
root.resizable(False, False)

# Style configuration
style = ttk.Style()
style.configure("TNotebook.Tab", font=('forte', 10))
style.configure("TLabel", font=('Eras Bold ITC', 12))
style.configure("TButton", font=('Arial', 10))

#Global Variables
key_file_var = tk.StringVar()
image_path_var = tk.StringVar()
audio_path_var = tk.StringVar()
video_path_var = tk.StringVar()

# Notebook/notebook tabs/notebook contents
window = ttk.Notebook(root)
window.pack(expand=True, fill="both", padx=10, pady=10)

# Frames
key_frame = ttk.Frame(window)
text_mode_in = ttk.Frame(window)
text_mode_out = ttk.Frame(window)
picture_mode_in = ttk.Frame(window)
picture_mode_out = ttk.Frame(window)
audio_mode_in = ttk.Frame(window)
audio_mode_out = ttk.Frame(window)
video_mode_in = ttk.Frame(window)
video_mode_out = ttk.Frame(window)


#Adding Frames to Root window
window.add(key_frame, text="Key Creation")
window.add(text_mode_in, text="Text Encryption")
window.add(text_mode_out, text="Text Decryption")
window.add(picture_mode_in, text="Picture Encryption")
window.add(picture_mode_out, text="Picture Decryption")
window.add(audio_mode_in,text="Audio Encryption")
window.add(audio_mode_out,text="Audio Decryption")
window.add(video_mode_in,text="Video Encryption")
window.add(video_mode_out,text="Video Decryption")


# Key Creation Frame
ttk.Label(key_frame, text="Key Creation", style="TLabel").pack(pady=20)
ttk.Label(key_frame, text="Generate a secure encryption key").pack(pady=10)
ttk.Button(key_frame, text="Create New Key", command=create_key).pack(pady=10)

# Text Encryption Frame
ttk.Label(text_mode_in, text="Text Encryption", style="TLabel").pack(pady=10)
ttk.Label(text_mode_in, text="Enter Text to Encrypt:").pack(pady=5)
text_encrypt_entry = ttk.Entry(text_mode_in, width=50)
text_encrypt_entry.pack(pady=5)
ttk.Button(text_mode_in, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(text_mode_in, text="Encrypt", command=encrypt_text).pack(pady=10)

# Text Decryption Frame
ttk.Label(text_mode_out, text="Text Decryption", style="TLabel").pack(pady=10)
ttk.Label(text_mode_out, text="Enter Encrypted Text:").pack(pady=5)
text_decrypt_entry = ttk.Entry(text_mode_out, width=50)
text_decrypt_entry.pack(pady=5)
ttk.Button(text_mode_out, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(text_mode_out, text="Decrypt", command=decrypt_text).pack(pady=10)

# Picture Encryption Frame
ttk.Label(picture_mode_in, text="Picture Encryption", style="TLabel").pack(pady=10)
ttk.Button(picture_mode_in, text="Select Image", command=select_picture).pack(pady=5)
image_label = ttk.Label(picture_mode_in)
image_label.pack(pady=10)
ttk.Label(picture_mode_in, text="Enter Text to Hide:").pack(pady=5)
text_hide_entry = ttk.Entry(picture_mode_in, width=50)
text_hide_entry.pack(pady=5)
ttk.Button(picture_mode_in, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(picture_mode_in, text="Hide in Image", command=hide_in_image).pack(pady=10)

# Picture Decryption Frame
ttk.Label(picture_mode_out, text="Picture Decryption", style="TLabel").pack(pady=10)
ttk.Button(picture_mode_out, text="Select Image", command=select_picture).pack(pady=5)
decrypt_image_label = ttk.Label(picture_mode_out)
decrypt_image_label.pack(pady=10)
ttk.Button(picture_mode_out, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(picture_mode_out, text="Extract from Image", command=unhide_from_image).pack(pady=10)

ttk.Label(audio_mode_in, text="Audio Encryption", style="TLabel").pack(pady=10)
ttk.Button(audio_mode_in, text="Select Audio", command=select_audio).pack(pady=5)
ttk.Label(audio_mode_in, text="Enter Text to Hide:").pack(pady=5)
text_hide_audio_entry = ttk.Entry(audio_mode_in, width=50)
text_hide_audio_entry.pack(pady=5)
ttk.Button(audio_mode_in, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(audio_mode_in, text="Hide in Audio", command=hide_in_audio).pack(pady=10)

# Modify Audio Decryption Frame
# Audio Decryption Frame
ttk.Label(audio_mode_out, text="Audio Decryption", style="TLabel").pack(pady=10)
ttk.Button(audio_mode_out, text="Select Audio", command=select_audio).pack(pady=5)
ttk.Button(audio_mode_out, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(audio_mode_out, text="Extract from Audio", command=unhide_from_audio).pack(pady=10)

# Update Video Encryption Frame
ttk.Label(video_mode_in, text="Video Encryption", style="TLabel").pack(pady=10)
ttk.Button(video_mode_in, text="Select Video", command=select_video).pack(pady=5)
ttk.Label(video_mode_in, text="Enter Text to Hide:").pack(pady=5)
text_hide_video_entry = ttk.Entry(video_mode_in, width=50)
text_hide_video_entry.pack(pady=5)
ttk.Button(video_mode_in, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(video_mode_in, text="Hide in Video", command=hide_in_video).pack(pady=10)

# Update Video Decryption Frame
ttk.Label(video_mode_out, text="Video Decryption", style="TLabel").pack(pady=10)
ttk.Button(video_mode_out, text="Select Video", command=select_video).pack(pady=5)
ttk.Button(video_mode_out, text="Select Key File", command=select_key).pack(pady=5)
ttk.Button(video_mode_out, text="Extract from Video", command=lambda:unhide_from_video(text_hide_video_entry.get())).pack(pady=10)



print(f"Video Path: {video_path_var.get()}, Exists: {os.path.exists(video_path_var.get())}")
print(f"Key File Path: {key_file_var.get()}, Exists: {os.path.exists(key_file_var.get())}")




root.mainloop()
