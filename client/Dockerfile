FROM node:lts
WORKDIR /app
COPY . .
RUN rm -rf node_modules
RUN npm install
CMD ["npm", "run", "generate"]
ENV HOST 0.0.0.0
EXPOSE 80
CMD ["npm", "run", "dev"]