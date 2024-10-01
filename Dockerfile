# Step 1: Build the React app using Node.js
FROM node:18 AS build

# Set working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json to the container
COPY frontend/package*.json ./frontend/

# Copy the rest of the app files into the container
COPY ./frontend ./frontend

# Install all dependencies including devDependencies
RUN npm --prefix frontend install

# Build the React app for production
RUN npm --prefix frontend run build

# Step 2: Use nginx to serve the built app
FROM nginx:alpine

# Copy the built React files from the previous stage to nginx's html directory
COPY --from=build /app/frontend/build /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
