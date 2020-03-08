#!/bin/sh

# POST request while without the optional URL
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Testing1", "text":"text1", "community":"CSUFTesting", "username":"user123"}' \
    http://localhost:5000/api/v1.0/resources/collections


