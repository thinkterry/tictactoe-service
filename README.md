This is a tic-tac-toe game built using Python 3.4.0, Django 1.11.1, and [Django REST framework](http://www.django-rest-framework.org/) 3.6.3.

## To run

1. Clone this project into ~/projects/tictactoe/.
1. Install Python 3.4.0 and the dependencies listed in requirements.txt.
1. Run the server:

    ```bash
    $ python3 ~/projects/tictactoe/manage.py runserver
    ```

    http://localhost:8000/games/1/ should then be available in the browser.

## To use

In this version, there is only one game.

### View the game

http://localhost:8000/games/1/

### Join the game

Join as X:

```bash
$ curl -X POST localhost:8000/games/1/join/x/
{"token":"64dd6c95-3e20-4e04-b320-62792dfe7e0a"}
```

Join as O:

```bash
$ curl -X POST localhost:8000/games/1/join/o/
{"token":"03d22119-192d-4cb2-a48c-7b131d46695d"}
```

### Make a move

Using the token returned from a successful POST to /join/x/ or /join/o/:

```bash
$ curl --header "Authorization: Token 64dd6c95-3e20-4e04-b320-62792dfe7e0a" --data "row=0&col=0" localhost:8000/games/1/
{"board":"[[true, null, null], [null, null, null], [null, null, null]]","current_player":false,"winner":null}
```

```bash
$ curl --header "Authorization: Token 03d22119-192d-4cb2-a48c-7b131d46695d" --data "row=2&col=2" localhost:8000/games/1/
{"board":"[[true, null, null], [null, null, null], [null, null, false]]","current_player":true,"winner":null}
```

The token defines which player is making the move, and players must alternate moves.

## Other operations

### Run the Django unit tests

```bash
$ cd ~/projects/tictactoe
$ python3 manage.py test
```

### Reset the game

Load in the provided Django fixture to the database:

```bash
$ python3 ~/projects/tictactoe/manage.py loaddata ~/projects/tictactoe/api/fixtures/game.json
```
