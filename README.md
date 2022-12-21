# What is this?

This is the backend server code for my NPdataCollection tool. It is written in python and connects to a website frontend that will be written in java where the user will input api_key, game number, and what data they want to be collected.

# How do I use it?

Fortunately you don't have to use this repo! If you would like to start submitting data to the database all you have to do is go to the [website] (that I haven't made yet) and register whatever games you want to submit. If you would like to set up your own server though all you have to do is clone the repo into your prefered python environment. Run init.py, and then set up a timed task (Ex: [cron](https://www.howtogeek.com/devops/what-is-a-cron-job-and-how-do-you-use-them/)) to run main.py at least every hour and recomended every 10 minutes.

# How does it work?

There are 3 main files. Main.py, which makes calls to the database class; database_class.py, which stores the database class that manages the player classes from player_class.py; and player_class.py, which takes an api_key and a game_number as input to create a class to manage each in game player.
