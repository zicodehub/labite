# pull official base image
FROM node:alpine3.14

# set working direction
WORKDIR /app
# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
# install application dependencies
COPY package.json ./
COPY package-lock.json ./
COPY . ./
RUN npm i -timeout=9999999
# start app
# CMD ["npm", "start"]