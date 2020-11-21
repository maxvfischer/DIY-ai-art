# Arthur
Run Arthur Kiosk on a Nvidia Jetson NX.

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
