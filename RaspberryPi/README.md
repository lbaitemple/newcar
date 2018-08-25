You will need to create a startup script to boot pgiod 
```
sudo cp gpio.service /lib/systemd/system/gpio.service
sudo systemctl daemon-reload
sudo systemctl enable gpio
sudo systemctl start gpio
```
