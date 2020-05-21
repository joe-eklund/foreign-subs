# Welcome

This is the repository for https://foreignsubs.com. It is currently a work in progress.

In short, the purpose of ForeignSubs is to document when a movie or tv show has foreign subtitles.

Foreign subtitles are defined as subtitles that exist to display information either not spoken but is relevant (e.g. `3 months later`) or language spoken that is not in the main language of the media. So if the main language of the movie is in English, but there are some lines in Italian, the spoken Italian lines would be considered foreign subs.

# How to Run

## Technologies

ForeignSubs is built in three parts: A frontend built in [TypeScript](https://www.typescriptlang.org/) using [Angular](https://angular.io/), a RESTful API built in [Python3](https://www.python.org/) using [FastAPI](https://fastapi.tiangolo.com/), and [MongoDB](https://www.mongodb.com/) as the database.

## Database

Inside the `docker` folder, run `docker-compose up -d` to launch MongoDB. Run `docker-compose down` to stop.

- Make sure to update the database username and password if you are using this in production.

## Backend

Create a Python virtual environment with `python -m venv venv` and `source venv/bin/activate`.

`cd` into the `backend` directory and run `pip install -r requirements.txt` to install dependencies.

Run `fsubs`. Add `--help` for additional options.

### Configuration

The `--config/-c` option lets you use a custom config file. It should be in [`ini`](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure) format.

> **NOTE:**
>
> If you want to reload automatically while developing, you must create a file in `backend/fsubs/config` called `default_reload.ini`. In the section called `[app]` set `reload=True`.
>
> Best practice: copy `default.ini` to `default_reload.ini` and change `reload` from `False` to `True`.

#### Environment Variables

fsubs can be configured using environment variables. They correspond to the command line options as follows:

 Environment Variable | CLI Option | Description
---|---|---
 FSUBS_APP_BIND_ADDRESS | `--bind-address`| Set app bind IP address.
 FSUBS_APP_BIND_PORT | `--bind-port`| Set app bind port.
 FSUBS_APP_LOG_LEVEL | `--log-level`| Set app log level; valid values are `debug,info,warning,error,critical`.
 FSUBS_DB_HOSTNAME | `--db-hostname`| Set the database hostname.
 FSUBS_DB_PASSWORD | `--db-password`| Set the database password.
 FSUBS_DB_PORT | `--db-port`| Set the database port.
 FSUBS_DB_USERNAME | `--db-username`| Set the database username.

#### Configuration Order

Configuration values are read in the following order:

- CLI params
- environment vars
- custom config file
- `default_reload.ini` config
- `default.ini` config

## Frontend

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 8.1.1.

### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.


### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

More information for the frontend can be found in the frontend folder README.

# License

This code is released under the MIT License. See the LICENSE file for details.


# Authors
- Joe Eklund - https://github.com/joe-eklund
- Sam Eklund - https://github.com/samueldeklund
- Sam Maphey - https://github.com/sammaphey 
- Nick Wong -  https://github.com/wongesse

Thanks to all contributors of this repo! If you would like to contribute you can contact the authors or open a Github issue.