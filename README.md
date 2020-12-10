This guide goes through all the steps to build an AI-art installation, using a 
Nvidia Jetson Xavier NX and a Samsung The Frame 32". It includes pre-designed CAD-files,
how to set up the computer to run an art-kiosk (with code), how to build and 
assemble the control box and button etc.

## Table of content
1. [Build control box](#build-the-control-box)
    1. [Hand-cut parts](#hand-cut-parts)
    2. [Cut cable slots](#cut-cable-slots)
    3. [Cut wood biscuits holes](#cut-wood-biscuits-holes)
    4. [Glue parts together](#glue-parts-together)
    5. [Spackling paste and sanding](#spackling-paste-and-sanding)
    6. [Add hinges](#add-hinges)
    7. [Add magnetic lock](#add-magnetic-lock)
2. [Build button box]()
    1. ...
    2. ...
3. [Set up Nvidia Jetson Xavier NX]()
    1. ...
    2. ...
4. [Assemble art installation]()
    1. ...
    2. ...

## Build the control box
To get a nice looking installation with as few visible cables as possible, a control box 
was built to encapsulate the Nvidia computer, power adapters, Samsung One Connect box etc.

### Hand-cut parts
The control box was build using 12mm (0.472") MDF. MDF is quite simple to work with and
looks good when painted. A disadvantage is that it produces very fine-graned
dust when cut or sanded.

![raw_mdf](./tutorial_images/build_control_box/raw_mdf.jpg)

A vertical panel saw was used to cut down the MDF into smaller pieces. A table saw was 
used to cut out the final pieces.

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

### Cut cable slots
To enable the cables to go in and out of the box, two cable slots were cut out:

1. One cable slot in the top side panel for the One Connect cable and button cables.
2. One cable slot in the bottom side panel for the electrical cable.

A caliper was used to measure the diameter of the cables. An extra ~1mm was then added to the slots for
the cables to fit nicely.

![caliper](./tutorial_images/build_control_box/caliper.jpg)

The slots were then outlined at the center of the panels.

![cable_slot_1](./tutorial_images/build_control_box/cable_slot_1.jpg)

![cable_slot_2](./tutorial_images/build_control_box/cable_slot_2.jpg)

A jigsaw was used to cut out the slots.

![jigsaw_1](./tutorial_images/build_control_box/jigsaw_1.jpg)

![jigsaw_2](./tutorial_images/build_control_box/jigsaw_2.jpg)

A small chisel and a hammer was used to remove the cut out piece.

![chisel_1](./tutorial_images/build_control_box/chisel_1.jpg)

![chisel_2](./tutorial_images/build_control_box/chisel_2.jpg)

![chisel_3](./tutorial_images/build_control_box/chisel_3.jpg)

![cable_slot_3](./tutorial_images/build_control_box/cable_slot_3.jpg)

### Cut wood biscuits holes
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

### Glue parts together
When gluing the parts together, you'll need to be fairly quick and structured. Prepare by placing the 
aligning panels next to each other and have all the wood biscuits ready.

![gluing_1](./tutorial_images/build_control_box/gluing_1.jpg)

![gluing_2](./tutorial_images/build_control_box/gluing_2.jpg)

Start of by adding the glue in the wood biscuit holes.

![gluing_3](./tutorial_images/build_control_box/gluing_3.jpg)

Press down the wood biscuits into the holes and apply wood glue along all the connecting parts.

![gluing_4](./tutorial_images/build_control_box/gluing_4.jpg)

Now, assemble all the connecting parts together and apply force using clamps. You should see
glue seeping out between the panels.

![gluing_5](./tutorial_images/build_control_box/gluing_5.jpg)

Use an engineer's square to check that you have 90 degrees in each corner of the box.

![gluing_6](./tutorial_images/build_control_box/gluing_6.jpg)

Finally, remove all the visible redundant glue with a wet paper tissue.

![gluing_7](./tutorial_images/build_control_box/gluing_7.jpg)

![gluing_8](./tutorial_images/build_control_box/gluing_8.jpg)

### Spackling paste and sanding
After removing the clamps, there were some visible gaps and cracks that needed to be filled.

![spackling_1](./tutorial_images/build_control_box/spackling_1.jpg)

![spackling_2](./tutorial_images/build_control_box/spackling_2.jpg)

![spackling_3](./tutorial_images/build_control_box/spackling_3.jpg)

I used plastic padding (a two component plastic spackling paste) to cover up the gaps and cracks.

![spackling_4](./tutorial_images/build_control_box/spackling_4.jpg)

Be careful with how much hardener you add, as it will dry very quickly if adding to much.

![spackling_5](./tutorial_images/build_control_box/spackling_5.jpg)

![spackling_6](./tutorial_images/build_control_box/spackling_6.jpg)

![spackling_7](./tutorial_images/build_control_box/spackling_7.jpg)

When everything had dried, an electric sander was used to remove redundant plastic padding.
The inside of the box was smoothed by manual sanding. As a rule of thumb, if you can
feel an edge or a crack, it will be visible when you paint it.

![spackling_8](./tutorial_images/build_control_box/spackling_8.jpg)

![spackling_9](./tutorial_images/build_control_box/spackling_9.jpg)

### Add hinges
The hinges were first added to the lid. It made it easier to align the lid on the box 
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
place. If you don't do this, there's a risk that the material will crack.

![hinge_7](./tutorial_images/build_control_box/hinge_7.jpg)

![hinge_8](./tutorial_images/build_control_box/hinge_8.jpg)

The depth of the screws were measured and adhesive tape was used to mark the depth
on the drill head. 

![hinge_9](./tutorial_images/build_control_box/hinge_9.jpg)

![hinge_10](./tutorial_images/build_control_box/hinge_10.jpg)

![hinge_11](./tutorial_images/build_control_box/hinge_11.jpg)

Before aligning the hinges on the box, make sure to add some support under the lid,
it should be able to rest at the same level as the box. Double-coated adhesive tape 
was then attached to each hinge and the lid was aligned on top of the box. When the 
lid was correctly aligned, I applied pressure to make the adhesive tape stick.

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

### Add magnetic lock
A standard magnetic lock was used to keep the lid in place.

![magnetic_lock_1](./tutorial_images/build_control_box/magnetic_lock_1.jpg)

![magnetic_lock_2](./tutorial_images/build_control_box/magnetic_lock_2.jpg)

![magnetic_lock_3](./tutorial_images/build_control_box/magnetic_lock_3.jpg)

![magnetic_lock_4](./tutorial_images/build_control_box/magnetic_lock_4.jpg)

![magnetic_lock_5](./tutorial_images/build_control_box/magnetic_lock_5.jpg)

![magnetic_lock_6](./tutorial_images/build_control_box/magnetic_lock_6.jpg)

![magnetic_lock_7](./tutorial_images/build_control_box/magnetic_lock_7.jpg)

![magnetic_lock_8](./tutorial_images/build_control_box/magnetic_lock_8.jpg)

![magnetic_lock_9](./tutorial_images/build_control_box/magnetic_lock_9.jpg)

### Milling edges
To give a nice finish, all the edges were milled.

![milling_1](./tutorial_images/build_control_box/milling_1.jpg)

![milling_2](./tutorial_images/build_control_box/milling_2.jpg)

![milling_3](./tutorial_images/build_control_box/milling_3.jpg)

## Set up Nvidia Jetson Xavier NX

### Clone repository
```bash
git clone https://github.com/maxvfischer/Arthur.git
```

### Set up virtual environemnt
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

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Set up user permission
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

### Add AI-model checkpoint
Copy the model checkpoint into `arthur/ml/checkpoint`:

    ├── arthur
         ├── ml
             ├── StyleGAN.model-XXXXXXX.data-00000-of-00001
             ├── StyleGAN.model-XXXXXXX.index
             └── StyleGAN.model-XXXXXXX.meta

### Add initial active artwork
Add an initial active artwork image by copying an image here: `arthur/active_artwork.jpg`

### Adjust config.yaml
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
