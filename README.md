# Run

## Database

Inside the `docker` folder, run `docker-compose up -d` to launch MongoDB. Run `docker-compose down` to stop.

## Backend

Create a Python virtual environment with `python -m venv venv` and `source venv/bin/activate`.

`cd` into the `backend` directory and run `pip install -r requirements.txt` to install dependencies.

Run `fsubs`. Add `--help` for additional options.

### Configuration

The `--config/-c` option lets you use a custom config file. It should be in [`ini`](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure) format.
