#!/bin/bash

mkdir -p lambda_layer
mkdir -p lambda_layer/python

rm -r ./lambda_layer/python/*
cp -r ./basketball_stats/*.py* ./lambda_layer/python

pip3 install -r requirements.txt -t ./lambda_layer/python

cd lambda_layer
zip -r lambda_layer_basketball_stats ./python/