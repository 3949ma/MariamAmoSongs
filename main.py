import os
import random
import traceback

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import (
    MDFlatButton,
    MDRaisedButton,
    MDIconButton,
)
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel

import arabic_reshaper
from bidi.algorithm import get_display


def fix_arabic(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))


FONT_NAME = "Roboto"

try:
    LabelBase.register(
        name="myfont",
        fn_regular="myfont.ttf"
    )
    FONT_NAME = "myfont"
except Exception:
    pass
    

class SplashScreen(Screen):
    pass


class ListScreen(Screen):
    pass


class PlayerScreen(Screen):
    pass


class FavoriteScreen(Screen):
    pass


class DeveloperScreen(Screen):
    pass


class NaderKhadrApp(MDApp):

    app_title = StringProperty(fix_arabic("موسوعة الأغاني السودانية"))
    current_song_title = StringProperty(fix_arabic("اختر أغنية"))
    current_lyrics = StringProperty("")
    current_poster = StringProperty("default_poster.png")

    time_label = StringProperty("00:00 / 00:00")
    next_song_preview = StringProperty("")
    smart_mood_tag = StringProperty("")

    song_length = NumericProperty(100)
    song_position = NumericProperty(0)

    image_angle = NumericProperty(0)

    is_playing = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    repeat_mode = BooleanProperty(False)
    shuffle_mode = BooleanProperty(False)
    sleep_timer_active = BooleanProperty(False)
    is_player_ready = BooleanProperty(False)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.player = None
        self.current_index = 0
        self.updating_track = None
        self.timer_dialog = None

        self.songs_list = []
        self.displayed_songs = []

        return Builder.load_file("main.kv")

    def on_start(self):
        self.songs_list = [
            {
                "title": "دالدومينق كو تراث دارفور",
                "file": "50.mp3",
                "poster": "default_poster.png",
                "lyrics": "دالدومينق كو",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "شرطاي سكيو",
                "file": "51.mp3",
                "poster": "default_poster.png",
                "lyrics": "شرطاي سكيو",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "كيلمانقا بقي",
                "file": "52.mp3",
                "poster": "default_poster.png",
                "lyrics": "كيلمانقا بقي",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "ناس دارفور كفاية المعاناة",
                "file": "53.mp3",
                "poster": "default_poster.png",
                "lyrics": "ناس دارفور كفاية المعاناة",
                "mood": "رسالة إنسانية",
                "fav": False,
            },
            {
                "title": "من أعلى مكان شفت أبعد مكان",
                "file": "54.mp3",
                "poster": "default_poster.png",
                "lyrics": "من أعلى مكان شفت أبعد مكان",
                "mood": "روائع مريم أمو",
                "fav": False,
            },
        ]

        self.displayed_songs = self.songs_list.copy()

        self.load_songs_menu()
        self.update_next_preview()

        Clock.schedule_once(self.switch_to_main, 2.5)
        
       
    def switch_to_main(self, dt):
        self.root.current = "list_screen"

    def format_time(self, seconds):
        seconds = max(0, int(seconds))
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_next_preview(self):
        if not self.songs_list:
            self.next_song_preview = ""
            return

        if self.shuffle_mode:
            self.next_song_preview = fix_arabic("التالي: تشغيل عشوائي")
        else:
            next_index = (self.current_index + 1) % len(self.songs_list)
            self.next_song_preview = fix_arabic(
                self.songs_list[next_index]["title"]
            )
            
    def load_songs_menu(self):
        from kivymd.uix.list import (
            OneLineAvatarIconListItem,
            IconRightWidget,
        )

        container = self.root.get_screen(
            "list_screen"
        ).ids.songs_container

        container.clear_widgets()

        for song in self.displayed_songs:

            item = OneLineAvatarIconListItem(
                text=fix_arabic(song["title"])
            )

            item.add_widget(
                IconRightWidget(icon="music-circle")
            )

            item.bind(
                on_release=lambda x, t=song["title"]:
                self.select_song_by_title(t)
            )

            container.add_widget(item)

    def select_song_by_title(self, title):

        for index, song in enumerate(self.songs_list):
            if song["title"] == title:
                self.current_index = index
                break

        self.play_current()
        self.root.current = "player_screen"
      
      
    def play_current(self):

        if not self.songs_list:
            return

        song = self.songs_list[self.current_index]

        self.current_song_title = fix_arabic(song["title"])
        self.current_lyrics = fix_arabic(song["lyrics"])
        self.current_poster = song["poster"]
        self.smart_mood_tag = fix_arabic(song["mood"])
        self.is_favorite = song["fav"]

        self.song_position = 0
        self.song_length = 100
        self.is_playing = True
        self.is_player_ready = True

        self.update_next_preview()

        if self.updating_track:
            self.updating_track.cancel()

        self.updating_track = Clock.schedule_interval(
            self.update_progress,
            1,
        )

    def update_progress(self, dt):

        if not self.is_playing:
            return

        self.song_position += 1

        if self.song_position > self.song_length:
            self.song_position = self.song_length

        self.time_label = (
            f"{self.format_time(self.song_position)} / "
            f"{self.format_time(self.song_length)}"
        )

        if self.song_position >= self.song_length:
            if self.repeat_mode:
                self.song_position = 0
            else:
                self.next_song()
      
      
    def next_song(self):

        if not self.songs_list:
            return

        if self.shuffle_mode:
            self.current_index = random.randint(
                0,
                len(self.songs_list) - 1,
            )
        else:
            self.current_index = (
                self.current_index + 1
            ) % len(self.songs_list)

        self.play_current()

    def previous_song(self):

        if not self.songs_list:
            return

        self.current_index = (
            self.current_index - 1
        ) % len(self.songs_list)

        self.play_current()

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        self.update_next_preview()

    def toggle_play(self):

        if not self.is_player_ready:
            self.play_current()
            return

        self.is_playing = not self.is_playing

    def stop_song(self):

        self.is_playing = False
        self.song_position = 0
        self.time_label = "00:00 / 00:00"

        if self.updating_track:
            self.updating_track.cancel()
            self.updating_track = None

    def seek_song(self, value):

        self.song_position = int(value)

        self.time_label = (
            f"{self.format_time(self.song_position)} / "
            f"{self.format_time(self.song_length)}"
        )


    def filter_songs(self, query):

        query = query.strip().lower()

        if not query:
            self.displayed_songs = self.songs_list.copy()
        else:
            self.displayed_songs = [
                song
                for song in self.songs_list
                if query in song["title"].lower()
            ]

        self.load_songs_menu()

    def toggle_favorite(self):

        if not self.songs_list:
            return

        song = self.songs_list[self.current_index]

        song["fav"] = not song["fav"]
        self.is_favorite = song["fav"]

        self.load_songs_menu()
        self.load_favorite_menu()

    def load_favorite_menu(self):

        from kivymd.uix.list import (
            OneLineAvatarIconListItem,
            IconRightWidget,
        )

        container = self.root.get_screen(
            "favorite_screen"
        ).ids.fav_songs_container

        container.clear_widgets()

        favorites = [
            song
            for song in self.songs_list
            if song["fav"]
        ]

        for song in favorites:

            item = OneLineAvatarIconListItem(
                text=fix_arabic(song["title"])
            )

            item.add_widget(
                IconRightWidget(icon="heart")
            )

            item.bind(
                on_release=lambda x, t=song["title"]:
                self.select_song_by_title(t)
            )

            container.add_widget(item)

    def set_sleep_timer(self):

        self.sleep_timer_active = not self.sleep_timer_active

        if self.sleep_timer_active:
            Clock.schedule_once(
                self.trigger_sleep,
                600,
            )

    def trigger_sleep(self, dt):

        self.sleep_timer_active = False

        self.stop_song()

        self.current_song_title = fix_arabic(
            "تم إيقاف التشغيل بواسطة مؤقت النوم"
        )

    def share_app(self):

        if platform != "android":
            return

        try:
            from jnius import autoclass

            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")

            intent.putExtra(
                Intent.EXTRA_TEXT,
                "موسوعة الأغاني السودانية"
            )

            chooser = Intent.createChooser(
                intent,
                "مشاركة التطبيق"
            )

            activity.startActivity(chooser)

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    NaderKhadrApp().run()
