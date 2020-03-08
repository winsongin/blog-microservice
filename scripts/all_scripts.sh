#!/bin/sh

# POST request while without the optional URL
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Testing1", "text":"text1", "community":"CSUFTesting", "username":"user123"}' \
    http://localhost:5000/api/v1.0/resources/collections

# POST request with the optional URL included
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Testing2", "text":"text2", "community":"CSUFTesting", "url":"http://fullerton.edu", "username":"user456"}' \
    http://localhost:5000/api/v1.0/resources/collections

# GET request that retrieves an existing post
curl --request GET "http://localhost:5000/api/v1.0/resources/collections?rowID=1"

# GET request that retrieves the N amount of posts for a particular community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/recent?community=CSUFTesting&amount=1"

# GET request that retrieves the N amount of posts from any community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/all?amount=2"

# DELETE request that deletes the row with rowID=1
curl --request DELETE "http://localhost:5000/api/v1.0/resources/collections?rowID=1"