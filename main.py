import multiprocessing
from arthur import Arthur
from utils import read_yaml
from aiartbutton import AiArtButton


def start_aiartbutton(GPIO_mode: str,
                      GPIO_button: int,
                      active_artwork_file_path: str,
                      image_directory: str,
                      button_sleep: float):
    button = AiArtButton(
        GPIO_mode=GPIO_mode,
        GPIO_button=GPIO_button,
        active_artwork_file_path=active_artwork_file_path,
        image_directory=image_directory,
        button_sleep=button_sleep
    )
    button.start()
    

def start_kiosk(active_artwork_file_path: str):
    arthur = Arthur(active_artwork_path=active_artwork_file_path)
    arthur.start()
    arthur.tk.mainloop()



if __name__ == '__main__':
    config = read_yaml('config.yaml')
    
    p_button = multiprocessing.Process(
        target=start_aiartbutton,
        args=(
            config['aiartbutton']['GPIO_mode'],
            config['aiartbutton']['GPIO_button'],
            config['active_artwork_file_path'],
            config['aiartbutton']['image_directory'],
            config['aiartbutton']['button_sleep']
        )
    )
    p_kiosk = multiprocessing.Process(
        target=start_kiosk,
        args=(config['active_artwork_file_path'], )
    )

    p_button.start()
    p_kiosk.start()

    p_button.join()
    p_kiosk.join()
