#!/bin/bash
rm db/db.json
cd scraper
python3 main.py && cd .. && docker stop Rightmove; docker run --rm -d -p 5000:5000 -v $(pwd)/db:/db  --name Rightmove $(docker build -q .)
wait
