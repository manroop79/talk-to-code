#!/bin/sh -l

for f in ./notebooks/*.ipynb; do jupyter nbconvert --to markdown $f;done