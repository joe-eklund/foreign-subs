# Run

## Database

Inside the `docker` folder, run `docker-compose up -d` to launch MongoDB. Run `docker-compose down` to stop.

## Backend

Create a Python virtual environment with `python -m venv venv` and `source venv/bin/activate`.

`cd` into the `backend` directory and run `pip install -r requirements.txt` to install dependencies.

Run `fsubs`. Add `--help` for additional options.

## Frontend

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 8.1.1.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).

### Configuration

The `--config/-c` option lets you use a custom config file. It should be in [`ini`](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure) format.
