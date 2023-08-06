#!/bin/bash

linkchecker ../build3/html/ \
    --ignore-url ../build3/html/.ipynb_checkpoints/ \
    --ignore-url ../build3/html/_sources/ \
    --ignore-url ../build3/html/cli/.ipynb_checkpoints/
