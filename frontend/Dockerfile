FROM node:18.7.0

WORKDIR /app

EXPOSE 3000

COPY package.json package-lock.json ./

RUN npm install --silent
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

CMD ["npm","start"]
