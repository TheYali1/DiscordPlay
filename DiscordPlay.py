import customtkinter as ctk
from pypresence import Presence
import time
from PIL import Image, ImageTk
import os
import sys
import threading
import tkinter as tk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DiscordPlayApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.rpc = None
        self.current_game = None
        self.closing = False
        
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        window_height = min(700, int(screen_height * 0.8))
        window_width = int(window_height * 16 / 9)
        
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        
        self.app.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        self.app.title("DiscordPlay")
        self.app.minsize(800, 500)
        self.app.attributes("-alpha", 0.0)

        self.font_name = "Rubik" if self.is_font_available("Rubik") else None
        
        self.games_data = {
            "Minecraft": {"client_id": "1360553018097012766", "image": "minecraft", "color": "#4faf5a"},
            "CS:GO": {"client_id": "1360557249977909299", "image": "csgo", "color": "#fabd0f"},
            "Roblox": {"client_id": "1360556985589960886", "image": "roblox", "color": "#ff0000"},
            "CS2": {"client_id": "1360556711034753135", "image": "cs2", "color": "#1e82de"},
            "osu!": {"client_id": "1360557956751687720", "image": "osu!", "color": "#ff66aa"},
            "Among Us": {"client_id": "1360558803220959273", "image": "amongus", "color": "#d10404"},
            "Elden Ring": {"client_id": "1360568456617001050", "image": "eldenring", "color": "#daa520"},
            "Stumble Guys": {"client_id": "1360568965062983710", "image": "stumbleguys", "color": "#8a2be2"},
            "Fall Guys": {"client_id": "1360569211575079062", "image": "fallguys", "color": "#fc36d0"},
            "Fortnite": {"client_id": "1360569629352923207", "image": "fortnite", "color": "#9d4dbb"},
            "Geometry Dash": {"client_id": "1360589184540344530", "image": "geometrydash", "color": "#89a599"},
            "Gartic Phone": {"client_id": "1360589799010074674", "image": "garticphone", "color": "#80ba98"},
            "Blazing 8s": {"client_id": "1360590338141585523", "image": "blazing8s", "color": "#8e840f"},
            "Cyberpunk 2077": {"client_id": "1360591034064699433", "image": "cyberpunk2077", "color": "#996f91"},
            "Whiteboard": {"client_id": "1360591745368330331", "image": "whiteboard", "color": "#8e28b1"},
            "Watch Together": {"client_id": "1360592283795329087", "image": "watchtogether", "color": "#f0689e"},
            "Banana": {"client_id": "1360593166839058452", "image": "banana", "color": "#875a67"},
            "BeamNG.drive": {"client_id": "1360595533307314378", "image": "beamngdrive", "color": "#56b3db"},
            "SCP: Secret Laboratory": {"client_id": "1360597279400267777", "image": "scpsecretlaboratory", "color": "#43cdb6"},
            "Marvel's Spider-Man 2": {"client_id": "1360597984441667675", "image": "marvelsspiderman2", "color": "#3d333a"},
            "GTAIII": {"client_id": "1360598547963318493", "image": "gtalll", "color": "#95a022"},
            "GTA San Andreas": {"client_id": "1360599045998907582", "image": "gtasanandreas", "color": "#ee0897"},
            "Half-Life": {"client_id": "1360599921887023308", "image": "halflife", "color": "#ce75ea"},
            "Chained Together": {"client_id": "1360600720713322696", "image": "chainedtogether", "color": "#23e172"},
            "Chess In The Park": {"client_id": "1360601412945318048", "image": "chessinthepark", "color": "#a4a987"},
        }
        
        self.create_ui()
        self.setup_layout()
        
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.animate_window_open()
    
    def animate_window_open(self):
        alpha = self.app.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.1
            self.app.attributes("-alpha", alpha)
            self.app.after(20, self.animate_window_open)
            
    def animate_window_close(self, callback):
        alpha = self.app.attributes("-alpha")
        if alpha > 0.0:
            alpha -= 0.1
            self.app.attributes("-alpha", alpha)
            self.app.after(20, lambda: self.animate_window_close(callback))
        else:
            callback()
    
    def is_font_available(self, font_name):
        return True
    
    def create_ui(self):
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="DiscordPlay",
            font=(self.font_name, 32, "bold"),
            text_color=("#0068d6" if ctk.get_appearance_mode() == "light" else "#60a5fa")
        )
        self.title_label.pack(pady=10)
        
        self.games_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.games_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.button_frames = []
        self.game_buttons = []
        
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_frame.pack(fill="x", pady=(20, 10))
        
        self.clear_button = ctk.CTkButton(
            self.control_frame,
            text="Cancel Activity",
            font=(self.font_name, 16),
            fg_color="#e11d48",
            hover_color="#be123c",
            height=45,
            command=self.clear_presence
        )
        self.clear_button.pack(pady=10)
        
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray90", "gray20"))
        self.status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Select a game to display",
            font=(self.font_name, 14),
            height=40
        )
        self.status_label.pack(fill="x", padx=10, pady=5)
    
    def setup_layout(self):
        games_per_row = 5
        
        num_rows = (len(self.games_data) + games_per_row - 1) // games_per_row
        
        for row in range(num_rows):
            button_row = ctk.CTkFrame(self.games_frame, fg_color="transparent")
            button_row.pack(fill="x", pady=5)
            self.button_frames.append(button_row)
            
            current_row_games = min(games_per_row, len(self.games_data) - row * games_per_row)
            
            for col in range(current_row_games):
                game_index = row * games_per_row + col
                game_name = list(self.games_data.keys())[game_index]
                game_color = self.games_data[game_name].get("color", "#1f538d")
                
                game_button = ctk.CTkButton(
                    button_row,
                    text=game_name,
                    font=(self.font_name, 16),
                    fg_color=game_color,
                    hover_color=self.adjust_color_brightness(game_color, -30),
                    height=60,
                    corner_radius=8,
                    command=lambda g=game_name: self.set_presence_with_animation(g)
                )
                game_button.pack(side="left", fill="x", expand=True, padx=5)
                self.game_buttons.append(game_button)
                
                self.app.after(game_index * 100, lambda btn=game_button: self.animate_button_appear(btn))
    
    def animate_button_appear(self, button):
        button.configure(height=0)
        
        def animate_height(current_height, target_height, step=1):
            if current_height < target_height:
                current_height += step
                button.configure(height=current_height)
                self.app.after(5, lambda: animate_height(current_height, target_height))
            elif current_height > target_height + 5:
                button.configure(height=target_height)
        
        animate_height(0, 60)
    
    def animate_button_click(self, button):
        original_color = button.cget("fg_color")
        highlight_color = self.adjust_color_brightness(original_color, 50)
        
        def pulse_animation(is_highlight=True):
            if self.closing:
                return
                
            if is_highlight:
                button.configure(fg_color=highlight_color)
                self.app.after(100, lambda: pulse_animation(False))
            else:
                button.configure(fg_color=original_color)
        
        pulse_animation()
    
    def adjust_color_brightness(self, hex_color, brightness_offset):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = max(0, min(255, r + brightness_offset))
        g = max(0, min(255, g + brightness_offset))
        b = max(0, min(255, b + brightness_offset))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def set_presence_with_animation(self, game_name):
        for button in self.game_buttons:
            if button.cget("text") == game_name:
                self.animate_button_click(button)
                break
                
        self.animate_loading_status(f"Setting up {game_name}...", 
                                   lambda: self.set_presence(game_name))
    
    def animate_loading_status(self, message, callback, dots=0):
        if self.closing:
            return
            
        dots_text = "." * dots
        self.status_label.configure(text=f"{message}{dots_text}")
        
        if dots < 3:
            self.app.after(300, lambda: self.animate_loading_status(message, callback, dots + 1))
        else:
            callback()
    
    def set_presence(self, game_name):
        game_info = self.games_data[game_name]
        client_id = game_info["client_id"]
        image = game_info["image"]
        
        try:
            if self.rpc:
                self.rpc.clear()
                self.rpc.close()
            
            self.rpc = Presence(client_id)
            self.rpc.connect()
            
            start_timestamp = 1
            
            end_timestamp = int(time.time())
            
            self.rpc.update(
                start=start_timestamp,
                end=end_timestamp,
                large_image=image,
                large_text=game_name
            )
            
            self.current_game = game_name
            
            self.animate_status_success(f"✅ Now showing: {game_name}")
            print(f"Presence started for: {game_name}")
        except Exception as e:
            self.animate_status_error(f"❌ Error: {e}")
            print("ERROR:", e)
    
    def animate_status_success(self, message):
        self.status_label.configure(text=message)
        
        colors = ["#ffffff", "#e6ffee", "#ccffdd", "#b3ffcc", "#99ffbb", "#80ffaa", "#66ff99", "#4dff88", "#33ff77", "#1aff66", "#00ff55", "#00e64d", "#00cc44", "#00b33c", "#009933", "#00802b", "#006622", "#004d1a", "#003311", "#001a09", "#4ade80"]
        
        def animate_color(index=0):
            if self.closing:
                return
                
            if index < len(colors):
                self.status_label.configure(text_color=colors[index])
                self.app.after(20, lambda: animate_color(index + 1))
        
        animate_color()
    
    def animate_status_error(self, message):
        self.status_label.configure(text=message)
        
        colors = ["#ffffff", "#ffe6e6", "#ffcccc", "#ffb3b3", "#ff9999", "#ff8080", "#ff6666", "#ff4d4d", "#ff3333", "#ff1a1a", "#ff0000", "#e60000", "#cc0000", "#b30000", "#990000", "#800000", "#660000", "#4d0000", "#330000", "#1a0000", "#f87171"]
        
        def animate_color(index=0):
            if self.closing:
                return
                
            if index < len(colors):
                self.status_label.configure(text_color=colors[index])
                self.app.after(20, lambda: animate_color(index + 1))
        
        animate_color()
    
    def clear_presence(self):
        if not self.rpc:
            self.status_label.configure(text="No active game to stop")
            return
            
        self.animate_loading_status("Stopping activity", self._clear_presence)
    
    def _clear_presence(self):
        try:
            if self.rpc:
                self.rpc.clear()
                self.rpc.close()
                self.rpc = None
                self.current_game = None
            
            color = ("orange", "#f97316")
            self.status_label.configure(
                text="🛑 Activity stopped",
                text_color=color
            )
            print("Presence cleared")
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Error: {e}",
                text_color=("red", "#f87171")
            )
            print("CLEAR ERROR:", e)
    
    def on_closing(self):
        self.closing = True
        
        if self.rpc and self.current_game:
            self.status_label.configure(
                text=f"Stopping {self.current_game} and closing...",
                text_color=("orange", "#f97316")
            )
            
            try:
                self.rpc.clear()
                self.rpc.close()
                print(f"Presence for {self.current_game} cleared before closing")
                
                self.animate_window_close(self.app.quit)
            except Exception as e:
                print(f"Error clearing presence: {e}")
                self.app.quit()
        else:
            self.animate_window_close(self.app.quit)
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = DiscordPlayApp()
    app.run()