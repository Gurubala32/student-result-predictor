#!/bin/bash
set -e
cd /opt/student-result-predictor
docker build -t student-result-predictor:latest .
docker rm -f student-result-predictor 2>/dev/null || true
docker run -d \
  --name student-result-predictor \
  --restart unless-stopped \
  -p 80:5000 \
  student-result-predictor:latest
