# SpotMicroAI runtime source code

This repo contains a basic os that let you move SpotMicroAI with a remote controller and a RaspberryPi

If you are looking for simulation, please check the simulation repositories here: https://gitlab.com/custom_robots/spotmicroai

## Start

Enable I2C
```
sudo raspi-config
```

SelfInstall
```
curl https://gitlab.com/custom_robots/spotmicroai/basic-runtime/-/raw/master/install/self_install.sh | bash
```
Manual install
* Copy the install/self_install.sh file to your spot using FileZilla client

Test components individually

```
i2cdetect -y 1

integration_test lcd_screen -> need to ask you for the i2c address, showing you the previous one configured, then will print and generate the config.json section needed


integration_test pca9685 -> need to ask you the i2c address, showing you the previous one configured, then will generate the config.json section, also will ask for the min max ranges of the servos

integration_test pca9685 -> servos -> will iterate over all locations in the board asking for each servo position in the robot, and center position, starts at 90º, then with the user input saves the config file
to identify the servo it will move it from 80º to 100º


integration_test abort_mechanism -> need to ask you which is the gpio port you have connected and will generate the config.json section needed, to test, we need the servos conf done first, power them all at 90º or whatever is the middle point the user told us, then shutdown them, and shut on them

```




Depending of your wiring you must configure in the code some I2C addresses and pins. Also if you are using less sensors you can just remove or comments those parts from the code.

This code is meant to be located in /opt/spotmicro_runtime in your SpotMicro Raspberry Pi board.

For simplicity I use Raspbian Lite in a SanDisk Extreme 32 GB microSDHC Memory Card. This card has the same specifications than the SanDisk Ultra 32GB Class 10 micro SD for big files copy and read, but the Extreme has far more I/O for small files operations.

The software here must be running right after the Raspberry Pi starts, to do so you need to setup it as deamon in linux.

To connect via SSH to your Raspberry PI you must add to Raspbian Lite your wpa_supplicant.conf file with your wifi network, and using raspi-config enable the ssh service.

The first time you connect to your Raspbian Lite your user is "pi" and your password "raspberry", use raspi-config to change it.

This source code project has been created using the instructions here: https://github.com/franferri/my_katas/tree/master/kata-new-python-project

When you try to clone this project and build, in Windows Mac or Linux in x86 architecture, you may encounter than some python dependencies are not available to be build, like the RPi.GPIO. To solve this issue I have purchased a second Raspberry Pi 4 4GB and use the SD card to be the boot partition and an USB3 external SSD drive for the OS, with an external monitor, keyboard and mouse. Developing in that environment with JetBrains PyCharm is very ok.

### Development

Clone this repository using:

    git clone https://gitlab.com/custom_robots/spotmicro/raspberry-pi
    cd raspberry-pi/spotmicropi_runtime

Prepare your python environment and activate it
    
    python3 -m venv venv --clear
    source venv/bin/activate
    
Updating pip this way works always and fix deprecated versions problems
 
    curl https://bootstrap.pypa.io/get-pip.py | python

    pip install --upgrade pip
    pip install --upgrade setuptools
    
Install all requirements to build the project (most likely not work in x86 platform)

    pip install -r requirements.txt

### Build and run

#### Run the project tests from the console

Run all tests in the project

    python3 -m unittest discover

Specific tests in a file

    python3 -m unittest tests/spotmicropi/test_example_main.py

Specific tests in a test class

    python3 -m unittest tests.spotmicropi.test_example_main.SpotMicroTestCase

Specific unit test

    python3 -m unittest tests.spotmicropi.test_example_main.SpotMicroTestCase.test_barks_in_spanish

#### Run the project tests from PyCharm

* Open the project in Pycharm
* Right click on the tests folders
* Run 'Unittests in tests' (**will fail**)
* Edit run configurations -> Working directory -> Remove the ending "/tests"
* Right click on the tests folders again
* Run 'Unittests in tests' (**will succeed**)

#### Run the example project to know you are all set

    python3 raspberry-pi/spotmicropi_runtime/example_main.py

Output

    Ladrar: guau-guau
    樹皮: wan-wan
    Bellen: wuff-wuff
    To bark: woof-woof

#### Run the project

    python3 raspberry-pi/spotmicropi_runtime/main.py
    
To stop the project use Control+C combination, since is meant to be a service/daemon it will hold the console till you press Control+C to terminate it.

### Modifying the project

How to add a dependency to your project

    source venv/bin/activate
    pip install --upgrade pip
    
    pip install <dependency_name>
    
    pip show <dependency_name>
    pip list
    
    pip freeze > requirements.txt







#### TODO



Runtime tiene q tener

    Para traer el sistema operativo usamos git, el usuario tiene q hacer un git clone, a partir de ahí todo es con git pull --force o similar para las actualizaciones

    Script de creación y activación de python, que hace el venv, isntalla los requirements.txt etc

    spotmicroai.service para q arranque con el sistema
    script para hacerlo auto arrancable o para quitarlo de autoarrancable

    Los scripts de test de pantalla y servos (integration tests)

    El (proceso) script de calibration (calibration)
    que debería devolver los datos necesarios para el fichero ~/.spotmicroai.cfg
    incluyendo las direcciones i2c
    posiciones iniciales y finales de los servos.

    El os en sí
        al arrancar tiene q auto actualizarse, si no hay wifi cuando arranca i esto falla es un problema, deberíamos decirle al servicio q no arranque hasta q tenga wifi? o hay gente q no lo tendrá enganchado al wifi (o lo han sacado de casa)... 
        Hacemos que el actualizarse sea opcional, una pregunta al usuario en la pantalla con un icono, que él ejecuta. Actualizar tira del repo principal, no de la rama de development
        al actualizar hay que actualizar el systemd y reiniciarlo.

    configuración base limpia? <- no, este es un fichero en ~/.spotmicroai.cfg que si no existe se genera en la primera ejecución del os. Pero no está en el repositorio