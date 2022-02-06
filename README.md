# Pipro
Pipro is a submission to U of T Hacks 2022. 
The hackathon's theme is Restoration. For the project, we chose
to focus on restoring broken pipes to deal with the common
and dangerous issue of leaky gas pipes in home or industrial complexes.

The app is a proof-of-concept and does not offer any real solutions.
The idea is that there would be drones linking to a web server which
would fly around and detect gas leaks. Upon detecting, the user's
web dashboard would light up with the location of the leak allowing
for quick repairs, or for evacuation if necessary.

First set up and run the server
```sh
$ project-direcrory> cd server
$ Sim> pip3 install flask
$ Sim> pip3 install flask-session
$ server> flask run
```

Run the frontend
```sh
$ project-direcrory> cd client
$ client> npm install
$ client> npm run dev
```

Run Simulation (Make sure to install Python 3.10)
```sh
$ project-direcrory> cd Sim
$ Sim> pip3 install pygame
$ Sim> pip3 install requests
$ Sim> python3 main.py
```

You can then open the application at the follwoing link in your browser
```
http://localhost:3000/
```

### Simulation Controls:
- Use ASWD to pan the camera
- Use Arrow Keys to move the drone
- Use the Scroll Wheel on your Mouse to Zoom

### Web Dashboard Controls:
- Click on red leak notification pings to remove them
