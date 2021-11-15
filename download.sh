#!/usr/bin/env bash

cd ./assets
echo "Download Videos"
scp -r -P43 backendS3@nathanm.fr:videos .
echo "Download Pictures"
scp -r -P43 backendS3@nathanm.fr:pictures .
echo "File Downloaded"