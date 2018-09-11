You will need to create a startup script to boot pgiod 
```
sudo apt-get install pigpio
sudo cp pigpiod.service /lib/systemd/system/pigpiod.service
sudo systemctl daemon-reload
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```
