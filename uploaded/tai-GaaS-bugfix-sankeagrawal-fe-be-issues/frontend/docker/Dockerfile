# Specify node version
FROM node:20.11.0 as builder

# Specify working directory
WORKDIR /frontend

COPY package.json .

# Install the npm packages
RUN npm install

COPY . .

RUN npm run build

# Serve the react frontend with nginx
FROM nginx
EXPOSE 80
COPY --from=builder /frontend/build /usr/share/nginx/html
