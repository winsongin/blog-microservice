#!/bin/sh

# POST request with the optional URL included
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Testing2", "text":"text2", "community":"CSUFTesting", "url":"http://fullerton.edu", "username":"user456"}' \
    http://localhost:5000/api/v1.0/resources/collections