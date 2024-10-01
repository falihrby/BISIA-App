# Build stage
FROM node:18 as build

# Set the working directory inside the container to /app
WORKDIR /app

# Copy only the frontend package.json and package-lock.json first to leverage Docker layer caching
COPY frontend/package*.json ./frontend/

# Install dependencies in the frontend directory
RUN npm --prefix frontend install --omit=dev

# Copy the entire project to the container (after dependencies are cached)
COPY . .

# Build the React app in the frontend directory
RUN npm --prefix frontend run build

# Production stage (if you plan to serve the built files)
FROM node:18 as production

# Set the working directory in the container
WORKDIR /app

# Copy the build files from the build stage to production
COPY --from=build /app/frontend/build /app/frontend/build

# Use npx to serve the application (if you're using 'serve' or any other tool)
CMD ["npx", "serve", "-s", "frontend/build"]

# Expose the port serve will use (optional, if using 'serve')
EXPOSE 5000
