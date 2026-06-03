import threading
import random
import requests
import time
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import speech_recognition as sr

CONVERSATION_HISTORY = []

class AplexInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.scroll = ScrollView()
        self.log_label = Label(
            text="[System Matrix]: Initializing Aplex...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.scroll.add_widget(self.log_label)
        self.add_widget(self.scroll)
        threading.Thread(target=self.start_aplex_core, daemon=True).start()

    def update_log(self, text):
        Clock.schedule_once(lambda dt: self._append_text(text))

    def _append_text(self, text):
        self.log_label.text += f"{text}\n"

    def start_aplex_core(self):
        r = sr.Recognizer()
        r.dynamic_energy_threshold = False
        r.energy_threshold = 40      
        r.pause_threshold = 0.5       
        self.update_log("[System Matrix]: Aplex Systems Fully Operational, sir.")
        
        aplex_wake_list = ["aplex", "apex", "plex", "alex", "apple x", "flex"]
        greetings = ["At your service, sir.", "Online and monitoring, sir."]

        while True:
            with sr.Microphone() as source:
                try:
                    r.adjust_for_ambient_noise(source, duration=0.1)
                    audio = r.listen(source, timeout=None, phrase_time_limit=2)
                    text = r.recognize_google(audio, language="en-IN").lower()
                    matched_word = next((word for word in aplex_wake_list if word in text), None)
                    
                    if matched_word:
                        self.update_log(f"\n[WAKE CODE RECOGNIZED: {matched_word}]")
                        self.update_log(f"Aplex: {random.choice(greetings)}")
                        audio_active = r.listen(source, timeout=4, phrase_time_limit=8)
                        command_text = r.recognize_google(audio_active, language="en-IN").lower()
                        self.update_log(f"[Decoded Text]: '{command_text}'")
                        self.process_command(command_text.strip())
                except Exception:
                    time.sleep(0.1)

    def process_command(self, command):
        if not command or len(command) < 2: return
        global CONVERSATION_HISTORY
        try:
            url = "https://text.pollinations.ai/"
            messages_payload = [{"role": "system", "content": "You are Aplex, built by Tanmoy Dey. Always address the user as sir."}]
            for item in CONVERSATION_HISTORY: messages_payload.append(item)
            messages_payload.append({"role": "user", "content": command})
            
            response = requests.post(url, json={"messages": messages_payload, "model": "openai"}, timeout=5)
            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content'].strip()
                self.update_log(f"Aplex: {reply}")
                CONVERSATION_HISTORY.append({"role": "user", "content": command})
                CONVERSATION_HISTORY.append({"role": "assistant", "content": reply})
        except Exception:
            self.update_log("Aplex: Link fluctuating, sir.")

class AplexApp(App):
    def build(self): return AplexInterface()

if __name__ == "__main__":
    AplexApp().run()
  
