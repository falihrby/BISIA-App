# Use Node.js 18 as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY frontend/package*.json ./frontend/

# Install production dependencies only
RUN npm --prefix frontend install --omit=dev

# Copy the remaining app files
COPY . .

# Build the React frontend
RUN npm --prefix frontend run build

# Use serve or any other static file server to serve the build
RUN npm install -g serve

# Expose the port
EXPOSE 5000

# Serve the built app
CMD ["serve", "-s", "frontend/build"]
