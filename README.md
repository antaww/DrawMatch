# DrawMatch 

A multiplayer web game where players have to draw words displayed in real time for "Pen", an AI based on TensorFlow, to guess.

## Features

- Game rooms that welcome 2 players
- 7 words randomly selected from a pool of 345 words to draw per game   
- Simple drawing interface with a few tools     
- 1 point per word guessed correctly by the AI, points tallied at the end of the game
- Leaderboard of top scoring players   
- Integrated AI for recognizing drawings based on TensorFlow

## Technologies

This project uses the following technologies:

- Python 3.10 for the backend
- HTML, CSS and JavaScript for the frontend  
- Django web framework 
- Websockets with Django Channels for real-time gameplay     
- TensorFlow for the AI model  
- SQLite database to store game data
- Numpy for numeric processing 
- Pillow for image manipulation
- Scikit-image for computer vision operations
- ASGI protocol for Channels
- p5 for graphic and interactive experiences

## Setup

Full setup instructions for running the game locally:

1. Install `Python 3.10` & `Virtualenv`  
2. Create a Virtualenv `virtualenv -p python3 env` 
3. Activate the virtualenv `source env/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Apply database migrations `python manage.py migrate` _(SQLite, locally generated)_
6. Add your IPV4 address in `settings.py` > `ALLOWED_HOSTS`
7. Replace the IP address in `main.py` with your IPV4 address
8. Launch `main.py` to run the development server     

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE)
