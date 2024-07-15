#!/bin/bash

# Navigate to the React front end directory
cd react_front_end || exit

# Build the React app
npm run build

# Copy the build files to the Django static directory
cp -r build/* ../Django_back_end/static/