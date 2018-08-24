You will need to create a startup script to boot pgiod 
```
sudo cp ipaddress.service /lib/systemd/system/gpio.service
sudo systemctl daemon-reload
sudo systemctl enable gpio
```
