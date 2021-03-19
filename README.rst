Linedrive
====================
A Python client script to interact with ESPN's Gamecast service, allowing you to follow along at the command line.

Modes of Execution
-----------------------
Linedrive supports two things:

- Following real-time game play events
- Checking league schedules for the purpose of following a specific game

To engage with this functionality, use the ``schedule`` and ``events`` command line arguments, which specify which 'mode' you would like to run the script in:

**schedule**: schedule mode queries ESPN's scoreboard interface to obtain the latest schedule for the provided sports league.

**events**: events mode accepts a league and team name, and provides real-time game play events.

Supported Leagues
-----------------------
In order to check schedules or to follow game play events, you need to know which leagues are supported. The following leagues are supported at the time of this writing:

* WNBA
* NBA
* NCAAW
* NCAAM
* NHL
* NFL

This information is also provided in the ``--help`` menu:

::

    poorbillionaire@computer:~$ python ./linedrive.py -h
    usage: linedrive.py [-h] -l {wnba,nba,ncaaw,ncaam,nfl,nhl} [-t TEAM] {events,schedule}

    positional arguments:
      {events,schedule}

    optional arguments:
      -h, --help            show this help message and exit
      -l {wnba,nba,ncaaw,ncaam,nfl,nhl}, --league {wnba,nba,ncaaw,ncaam,nfl,nhl}
      -t TEAM, --team TEAM  Team name

Selecting a Team
-----------------------
I have not compiled a list of "supported teams" to choose from. I recommend that users of the script who want to follow along with game play events specify a team name without including the city name. More complete usage examples are provided below; however some examples of team names are:

* grizzlies
* clippers
* cowboys
* jackrabbits
* yellow jackets

Usage Examples
-----------------------
**Schedule Mode**

::

    python ./linedrive.py schedule -l ncaam


    2021-03-19T16:15Z | STATUS_IN_PROGRESS | Virginia Tech Hokies at Florida Gators
    2021-03-19T16:45Z | STATUS_HALFTIME    | Colgate Raiders at Arkansas Razorbacks
    2021-03-19T17:15Z | STATUS_IN_PROGRESS | Drexel Dragons at Illinois Fighting Illini
    2021-03-19T17:45Z | STATUS_IN_PROGRESS | Utah State Aggies at Texas Tech Red Raiders
    2021-03-19T19:00Z | STATUS_SCHEDULED   | Oral Roberts Golden Eagles at Ohio State Buckeyes
    2021-03-19T19:30Z | STATUS_SCHEDULED   | Hartford Hawks at Baylor Bears
    2021-03-19T20:00Z | STATUS_SCHEDULED   | Georgia Tech Yellow Jackets at Loyola Chicago Ramblers

**Events Mode**

Continuing the example above, let's say we want to follow along with the Hokies/Gators game showing a status of ``STATUS_IN_PROGRESS``. 

::

    python ./linedrive.py events -l ncaam -t gators
        __    _____   ____________  ____  _____    ________
       / /   /  _/ | / / ____/ __ \/ __ \/  _/ |  / / ____/
      / /    / //  |/ / __/ / / / / /_/ // / | | / / __/   
     / /____/ // /|  / /___/ /_/ / _, _// /  | |/ / /___   
    /_____/___/_/ |_/_____/_____/_/ |_/___/  |___/_____/   

    Gators: 44  | Hokies: 46  | Period 2 9:51  | Foul on Cordell Pemsl.
    Gators: 44  | Hokies: 46  | Period 2 9:51  | Colin Castleton missed Free Throw.
    Gators: 44  | Hokies: 46  | Period 2 9:51  | Tyrece Radford Defensive Rebound.
    Gators: 44  | Hokies: 46  | Period 2 9:34  | Foul on Anthony Duruji.
    Gators: 44  | Hokies: 47  | Period 2 9:34  | Nahiem Alleyne made Free Throw.
    Gators: 44  | Hokies: 48  | Period 2 9:34  | Nahiem Alleyne made Free Throw.
    Gators: 46  | Hokies: 48  | Period 2 9:19  | Colin Castleton made Dunk.
    Gators: 46  | Hokies: 50  | Period 2 9:01  | Tyrece Radford made Jumper.
    Gators: 46  | Hokies: 50  | Period 2 8:28  | Florida  Turnover.
    Gators: 46  | Hokies: 50  | Period 2 8:00  | Tyrece Radford missed Jumper.
    Gators: 46  | Hokies: 50  | Period 2 8:00  | Osayi Osifo Defensive Rebound.

Installation
--------------
``pip install -r requirements.txt``
