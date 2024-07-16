#!/bin/bash

# Delete contents of Django_back_end/build/
rm -r Django_back_end/build/*

# Copy contents of react_front_end/build/ to Django_back_end/build/
cp -r react_front_end/build/* Django_back_end/build/
cp Django_back_end/build/favicon_custom.ico Django_back_end/build/static/