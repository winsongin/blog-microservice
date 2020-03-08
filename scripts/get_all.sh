#!/bin/sh

# GET request that retrieves the N amount of posts from any community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/all?amount=2"