#!/bin/bash
docker build -t unite_us .
docker run -it --rm --log-opt max-file=2 --log-opt max-size=2k -v $(pwd)/output:/output unite_us