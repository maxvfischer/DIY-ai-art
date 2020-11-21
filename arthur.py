import sys
import PIL.Image
import PIL.ImageTk
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from tkinter import *


class Arthur:
    """
    Kiosk GUI class displaying Arthur's art on full-screen.

    Parameters
    ----------
    active_artwork_path : str
        Path to active artwork to be displayed. If the active artwork image is updated, the new image will be rendered.
    """
    def __init__(self,
                 active_artwork_path: str) -> None:
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.label = None
        self.fullscreen_state = False
        self.tk.bind("<F11>", self._toggle_fullscreen)
        self.tk.bind("<Escape>", self._end_fullscreen)

        self.active_artwork_path = active_artwork_path
        self.image_last_modified = datetime.now()

        self._start_image_event_handler()

    def _start_image_event_handler(self) -> None:
        """Starts watchdog event handler looking for modificaitons to the active artwork image."""
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self._on_updated_image
        observer = Observer()
        observer.schedule(event_handler, path=self.active_artwork_path, recursive=False)
        observer.start() 

    def _toggle_fullscreen(self, event: Event = None) -> str:
        """Toggle Tkinter fullscreen state"""
        self.fullscreen_state = not self.fullscreen_state
        self.tk.attributes("-fullscreen", self.fullscreen_state)
        return "break"

    def _end_fullscreen(self, event: Event = None) -> str:
        """End Tkinter fullscreen state"""
        self.fullscreen_state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def _image_to_recently_modified(self) -> bool:
        """
        Check if active artwork image file was to recently modified.

        Returns
        -------
        bool
            If active artwork image file was to recentrly modified.
        """
        if datetime.now() - self.image_last_modified < timedelta(seconds=1):
            return True
        else:
            return False

    def _on_updated_image(self,
                          event: FileModifiedEvent) -> None:
        """
        Re-read active artwork image file and display file.

        Parameters
        ----------
        event : FileModifiedEvent
            Event body from watchdog event handler/observer

        Return
        ------
        None
        """
        if self._image_to_recently_modified():
            return

        img_path = event.src_path
        img = self._read_image(img_path=self.active_artwork_path)
        self.panel.configure(image=img)
        self.panel.image = img
        self.image_last_modified = datetime.now()

    @staticmethod
    def _read_image(img_path: str) -> Image:
        """
        Reads image to PIL ImageTk PhotoImage.

        Parameters
        ----------
        img_path : str
            Path to image.

        Returns
        -------
        Image
            PIL ImageTk PhotoImage.
        """
        img = PIL.Image.open(img_path)
        img = PIL.ImageTk.PhotoImage(img)
        return img

    def _setup_image_on_start(self) -> None:
        """Initially setting up and displaying the active artwork image."""
        img = self._read_image(img_path=self.active_artwork_path)
        self.panel = Label(self.tk, image=img)
        self.panel.image = img
        self.panel.pack()

    def start(self) -> None:
        """Start GUI"""
        self._setup_image_on_start()

