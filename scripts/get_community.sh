#!/bin/sh

# GET request that retrieves the N amount of posts for a particular community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/recent?community=CSUFTesting&amount=2"