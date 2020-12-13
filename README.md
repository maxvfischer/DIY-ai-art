# Arthur
Run Arthur Kiosk on a Nvidia Jetson NX.

## Clone repository
```bash
git clone https://github.com/maxvfischer/Arthur.git
```

## Set up virtual environemnt
Install `venv`:
```bash
sudo apt-get install python3-venv
```

Create environment:
```bash
python3 -m venv venv
```

Activate environment:
```bash
source venv/bin/activate
```

Install `wheel`:
```bash
sudo pip3 install wheel
```

## Install dependencies
```bash
pip3 install -r requirements.txt
```

## Set up user permission
We need to set up user permissions to be able to access the GPIOs.

Create new GPIO user group (remember to change `your_user_name`):
```bash
sudo groupadd -f -r gpio
sudo usermod -a -G gpio your_user_name
```

Copy custom GPIO rules (remember to change `pythonNN`):
```bash
sudo cp venv/lib/pythonNN/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/
```

## Install xscreensaver
The default screen saver on Ubuntu is `gnome-screensaver`. It's not a screen saver in the traditional sense. Instead of showing moving images, it blanks the screen,
basically shuts down the HDMI signals to the screen, enabling the screen to fall into low energy mode.

The screen used in this project is a Samsung The Frame 32" (2020). When the screen is set to HDMI (1/2) and no HDMI signal is provided, it shows a static image telling the user that no HDMI signal is found. This is a unwanted behaviour in this set up, as we either wants the screen to go blank, or show some kind of a moving image, to reduce the risk of burn-in. We do not want to see a static
screen telling us that no hdmi signal is found.

To solve this problem, `xscreensaver` was installed instead. It's a screen saver that allows for moving images.

Full installation guide: https://askubuntu.com/questions/292995/configure-screensaver-in-ubuntu

```bash
sudo apt-get remove gnome-screensaver
sudo apt-get install xscreensaver xscreensaver-data-extra xscreensaver-gl-extra
```

## Add AI-model checkpoint
Copy the model checkpoint into `arthur/ml/checkpoint`:

    ├── arthur
         ├── ml
             ├── StyleGAN.model-XXXXXXX.data-00000-of-00001
             ├── StyleGAN.model-XXXXXXX.index
             └── StyleGAN.model-XXXXXXX.meta

## Add initial active artwork
Add an initial active artwork image by copying an image here: `arthur/active_artwork.jpg`

## Adjust config.yaml
The config.yaml contains all the settings.

```
active_artwork_file_path: 'active_artwork.jpg'  # Path and name of active artwork

aiartbutton:
  GPIO_mode: 'BOARD'  # GPIO mode
  GPIO_button: 15  # GPIO pinout used for the button
  image_directory: 'images'  # Directory to copy new images from
  button_sleep: 1.0  # Timeout in seconds after button has been pressed

ml_model:
  batch_size: 1  # Latent batch size used when generating images
  img_size: 1024  # Size of generated image (img_size, img_size)
  test_num: 20  # Number of images generated when model is triggered
  checkpoint_directory: 'ml/checkpoint'  # Checkpoint directory
  image_directory: 'images'  # Output directory of generated images
  lower_limit_num_images: 200  # Trigger model if number of images in image_directory is below this value
```

## Add 