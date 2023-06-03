import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
import os
import customtkinter as ctk

class MusicPlayer:
    def __init__(self):
        # komponen GUI
        self.window = tk.Tk()
        self.window.title("Music Player")
        self.window.geometry("500x500")
        self.window.configure(bg="#f3aac0")

        # atribut
        self.playlist = []
        self.current_song_index = None

        # komponen GUI
        self.song_label = ctk.CTkLabel(self.window, text="Welcome to Music Player!", font=("Poppins", 22, "bold"))
        self.song_label.pack(pady=15)

        # komponen GUI
        self.song_label = ctk.CTkLabel(self.window, text="No current song", font=("Poppins", 12))
        self.song_label.pack(pady=10)

        # komponen GUI
        self.add_button = ctk.CTkButton(self.window, text="Add Song", command=self.add_song, fg_color="#8b1337")
        self.add_button.pack(pady=10)

        # komponen GUI
        self.play_button = ctk.CTkButton(self.window, text="Play", command=self.play_song, fg_color="#8b1337")
        self.play_button.pack(pady=10)

        # komponen GUI
        self.pause_button = ctk.CTkButton(self.window, text="Pause", command=self.pause_song, fg_color="#8b1337")
        self.pause_button.pack(pady=10)

        # atribut
        self.paused = False
        self.paused_position = 0

        # komponen GUI
        self.next_button = ctk.CTkButton(self.window, text="Next", command=self.play_next_song, fg_color="#8b1337")
        self.next_button.pack(pady=10)

        # komponen GUI
        self.previous_button = ctk.CTkButton(self.window, text="Previous", command=self.play_previous_song, fg_color="#8b1337")
        self.previous_button.pack(pady=10)

        # komponen GUI
        self.stop_button = ctk.CTkButton(self.window, text="Stop", command=self.stop_song, fg_color="#8b1337")
        self.stop_button.pack(pady=10)

        # event protocol untuk menutup aplikasi
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.mainloop()

    def add_song(self):
        song = filedialog.askopenfilename(title="Choose Song", filetypes=(("MP3 Files", "*.mp3"),))
        if song:
            self.playlist.append(song)
            messagebox.showinfo("Success", "Song added to playlist successfully!")
            self.set_current_song_index(len(self.playlist) - 1)

    def play_song(self):
        if self.playlist:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                if self.current_song_index is not None:
                    song = self.playlist[self.current_song_index]
                    song_name = os.path.basename(song)
                    self.song_label.configure(text="Playing: " + song_name)
            else:
                self.play_current_song()
        else:
            messagebox.showwarning("Warning", "Empty Playlist!")

    def pause_song(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.paused_position = pygame.mixer.music.get_pos()
            self.song_label.configure(text="Paused")

    def stop_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.song_label.configure(text="No current song")

    def play_current_song(self):
        if self.current_song_index is not None:
            song = self.playlist[self.current_song_index]
            song_name = os.path.basename(song)
            self.current_song = pygame.mixer.music.load(song)
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            pygame.mixer.music.set_pos(self.paused_position / 1000)
            self.song_label.configure(text="Playing: " + song_name)

    def play_previous_song(self):
        if self.playlist and self.current_song_index is not None:
            self.current_song_index -= 1
            if self.current_song_index < 0:
                self.current_song_index = len(self.playlist) - 1
            self.play_current_song()

    def play_next_song(self):
        if self.playlist and self.current_song_index is not None:
            self.current_song_index += 1
            if self.current_song_index >= len(self.playlist):
                self.current_song_index = 0
            self.play_current_song()

    def set_current_song_index(self, index):
        self.current_song_index = index

    def on_close(self):
        # Menghentikan pemutaran lagu saat menutup aplikasi
        self.stop_song()
        self.window.destroy()
        
if __name__ == "__main__":
    pygame.mixer.init()
    player = MusicPlayer()
    while True : 
        player.window.update()