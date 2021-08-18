![main_gif](./tutorial_images/main_gif.gif)

This guide goes through all the steps to build your own AI art installation, using a button to 
change the AI artwork displayed on a screen. The main components used in this guide are:
 
* Nvidia Jetson Xavier NX (GPU-accelerated single-board computer)
* Screen with HDMI support
* Button to change artwork
* Passive infrared sensor to reduce risk of screen burn-in

It includes how to set up the computer to run an art kiosk (with code), how to build and assemble the control 
box, how to integrate the button and PIR sensor etc.

If you have any questions, feel free to contact me on LinkedIn: [https://www.linkedin.com/in/max-fischer-92997281/](https://www.linkedin.com/in/max-fischer-92997281/) 

or

![contact](./tutorial_images/contact.png)

![final_gif_1](./tutorial_images/final_ai_installation/final_gif.gif)

# Table of content
1. [Prepare the computer (Nvidia Jetson Xavier NX Dev Kit)](#prepare-the-computer-(nvidia-jetson-xavier-nx-dev-kit))
    1. [Install operating system](#install-operating-system)
    2. [Install base requirements](#install-base-requirements)
    3. [Install Jetson GPIO](#install-jetson-gpio)
    4. [Install xscreensaver (optional)](#install-xscreensaver-(optional))
    5. [Install Jetson stats (optional)](#install-jetson-stats-(optional))
2. [Install art kiosk](#install-art-kiosk)
3. [Add your generative code](#add-your-generative-code)
    1. [kiosk/arteventhandler.py](#kioskarteventhandlerpy)
    2. [main.py](#mainpy)
4. [Build the control box](#build-the-control-box)
    1. [Hand-cut parts](#hand-cut-parts)
    2. [Cut wood biscuits holes](#cut-wood-biscuits-holes)
    3. [Glue parts together](#glue-parts-together)
    4. [Remove visible gaps](#remove-visible-gaps)
    5. [Add hinges](#add-hinges)
    6. [Add magnetic lock](#add-magnetic-lock)
    7. [Milling edges](#milling-edges)
    8. [Drill PIR sensor hole](#drill-pir-sensor-hole)
    9. [Cut cable slots](#cut-cable-slots)
    10. [Vent holes](#vent-holes)
    11. [Spackling paste and sanding](#spackling-paste-and-sanding)
    12. [Painting](#painting)
5. [Build the button box](#build-the-button-box)
6. [Assemble art installation](#assemble-art-installation)
    1. [Screen](#screen)
    2. [Button box](#button-box)
    3. [Control box](#control-box)
    4. [Electronic components](#electronic-components)
        1. [Main power cable and junction box](#main-power-cable-and-junction-box)
        2. [Samsung One Connect box](#samsung-one-connect-box)
        3. [Nvidia Jetson's power adapter](#nvidia-jetson's-power-adapter)
        4. [Nvidia Jetson](#nvidia-jetson)
        4. [Connect cables](#connect-cables)
        5. [Button](#button)
        6. [PIR sensor](#pir-sensor)
7. [Final AI art installation](#final-ai-art-installation)

# Prepare the computer (Nvidia Jetson Xavier NX Dev Kit)
The Nvidia Jetson Xavier NX Development Kit 
([https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/)) is a single-board computer
with an integrated Nvidia Jetson Xavier NX module ([https://developer.nvidia.com/embedded/jetson-xavier-nx](https://developer.nvidia.com/embedded/jetson-xavier-nx)). It's 
developed by Nvidia for running computationally demanding tasks on edge. Similar to the Raspberry Pi, it has 40 GPIO pins that you can
interact with.

The development kit (version US/JP/TW) includes:

* x1 Nvidia Jetson Xavier NX
* x1 19.0V/2.37A power adapter
* x2 Power cables:
    * Plug type I -> C5
    * Plug type B -> C5
* Quick start / Support guide

![xavier_1](./tutorial_images/setup_computer/xavier_1.jpg)

![xavier_2](./tutorial_images/setup_computer/xavier_2.jpg)

## Install operating system
As the Raspberry Pi, Jetson Xavier is using a micro-SD card as its hard drive. As far as I know, there's only one 
supported OS image (Ubuntu) provided by Nvidia.

To install the OS, you'll need to use a second computer. 

Start of by downloading the OS image: [https://developer.nvidia.com/jetson-nx-developer-kit-sd-card-image](https://developer.nvidia.com/jetson-nx-developer-kit-sd-card-image).
To be able to download it, you need to sign up for a `NVIDIA Developer Program Membership`. It's free and quite useful 
as you'll get access to the Nvidia Developer forum. 

After you've downloaded it, unzip it. 

To flash the OS image to the micro-SD card, start of by inserting the micro-SD card into the second computer and list 
the available disks. Find the disk name of the micro-SD card you just inserted. In my case, it's `/dev/disk2`:

![xavier_4](./tutorial_images/setup_computer/xavier_4.svg)

When you've found the name of the micro-SD card, unmount it.

![xavier_5](./tutorial_images/setup_computer/xavier_5.svg)

Now, change your current directory to where you downloaded and un-zipped the OS image.

![xavier_6](./tutorial_images/setup_computer/xavier_6.svg)

To flash the micro-SD card with the OS image, run the command below. Replace `/dev/disk2` with the disk name of your 
micro-SD card and replace `sd-blob.img` with the name of the un-zipped image you downloaded. I've sped up the 
animation, flashing the card usually takes quite a long time (it took ~55 min @ ~4.6 MB/s for me).

![xavier_7](./tutorial_images/setup_computer/xavier_7.svg)

When you're done flashing the micro-SD card with the image, you're ready to boot up the Jetson! Remove the SD-card 
from the second computer and insert it into the Jetson computer. The SD-slot is found under the Xavier NX Module.

![xavier_8](./tutorial_images/setup_computer/xavier_8.jpg)

There's no power button, it will boot when you plug in the power cable. After booting and filling in the initial 
system configuration, you should see the Ubuntu desktop.

![xavier_9](./tutorial_images/setup_computer/xavier_9.gif)

If you get stuck during boot-up with an output as below, try to reboot the machine.
```bash
[ *** ] (1 of 2) A start job is running for End-user configuration after initial OEM installation...
```

Full installation guide from Nvidia can be found here: 
[https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit)

## Install base requirements
Update and upgrade apt-get

```
sudo apt-get update
sudo apt-get upgrade
```
If asked to choose between `gdm3` and `lightdm`, choose `gdm3`.

Reboot before continuing:

```bash
sudo reboot
```

After reboot, install pip3:

```bash
sudo apt install python3-pip
```

Install virtual environment:

```bash
sudo apt install -y python3-venv
```

Create a virtual environment in the directory `~/venvs` with the name `artkiosk`:

```bash
python3 -m venv ~/venvs/artkiosk
```

Activate the virtual environment:

```bash
source ~/venvs/artkiosk/bin/activate
```

Install python wheel:

```bash
pip3 install wheel
```

## Install Jetson GPIO
[Jetson.GPIO](https://github.com/NVIDIA/jetson-gpio) is a Python package developed by Nvidia that works in the same way
as RPi.GPIO, but for the Jetson family of computers. It enables the user to, through Python code, interact with the GPIO 
pinouts on the Jetson computer.

First, install the Jetson.GPIO package into the virtual environment:

```bash
pip3 install Jetson.GPIO
```

Then, set up user permissions to be able to access the GPIOs. Create a new GPIO user group (replace 
`your_user_name`):

```bash
sudo groupadd -f -r gpio
sudo usermod -a -G gpio your_user_name
```

Copy custom GPIO rules (replace `pythonNN` with your Python version):

```bash
sudo cp venvs/artkiosk/lib/pythonNN/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/
```

Full installation guide can be found here: [https://github.com/NVIDIA/jetson-gpio#installation](https://github.com/NVIDIA/jetson-gpio#installation)

## Install xscreensaver (optional)
To reduce the risk of burn-in when displaying static art on the screen, a PIR (passive infrared) sensor was integrated. 
When no movement has been registered around the art installation, a screen saver was triggered.

The default screen saver on Ubuntu is `gnome-screensaver`. It's not a screen saver in the "traditional sense". Instead of 
showing moving images, it blanks the screen, basically shutting down the HDMI signals to the screen, enabling the screen to fall into low energy mode.

The screen I used in this project was a Samsung The Frame 32" (2020). When the screen was set to HDMI (1/2) and no HDMI 
signal was provided, it showed a static image telling the user that no HDMI signal is found. This is an unwanted behaviour in this set up, as we either 
wants the screen to go blank, or show some kind of a moving image, to reduce the risk of burn-in. We do not want to see 
a new static screen telling us that no hdmi signal is found.

To solve this problem, `xscreensaver` was installed instead. It's an alternative screen saver that support moving 
images. Also, it seems like `xscreensaver's` blank screen mode works differently than `gnome-screensaver`. When 
`xscreensaver's` blank screen is triggered, it doesn't seems to shut down the HDMI signal, but rather turn the screen 
black. This is the behaviour we want in this installation. 

If you're experiencing the same challenge as I did with the screen saver, follow these steps 
to uninstall `gnome-screensaver` and install `xscreensaver`:

```bash
sudo apt-get remove gnome-screensaver
sudo apt-get install xscreensaver xscreensaver-data-extra xscreensaver-gl-extra
```
After uninstalling `gnome-screensaver` and installing `xscreensaver`, it was added to `Startup Applications`:

![screen_saver_installation_1](./tutorial_images/setup_computer/screen_saver_installation_1.png)

![screen_saver_installation_2](./tutorial_images/setup_computer/screen_saver_installation_2.png)


Full installation guide: [https://askubuntu.com/questions/292995/configure-screensaver-in-ubuntu/293014#293014](https://askubuntu.com/questions/292995/configure-screensaver-in-ubuntu/293014#293014)

## Install Jetson stats (optional)
[Jetson stats](https://github.com/rbonghi/jetson_stats) is a really useful open-source package to monitor and control 
the Jetson. It enables you to track CPU/GPU/Memory usage, check temperatures, increase the swap memory etc.

To install Jetson stats:

```bash
sudo -H pip install -U jetson-stats
```

Reboot your machine:

```bash
sudo reboot
```

Activate the virtual environment again after reboot:

```bash
source ~/venvs/artkiosk/bin/activate
```

To check CPU/GPU/Memory usage etc:

```bash
jtop
```

Full list of commands can be found here: [https://github.com/rbonghi/jetson_stats](https://github.com/rbonghi/jetson_stats)

# Install art kiosk
We're now ready to install the art kiosk on the computer! 

Start by clone this repository:

```bash
git clone https://github.com/maxvfischer/DIY-ai-art.git
```

Change active directory and install the dependencies:

```bash
cd DIY-ai-art
pip3 install -r requirements.txt
```

The art kiosk is started by executing:

```bash
python3 -m main
```

NOTE: The art kiosk will **NOT** work properly if you don't attach the button and the PIR sensor. Please continue to 
follow the instructions.

The program running the art kiosk is written in `Python` 
and is running as 4 parallel processes, each implemented as its own class: `Kiosk`, `ArtButton`, `PIRSensorScreensaver` 
and `GANEventHandler`. The entry point is `main.py` and all the parameters used are defined in `config.yaml` (e.g. path to 
image directory, GPIO pinouts used etc).

![screen_saver_installation_1](./tutorial_images/install_art_kiosk/art_kiosk_diagram.png)

| **Process/Class**              | **File**                   | **Description**                                                                                                                                                                                                                                                                                                                                                                                      |
|--------------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Kiosk**                      | kiosk/kiosk.py             |The `Kiosk` process handles all the GUI: toggling (\<F11>) and ending (\<Escape>) fullscreen, listens to change of the active artwork to be displayed etc.                                                                                                                                                                                                                                            |
| **ArtButton**                  | kiosk/artbutton.py         |The `ArtButton` process listens to a GPIO pinout connected to a button. When the button is pushed and the GPIO is triggered, it replaces the active artwork file with a random image sampled from the image directory.                                                                                                   |
| **PIRSensorScreensaver**       | kiosk/pirsensorscreensaver |The `PIRSensorScreensaver` process listens to a GPIO pinout connected to a PIR sensor. When no motion has triggered the PIR sensor within a predefined threshold of seconds, the computer's screensaver is activated. When motion is detected, the screensaver is deactivated.                                              |
| **ArtEventHandler**            | kiosk/art_event_handler.py             |The `ArtEventHandler` process is listening to deleted items in the image directory. When the button is clicked and an image is deleted (i.e. moved to replace the active artwork file, active_artwork.jpg), this process checks how many images that are left in the image directory. If the number of images falls are below a predefined threshold, a new process (function) is spawned, generating a new set of images. You need to update this class to generate the images. |

# Add your generative code
You need to add your own generative code (GAN-network or others), by updating two files:

* kiosk/arteventhandler.py
* main.py

## kiosk/arteventhandler.py
The class `ArtEventHandler` found in the file `kiosk/arteventhandler.py` is an event handler that is triggered to generate new images to be saved in the image directory. When an image is deleted from the image directory (i.e. moved to replace the active artwork), `ArtEventHandler's` class function `on_deleted` is executed. It checks if the number of images found in the image directory is above or below a pre-defined threshold. If the number of images falls below the threshold, `ArtEventHandler's` class function `generate_images` is executed. It is in this function that you need to add your generative code that will add new images to the image directory.

## main.py
If you have updated `ArtEventHandler's` constructor with new arguments, you need to update the initialization of `ArtEventHandler` in the function `start_art_generator` found in `main.py`.

# Build the control box
To get a nice looking installation with as few visible cables as possible, a control box was built to encapsulate the Nvidia computer, power adapters, Samsung One Connect box etc.

## Hand-cut parts
The control box was build using 12mm (0.472") MDF. A vertical panel saw was used to cut down the MDF into smaller pieces. A table saw was used to cut out the final pieces.

![raw_mdf](./tutorial_images/build_control_box/raw_mdf.jpg)

![vertical_panel_saw](./tutorial_images/build_control_box/vertical_panel_saw.jpg)

![table_saw](./tutorial_images/build_control_box/table_saw.jpg)

| Piece              | Dimensions (width, height)    | Sketch                                                                         |
|--------------------|-------------------------------|--------------------------------------------------------------------------------|
| Bottom base panel  | 320mm x 235mm                 | ![table_saw](./tutorial_images/build_control_box/bottom_base_panel_sketch.png) |
| Top lid panel      | 344mm x 259mm                 | ![table_saw](./tutorial_images/build_control_box/top_lid_panel_sketch.png)     |
| Left side panel    | 235mm x 57mm                  | ![table_saw](./tutorial_images/build_control_box/left_side_panel_sketch.png)   |
| Right side panel   | 235mm x 57mm                  | ![table_saw](./tutorial_images/build_control_box/right_side_panel_sketch.png)  |
| Top side panel     | 344mm x 57mm                  | ![table_saw](./tutorial_images/build_control_box/top_side_panel_sketch.png)    |
| Bottom side panel  | 344mm x 57mm                  | ![table_saw](./tutorial_images/build_control_box/bottom_side_panel_sketch.png) |

![raw_pieces](./tutorial_images/build_control_box/raw_pieces.jpg)

![raw_pieces_with_lid](./tutorial_images/build_control_box/raw_pieces_with_lid.jpg)

## Cut wood biscuits holes
To make the control box robust, wood biscuits were used to glue the parts together. By using wood biscuits, 
no screws were needed, thus giving a nice finish without visible screw heads. It also helps to aligning the
pieces when gluing.

When using the wood biscuit cutter, it's important that the holes end up at the correct place at the 
aligning panels. One simple way of solving this is to align your panels and then draw a line on both 
panels at the center of where you want the biscuit to be. If you do this, the holes will end up at the 
right place.

![wood_biscuit_align](./tutorial_images/build_control_box/wood_biscuit_align.jpg)

![wood_biscuit_machine_1](./tutorial_images/build_control_box/wood_biscuit_machine_1.jpg)

![wood_biscuit_machine_2](./tutorial_images/build_control_box/wood_biscuit_machine_2.jpg)

![wood_biscuit_all_pieces](./tutorial_images/build_control_box/wood_biscuit_all_pieces.jpg)

Before gluing the pieces together, check that the connecting holes are correctly aligning and that all
wood biscuits fit nicely (they can somethings vary a bit in size).

![wood_biscuit_asseble](./tutorial_images/build_control_box/wood_biscuit_asseble.jpg)

## Glue parts together
When gluing the parts together, you'll need to be fairly quick and structured. Prepare by placing the 
aligning panels next to each other and have all the wood biscuits ready.

![gluing_1](./tutorial_images/build_control_box/gluing_1.jpg)

![gluing_2](./tutorial_images/build_control_box/gluing_2.jpg)

Start of by adding the glue in the wood biscuit holes.

![gluing_3](./tutorial_images/build_control_box/gluing_3.jpg)

Then, press down the wood biscuits into the holes and apply wood glue along all the connecting parts.

![gluing_4](./tutorial_images/build_control_box/gluing_4.jpg)

Now, assemble all the connecting parts and apply force using clamps. You should see
glue seeping out between the panels.

![gluing_5](./tutorial_images/build_control_box/gluing_5.jpg)

Use an engineer's square to check each corner.

![gluing_6](./tutorial_images/build_control_box/gluing_6.jpg)

Finally, remove all the visible redundant glue with a wet paper tissue.

![gluing_7](./tutorial_images/build_control_box/gluing_7.jpg)

![gluing_8](./tutorial_images/build_control_box/gluing_8.jpg)

## Remove visible gaps
After removing the clamps, there were some visible gaps and cracks that needed to be filled.

![spackling_1](./tutorial_images/build_control_box/spackling_1.jpg)

![spackling_2](./tutorial_images/build_control_box/spackling_2.jpg)

![spackling_3](./tutorial_images/build_control_box/spackling_3.jpg)

I used plastic padding (a two component plastic spackling paste) to cover up the gaps and cracks. Be careful with how 
much hardener you add, as it will dry very quickly if adding too much.

![spackling_4](./tutorial_images/build_control_box/spackling_4.jpg)

![spackling_5](./tutorial_images/build_control_box/spackling_5.jpg)

![spackling_6](./tutorial_images/build_control_box/spackling_6.jpg)

![spackling_7](./tutorial_images/build_control_box/spackling_7.jpg)

When everything had dried, an electric sander was used to remove redundant plastic padding.
The inside of the box was smoothed by manual sanding. As a rule of thumb, if you can
feel an edge or a crack, it will be visible when painted.

![spackling_8](./tutorial_images/build_control_box/spackling_8.jpg)

![spackling_9](./tutorial_images/build_control_box/spackling_9.jpg)

## Add hinges
The hinges were first added to the lid. It made it easier to align the lid on top of the box 
later on.

The hinge mortises were measured and outlined. An electric multicutter tool was then used 
to cut out a grid with the same depth as the hinges. The material was then removed using 
a chisel and a hammer. The mortises were then smoothed
by manual sanding.

![hinge_1](./tutorial_images/build_control_box/hinge_1.jpg)

![hinge_2](./tutorial_images/build_control_box/hinge_2.jpg)

![hinge_3](./tutorial_images/build_control_box/hinge_3.jpg)

![hinge_4](./tutorial_images/build_control_box/hinge_4.jpg)

![hinge_5](./tutorial_images/build_control_box/hinge_5.jpg)

![hinge_6](./tutorial_images/build_control_box/hinge_6.jpg)

The hinges were aligned and a bradawl was used to mark the centers of the holes. MDF is a 
very dense material, therefore it's important to pre-drill before screwing the hinges in 
place. If you don't do this, there's a high risk that the material will crack.

![hinge_7](./tutorial_images/build_control_box/hinge_7.jpg)

![hinge_8](./tutorial_images/build_control_box/hinge_8.jpg)

The depth of the screws were measured and adhesive tape was used to mark the depth
on the drill head. 

![hinge_9](./tutorial_images/build_control_box/hinge_9.jpg)

![hinge_10](./tutorial_images/build_control_box/hinge_10.jpg)

![hinge_11](./tutorial_images/build_control_box/hinge_11.jpg)

Before aligning the hinges on the box, make sure to add some support under the lid,
it should be able to rest at the same level as the control box. Double-coated adhesive tape 
was then attached to each hinge and the lid was aligned on top of the box. When the 
lid was correctly aligned, pressure was applied to make the adhesive tape stick.

![hinge_12](./tutorial_images/build_control_box/hinge_12.jpg)

![hinge_13](./tutorial_images/build_control_box/hinge_13.jpg)

![hinge_14](./tutorial_images/build_control_box/hinge_14.jpg)

The hinge holes and the mortises were drilled and cut out in the same way as on
the lid.

![hinge_15](./tutorial_images/build_control_box/hinge_15.jpg)

![hinge_16](./tutorial_images/build_control_box/hinge_16.jpg)

![hinge_17](./tutorial_images/build_control_box/hinge_17.jpg)

![hinge_18](./tutorial_images/build_control_box/hinge_18.jpg)

![hinge_19](./tutorial_images/build_control_box/hinge_19.jpg)

![hinge_20](./tutorial_images/build_control_box/hinge_20.jpg)

![hinge_21](./tutorial_images/build_control_box/hinge_21.jpg)

![hinge_22](./tutorial_images/build_control_box/hinge_22.jpg)

![hinge_23](./tutorial_images/build_control_box/hinge_23.jpg)

![hinge_24](./tutorial_images/build_control_box/hinge_24.jpg)

## Add magnetic lock
A magnetic lock was used to keep the lid in place.

![magnetic_lock_1](./tutorial_images/build_control_box/magnetic_lock_1.jpg)

![magnetic_lock_2](./tutorial_images/build_control_box/magnetic_lock_2.jpg)

![magnetic_lock_3](./tutorial_images/build_control_box/magnetic_lock_3.jpg)

![magnetic_lock_4](./tutorial_images/build_control_box/magnetic_lock_4.jpg)

![magnetic_lock_5](./tutorial_images/build_control_box/magnetic_lock_5.jpg)

![magnetic_lock_6](./tutorial_images/build_control_box/magnetic_lock_6.jpg)

![magnetic_lock_7](./tutorial_images/build_control_box/magnetic_lock_7.jpg)

![magnetic_lock_8](./tutorial_images/build_control_box/magnetic_lock_8.jpg)

![magnetic_lock_9](./tutorial_images/build_control_box/magnetic_lock_9.jpg)

## Milling edges
All the edges were rounded using a handheld milling machine.

![milling_1](./tutorial_images/build_control_box/milling_1.jpg)

![milling_2](./tutorial_images/build_control_box/milling_2.jpg)

![milling_3](./tutorial_images/build_control_box/milling_3.jpg)

## Drill PIR sensor hole
To integrate the PIR sensor, the control box was disassembled. A hole was 
then measured, aligned and drilled all the way through the lid to enable 
the PIR reflector to stick out. A larger drill with the same diameter as the 
sensor chip was then used to carefully extend the slot from the inside of the lid. 
The extended hole was not drilled all the way through, approximately 2 mm was 
left for the sensor chip to rest on. Finally, a sand paper was used to manually 
sand the edges for a perfect fit.

![pir_sensor_1](./tutorial_images/build_control_box/pir_sensor_1.jpg)

![pir_sensor_2](./tutorial_images/build_control_box/pir_sensor_2.jpg)

![pir_sensor_3](./tutorial_images/build_control_box/pir_sensor_3.jpg)

![pir_sensor_4](./tutorial_images/build_control_box/pir_sensor_4.jpg)

![pir_sensor_5](./tutorial_images/build_control_box/pir_sensor_5.jpg)

![pir_sensor_6](./tutorial_images/build_control_box/pir_sensor_6.jpg)

## Cut cable slots
To enable the cables to go in and out of the box, two cable slots were cut out:

1. One cable slot in the top side panel for the One Connect cable and button cables.
2. One cable slot in the bottom side panel for the electrical cable.

Initially, the cable slots were only cut half way through the top and bottom panels. 
But I then realized (after I had assembled and painted everything ¯\\(ツ)/¯), that it will look much better if I cut the 
cable slots all the way through and then glue a piece of MDF into the hole to cover up the redundant space. That's why 
the control box is painted in the images below.

A caliper was used to measure the diameter of the cables. An extra ~1mm was then added to the slots for the cables to fit nicely. But in hindsight I would've extended the slot 2-3 mm more.

![caliper](./tutorial_images/build_control_box/caliper.jpg)

The slots were then outlined at the center of the top and bottom panels. The outlines were also extended approximately 
15 mm into the back panel. A Japanese hand saw/Dozuki saw was used to cut out the slots. A small chisel and a hammer was used to remove the cut out pieces.

![cable_slot_4](./tutorial_images/build_control_box/cable_slot_4.jpg)

![cable_slot_5](./tutorial_images/build_control_box/cable_slot_5.jpg)

![cable_slot_7](./tutorial_images/build_control_box/cable_slot_7.jpg)

![cable_slot_6](./tutorial_images/build_control_box/cable_slot_6.jpg)

A hole saw was used to extract a larger hole in the top of the back panel, connected to the top panel's cable slot. It 
enabled the One Connect Cable to be inserted.

![cable_slot_8](./tutorial_images/build_control_box/cable_slot_8.jpg)

Pieces of MDF with the same width and height as the cable slots were cut out. Sand paper was used to do small 
adjustments. The cables were then inserted into the slots and the MDF pieces were aligned and cut to give just enought 
space for the cables to fit.

![cable_slot_11](./tutorial_images/build_control_box/cable_slot_11.jpg)

![cable_slot_9](./tutorial_images/build_control_box/cable_slot_9.jpg)

![cable_slot_10](./tutorial_images/build_control_box/cable_slot_10.jpg)

Wood glue were applied and smeared out on the connecting parts. The MDF pieces were then squeezed 
into the slots.

![cable_slot_11](./tutorial_images/build_control_box/cable_slot_12.jpg)

![cable_slot_12](./tutorial_images/build_control_box/cable_slot_13.jpg)

![cable_slot_13](./tutorial_images/build_control_box/cable_slot_14.jpg)

## Vent holes
Vent holes were drilled in the bottom and the top panel to enable heat to flow out of the control box.

![vent_holes_1](./tutorial_images/build_control_box/vent_holes_1.jpg)

![vent_holes_2](./tutorial_images/build_control_box/vent_holes_2.jpg)

## Spackling paste and sanding
Plastic padding were used cover the cracks between the cables slots and the glued MDF pieces. The control box was then 
manually sanded to remove the redundant plastic padding and round the edges around the vent holes etc. 

![spackling_11](./tutorial_images/build_control_box/spackling_11.jpg)

![spackling_12](./tutorial_images/build_control_box/spackling_12.jpg)

![spackling_13](./tutorial_images/build_control_box/spackling_13.jpg)

![spackling_10](./tutorial_images/build_control_box/spackling_10.jpg)

## Painting
The control box was painted in the same color as the wall it was attached to. A tip is to buy a color sample can 
instead of a full can. You will not need a full can, and the sample cans are usually cheaper per litre.

A paint roller was used on the flat areas and a small brush was used to paint the smaller details.

![painting_1](./tutorial_images/build_control_box/painting_1.jpg)

![painting_2](./tutorial_images/build_control_box/painting_2.jpg)

![painting_3](./tutorial_images/build_control_box/painting_3.jpg)

![painting_4](./tutorial_images/build_control_box/painting_4.jpg)

![painting_5](./tutorial_images/build_control_box/painting_5.jpg)

After the paint had dried, everything was reassembled.

![painting_6](./tutorial_images/build_control_box/painting_6.jpg)

# Build the button box
A modified black plastic enclosure box was used as a button box. To integrate the 
button, the vertical and horizontal center was first measured and pre-drilled. Then, 
a hole with the diameter of the button was drilled.

![button_box_1](./tutorial_images/build_button_box/button_box_1.jpg)

![button_box_2](./tutorial_images/build_button_box/button_box_2.jpg)

![button_box_3](./tutorial_images/build_button_box/button_box_3.jpg)

![button_box_4](./tutorial_images/build_button_box/button_box_4.jpg)

![button_box_5](./tutorial_images/build_button_box/button_box_5.jpg)

As the button box will be located between the control box and the screen, the two 
button cables and the One Connect cable (bringing electricity and HDMI to the screen) 
will enter the button box at the bottom. The One Connect cable will also exit 
the button box at the top (continuing to the TV). Two cable slots were therefore extracted at the top
and the bottom, using a Japanese hand saw/Dozuki saw. The slots were then smoothed
by manual sanding.

![button_box_6](./tutorial_images/build_button_box/button_box_6.jpg)

![button_box_7](./tutorial_images/build_button_box/button_box_7.jpg)

![button_box_8](./tutorial_images/build_button_box/button_box_8.jpg)

The screws keeping the enclosure box together were colored black using an aerosol varnish paint. A tip
when painting screws is to stick them into a piece of styrofoam.

![button_box_9](./tutorial_images/build_button_box/button_box_9.jpg)

![button_box_10](./tutorial_images/build_button_box/button_box_10.jpg)

# Assemble art installation
The art installation was now ready to be assembled and attached to the wall. A cross line laser was used to vertically align the screen, button box and control box. 

## Screen
The screen (Samsung The Frame 32" 2020) was wall-mounted following the instructions included when buying the screen.

![assembly_1](./tutorial_images/assemble_art_installation/assembly_1.jpg)

## Button box
Two screw holes were drilled in the bottom plate of the button box. Double-coated adhesive tape was also attached
to the back side of the bottom plate for further support. The button box was then aligned using the laser and
attached to the wall using two wall plugs, the two screws and the double-coated adhesive tape.

![assembly_3](./tutorial_images/assemble_art_installation/assembly_3.jpg)

![assembly_6](./tutorial_images/assemble_art_installation/assembly_6.jpg)

![assembly_4](./tutorial_images/assemble_art_installation/assembly_4.jpg)

![assembly_5](./tutorial_images/assemble_art_installation/assembly_5.jpg)

![assembly_7](./tutorial_images/assemble_art_installation/assembly_7.jpg)

![assembly_8](./tutorial_images/assemble_art_installation/assembly_8.jpg)

![assembly_9](./tutorial_images/assemble_art_installation/assembly_9.jpg)

## Control box
The control box was attached to the wall using wall plug and two screws. To be able to outline the screw holes, all the electronics were temporarily placed in the control box and two screw holes were outlined and drilled. The HDMI/One Connect
cable were then inserted into the cable slot and the control box was attached to the wall. 

![assembly_10](./tutorial_images/assemble_art_installation/assembly_10.jpg)

![assembly_11](./tutorial_images/assemble_art_installation/assembly_11.jpg)

![assembly_12](./tutorial_images/assemble_art_installation/assembly_12.jpg)

![assembly_13](./tutorial_images/assemble_art_installation/assembly_13.jpg)

## Electronic components

**NOTE: THIS PART INCLUDES WIRING OF HIGH VOLTAGE ELECTRICITY THAT CAN BE
LETHAL IF NOT DONE PROPERLY. THE COLORS OF THE CABLES CAN VARY DEPENDING ON 
REGION/COUNTRY. BEFORE YOU CONNECT THE POWER CORD TO THE POWER OUTLET, CONSULT WITH A LICENSED ELECTRICIAN TO MAKE SURE THAT EVERYTHING IS PROPERLY WIRED 
AND THAT IT IS IN LINE WITH YOUR LOCAL LEGISLATIONS.**


### Main power cable and junction box

The female side of the main power cord was removed and the cable was inserted
into the control box. A junction box was then attach in the bottom right 
corner using velcro tape. Before the velcro tape was attached, the backside of the junction box was cleaned with denatured alcohol. Three holes were created in the side of the junction box to enable three cables to enter.

![assembly_14](./tutorial_images/assemble_art_installation/assembly_14.jpg)

![assembly_15](./tutorial_images/assemble_art_installation/assembly_15.jpg)

![assembly_16](./tutorial_images/assemble_art_installation/assembly_16.jpg)

![assembly_17](./tutorial_images/assemble_art_installation/assembly_17.jpg)

![assembly_18](./tutorial_images/assemble_art_installation/assembly_18.jpg)

![assembly_19](./tutorial_images/assemble_art_installation/assembly_19.jpg)

A wire stripper was used to strip the jacket/insulation of the power cord, 
as well as the wires inside. A splicing connector (Wago 221, 3-conductor) was then 
attached to each wire, enabling electricity from a single power outlet to be 
split to the One Connect Box and to the Nvidia Jetson Xavier NX, without using 
a power strip.

![assembly_54](./tutorial_images/assemble_art_installation/assembly_54.jpg)

![assembly_20](./tutorial_images/assemble_art_installation/assembly_20.jpg)

![assembly_21](./tutorial_images/assemble_art_installation/assembly_21.jpg)

![assembly_22](./tutorial_images/assemble_art_installation/assembly_22.jpg)

### Samsung One Connect box

The Samsung One Connect box was then attached in the left bottom corner using
velcro tape. Some margin was left below and to the left of the One Connect box for the power cord and for the PIR sensor cables. Also, the backside of the One Connect Box was cleaned using denatured alcohol before attaching the velcro tape. 

![assembly_23](./tutorial_images/assemble_art_installation/assembly_23.jpg)

![assembly_24](./tutorial_images/assemble_art_installation/assembly_24.jpg)

The screen's power cord (IEC C7 coupler) was inserted into the One Connect 
Box. It was then aligned, measured and cut at an appropriate length to reach 
inside the junction box. The wire stripper was used to remove the jacket/insulation of the power cord, as well as the wires inside. The C7 cable was 
then inserted into the junction box and connected to the splicing connectors. 
The ground was left out as the C7 coupler is ungrounded.

![assembly_26](./tutorial_images/assemble_art_installation/assembly_26.jpg)

![assembly_25](./tutorial_images/assemble_art_installation/assembly_25.jpg)

![assembly_27](./tutorial_images/assemble_art_installation/assembly_27.jpg)

### Nvidia Jetson's power adapter

The power adapter to the Nvidia Jetson Xavier NX was attached in the top left 
corner using velcro tape. The power cord (IEC C5 coupler) was inserted 
into the power adapter. It was then aligned, measured and cut at an appropriate 
length to reach inside the junction box. The wire stripper was used to remove 
the jacket/insulation of the power cord, as well as the wires inside. The C5 
cable was then inserted into the junction box and connected to the splicing 
connectors.

![assembly_28](./tutorial_images/assemble_art_installation/assembly_28.jpg)

![assembly_29](./tutorial_images/assemble_art_installation/assembly_29.jpg)

![assembly_30](./tutorial_images/assemble_art_installation/assembly_30.jpg)

![assembly_31](./tutorial_images/assemble_art_installation/assembly_31.jpg)

Before closing the junction box, cable ties were tightened around each cable 
going into the junction box as strain reliefs.

![assembly_32](./tutorial_images/assemble_art_installation/assembly_32.jpg)

![assembly_55](./tutorial_images/assemble_art_installation/assembly_55.jpg)

### Nvidia Jetson

To attach the Nvidia Jetson, two pieces of galvanised band was cut out and wrapped 
in insulating tape. The computer was then attached in the top right corner 
using 4 small screws and washers.

![assembly_56](./tutorial_images/assemble_art_installation/assembly_56.jpg)

![assembly_57](./tutorial_images/assemble_art_installation/assembly_57.jpg)

![assembly_58](./tutorial_images/assemble_art_installation/assembly_58.jpg)

![assembly_33](./tutorial_images/assemble_art_installation/assembly_33.jpg)

![assembly_34](./tutorial_images/assemble_art_installation/assembly_34.jpg)

### Connect cables

The HDMI, the One Connect Cable and the Xavier NX power cable were connected. 
Cable ties were used to structure the cables.

![assembly_35](./tutorial_images/assemble_art_installation/assembly_35.jpg)

![assembly_36](./tutorial_images/assemble_art_installation/assembly_36.jpg)

### Button

The button changing the artwork was implemented as a pull-up resistor. When the button is "off" (i.e. not pushed), a small current will flow from the positive 3.3v, through the resistor and into the GPIO pin, leading to the GPIO pin being HIGH (1). On the other hand, when the button is pushed, the current will flow from the positive 3.3v, through the resistor, via the button and into ground (GND). This will lead to the GPIO pin being LOW (0). This shift in HIGH/LOW on the GPIO pin is registered in the code and is used to change the artwork on the screen. The schema for the pull-up resistor can be found below.

![pull_up_resistor](./tutorial_images/assemble_art_installation/pull-up_resistor.png)

Two cables were measured and soldered to the button. The cables were then 
inserted into the control box via the same cable slot as the One Connect cable. 
Make sure that you have enough cable to reach to the Nvidia Jetson computer.

![assembly_37](./tutorial_images/assemble_art_installation/assembly_37.jpg)

The end of a female jumping wire were then soldered to the end of the cable 
connecting to the ground (for being able to unplug the cable easily). Before 
soldering the two cables together, one of the cables were passed through a 
shrinking tube. After the cables were soldered together, a blow torch was used 
to shrink the tube around the soldering.

![assembly_38](./tutorial_images/assemble_art_installation/assembly_38.jpg)

A 1kΩ resistor and a female jumping wire were soldered to the other button 
cable. Finally, another female jumping cable were soldered to the other side of 
the resistor.

![assembly_39](./tutorial_images/assemble_art_installation/assembly_39.jpg)

![assembly_40](./tutorial_images/assemble_art_installation/assembly_40.jpg)

![assembly_41](./tutorial_images/assemble_art_installation/assembly_41.jpg)

![assembly_42](./tutorial_images/assemble_art_installation/assembly_42.jpg)

The jumping wires were then connected to the following Nvidia Jetson GPIOs:

* Blue: Ground (pin 14)
* Red: 3.3v (pin 17)
* Green: GPIO (pin 15)

![button_pinout](./tutorial_images/assemble_art_installation/button_pinout.png)

![assembly_43](./tutorial_images/assemble_art_installation/assembly_43.jpg)

The Samsung One Connect cable were finally inserted through the button box and the button box's top plate was attached.

![assembly_44](./tutorial_images/assemble_art_installation/assembly_44.jpg)

![assembly_45](./tutorial_images/assemble_art_installation/assembly_45.jpg)

A cable channel was attached to the wall between the button box and the control box using double-coated adhesive tape, fitting the button cables and the One Connect cable. Before it was painted, the cable channel was manually sanded to make a better grip for the color. A primer was then added, followed by two layers of wall paint.

![assembly_60](./tutorial_images/assemble_art_installation/assembly_60.jpg)

![assembly_61](./tutorial_images/assemble_art_installation/assembly_61.jpg)

![assembly_62](./tutorial_images/assemble_art_installation/assembly_62.jpg)

![assembly_63](./tutorial_images/assemble_art_installation/assembly_63.jpg)

![assembly_64](./tutorial_images/assemble_art_installation/assembly_64.jpg)

![assembly_65](./tutorial_images/assemble_art_installation/assembly_65.jpg)

### PIR sensor

Three cables of equal length were measured and cut out (I would've preferred 
to have three different colors, but I only had black and red cable).

![assembly_46](./tutorial_images/assemble_art_installation/assembly_46.jpg)

Three female/female jumping wires were then cut in the middle and soldered 
to the three cables, one set of jumping wires for each cable. To compensate for the bad coloring of the main cables, three different colors were chosen for the 
jumping wires.

Multiple larger shrinking tubes were used to keep the three cables together.

![assembly_47](./tutorial_images/assemble_art_installation/assembly_47.jpg)

![assembly_48](./tutorial_images/assemble_art_installation/assembly_48.jpg)

The PIR sensor I used was a SR602. It has three pinouts that were connected to the Nvidia Jetson:

* **\-** to GND (pin 6)
* **\+** to 3.3v (pin 1)
* **out** to a GPIO (pin 7)

![pir_pinout](./tutorial_images/assemble_art_installation/pir_pinout.png)

When the PIR sensor register a person walking by, **out** will be HIGH. When 
there's no detection, **out** will be LOW.

The PIR sensor were then inserted into its slot in the control box lid.

![assembly_59](./tutorial_images/assemble_art_installation/assembly_59.jpg)

![assembly_49](./tutorial_images/assemble_art_installation/assembly_49.jpg)

![assembly_50](./tutorial_images/assemble_art_installation/assembly_50.jpg)

![assembly_51](./tutorial_images/assemble_art_installation/assembly_51.jpg)

![assembly_52](./tutorial_images/assemble_art_installation/assembly_52.jpg)

![assembly_53](./tutorial_images/assemble_art_installation/assembly_53.jpg)

# Final AI art installation
![final_gif_1](./tutorial_images/final_ai_installation/final_gif.gif)

![final_1](./tutorial_images/final_ai_installation/final_1.jpg)

![final_2](./tutorial_images/final_ai_installation/final_2.jpg)

![final_3](./tutorial_images/final_ai_installation/final_3.jpg)

![final_4](./tutorial_images/final_ai_installation/final_4.jpg)

![final_5](./tutorial_images/final_ai_installation/final_5.jpg)

![final_6](./tutorial_images/final_ai_installation/final_6.jpg)

![final_7](./tutorial_images/final_ai_installation/final_7.jpg)

![final_8](./tutorial_images/final_ai_installation/final_8.jpg)
