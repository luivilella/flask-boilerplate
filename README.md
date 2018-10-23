# Flask-boilerplate

## Running locally
To setup the local dev env run the commands bellow:

    $ make build
    $ make up

Check the APIs:

    curl -X POST http://localhost:5000/auth/users \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "niceuser",
            "password": "234567890"
        }'

    curl -X GET http://localhost:5000/auth/users \
        -H 'Content-Type: application/json'
