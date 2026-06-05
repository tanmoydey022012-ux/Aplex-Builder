from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# --- NATIVE ANDROID UI SOUND ENGINE ---
try:
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    
    # Import native Android media sound systems for zero-delay UI sound feedback
    ToneGenerator = autoclass('android.media.ToneGenerator')
    AudioManager = autoclass('android.media.AudioManager')
    
    # Setup native audio chirps (skips heavy file assets)
    beep_click = ToneGenerator(AudioManager.STREAM_SYSTEM, 80)      # Standard keypress click
    beep_success = ToneGenerator(AudioManager.STREAM_SYSTEM, 100)   # Access Granted sound
    beep_alert = ToneGenerator(AudioManager.STREAM_SYSTEM, 100)     # Access Denied warning sound
except ImportError:
    activity = None
    beep_click = None
    beep_success = None
    beep_alert = None

class AplexInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Cyberpunk Palette Layout
        self.CYAN = "#00E5FF"
        self.MAGENTA = "#FF007F"
        self.DARK_BG = "#0A0E17"
        self.SURFACE = "#121B2A"
        
        self.is_active = False
        self.authenticated = False

        # --- HEADER ROW LAYER ---
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        header.add_widget(Label(text="[b]AI[/b]", markup=True, font_size='24sp', color=get_color_from_hex(self.CYAN), halign='left'))
        
        settings_btn = Button(text="⚙", font_size='24sp', size_hint_x=None, width=50, background_color=(0,0,0,0), color=get_color_from_hex(self.CYAN))
        settings_btn.bind(on_press=self.trigger_settings)
        header.add_widget(settings_btn)
        self.add_widget(header)

        # --- APP TITLE ---
        self.add_widget(Label(text="[b]APLEX[/b]", markup=True, font_size='32sp', size_hint_y=0.08, color=get_color_from_hex("#FFFFFF")))

        # --- SWITCHABLE CONTROL HOUSING CONTAINER ---
        self.workspace = BoxLayout(orientation='vertical', size_hint_y=0.67)
        self.add_widget(self.workspace)
        self.build_security_gate()

        # --- CONTROL DASHBOARD FOOTER ---
        footer_grid = GridLayout(cols=2, spacing=15, size_hint_y=0.15)
        
        bg_btn = Button(text="BACKGROUND\nUSE", font_size='14sp', halign='center', background_color=get_color_from_hex(self.SURFACE), color=get_color_from_hex(self.CYAN))
        bg_btn.bind(on_press=self.minimize_to_background)
        footer_grid.add_widget(bg_btn)
        
        term_btn = Button(text="TERMINAL\nACCESS", font_size='14sp', halign='center', background_color=get_color_from_hex(self.SURFACE), color=get_color_from_hex(self.CYAN))
        term_btn.bind(on_press=self.focus_terminal)
        footer_grid.add_widget(term_btn)
        
        self.add_widget(footer_grid)

    def play_sound(self, sound_type):
        """Fires instant, low-latency system-level electronic chirps"""
        if beep_click:
            try:
                if sound_type == "click":
                    beep_click.startTone(ToneGenerator.TONE_PROP_BEEP, 50) 
                elif sound_type == "success":
                    beep_success.startTone(ToneGenerator.TONE_CDMA_PIP, 150) 
                elif sound_type == "alert":
                    beep_alert.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 200) 
            except Exception:
                pass

    def build_security_gate(self):
        self.workspace.clear_widgets()
        gate_layout = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20])
        gate_layout.add_widget(Label(text="SYSTEM ENCRYPTED", font_size='18sp', color=get_color_from_hex(self.MAGENTA)))
        
        self.pass_input = TextInput(text="", password=True, multiline=False, size_hint_y=None, height=50, background_color=get_color_from_hex(self.SURFACE), foreground_color=get_color_from_hex("#FFFFFF"), hint_text="Enter lock password")
        self.pass_input.bind(on_text_validate=self.verify_password)
        gate_layout.add_widget(self.pass_input)
        
        unlock_btn = Button(text="DECRYPT CORE", size_hint_y=None, height=50, background_color=get_color_from_hex(self.MAGENTA))
        unlock_btn.bind(on_press=self.verify_password)
        gate_layout.add_widget(unlock_btn)
        self.workspace.add_widget(gate_layout)

    def verify_password(self, instance):
        if self.pass_input.text == "core7":
            self.play_sound("success")
            self.authenticated = True
            self.build_main_engine_ui()
        else:
            self.play_sound("alert")
            self.pass_input.text = ""
            self.pass_input.hint_text = "INVALID KEY - RE-ENTER"

    def build_main_engine_ui(self):
        self.workspace.clear_widgets()
        
        # Central Core UI Ring Button Placement
        anchor = AnchorLayout(size_hint_y=0.5)
        self.core_toggle_btn = Button(
            text="START",
            font_size='22sp',
            size_hint=(None, None),
            size=(180, 180),
            background_normal='',
            background_color=get_color_from_hex(self.CYAN),
            color=get_color_from_hex(self.DARK_BG)
        )
        self.core_toggle_btn.bind(on_press=self.toggle_core_state)
        anchor.add_widget(self.core_toggle_btn)
        self.workspace.add_widget(anchor)
        
        # Real-time System Scrolling Output Log Window
        self.scroll = ScrollView(size_hint_y=0.5)
        self.terminal_log = Label(
            text="Hello! CYBER_APLEX at your service.\nSystem authenticated. Status: ONLINE",
            font_size='14sp',
            markup=True,
            halign='left',
            valign='top',
            size_hint_y=None,
            color=get_color_from_hex("#FFFFFF")
        )
        self.terminal_log.bind(texture_size=self.terminal_log.setter('size'))
        self.scroll.add_widget(self.terminal_log)
        self.workspace.add_widget(self.scroll)

    def toggle_core_state(self, instance):
        self.play_sound("click")
        if not self.is_active:
            self.is_active = True
            self.core_toggle_btn.text = "STOP"
            self.core_toggle_btn.background_color = get_color_from_hex(self.MAGENTA)
            self.core_toggle_btn.color = get_color_from_hex("#FFFFFF")
            self.log_to_terminal("[color=00E5FF][b][SYSTEM][/b] Listening and processing...[/color]")
        else:
            self.is_active = False
            self.core_toggle_btn.text = "START"
            self.core_toggle_btn.background_color = get_color_from_hex(self.CYAN)
            self.core_toggle_btn.color = get_color_from_hex(self.DARK_BG)
            self.log_to_terminal("[color=FF007F][b][SYSTEM][/b] Core stopped voice recognition.[/color]")

    def log_to_terminal(self, message):
        if self.authenticated:
            self.terminal_log.text += f"\n{message}"

    def minimize_to_background(self, instance):
        self.play_sound("click")
        if self.authenticated:
            self.log_to_terminal("[b][CORE][/b] Moving to background tasks...")
            if activity:
                activity.moveTaskToBack(True)

    def focus_terminal(self, instance):
        self.play_sound("click")
        if self.authenticated:
            self.log_to_terminal("[b][SHELL][/b] Terminal frame focused.")

    def trigger_settings(self, instance):
        self.play_sound("click")
        if self.authenticated:
            self.log_to_terminal("[b][SYSTEM][/b] Opening Settings Panel...")

class MainCyberApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#0A0E17")
        return AplexInterface()

if __name__ == '__main__':
    MainCyberApp().run()
