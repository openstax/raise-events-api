# RAISE Events API

A REST API used to capture events from RAISE.

There is a docker environment that can be used for development:

```bash
$ docker-compose up -d
```

The development container launches `uvicorn` with `--reload` and volume mounts the code directory so file changes should get reflected without any additional steps. The API is accessible on port 8888 and docs available at http://localhost:8888/docs. The environment also has CORS configured to allow requests from `localhost:8000` (the port used for dev Moodle instances).

If you would like to configure secrets that the API uses to verify token signatures, you can configure them via local environment variable and then inject via `docker-compose`:

```bash
$ export AUTH_KEYS='[{"kid":"testid","secret":"testsecret"}]'
$ docker-compose up -d
```

The code can be linted and tested locally as follows:

```bash
$ pip install .[test]
$ flake8
$ pytest
```

Code coverage reports can be generated when running tests:

```bash
$ pytest --cov=eventsapi --cov-report=term --cov-report=html
```
