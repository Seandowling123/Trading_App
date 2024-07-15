#!/bin/bash

# Navigate to the React front end directory
cd /var/Trading_App/react_front_end

# Install dependencies and build the React app
npm install
npm run build

# Copy the build files to the Django back end directory
cp -r build/* /var/Trading_App/Django_back_end/static/