#!/bin/sh

# DELETE request that deletes the row with rowID=1
curl --request DELETE "http://localhost:5000/api/v1.0/resources/collections?rowID=1"