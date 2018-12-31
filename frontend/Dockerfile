# Install node
FROM node:10.9.0

# The base node image sets a very verbose log level.
ENV NPM_CONFIG_LOGLEVEL warn

# Install and configure 'serve'
RUN npm install -g serve
CMD serve -s build
EXPOSE 5000

# Install all dependencies
COPY package.json package.json
RUN npm install

# Copy all local files into the image.
COPY . .

# build
RUN npm run build --production
