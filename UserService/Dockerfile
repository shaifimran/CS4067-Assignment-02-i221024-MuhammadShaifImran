FROM node:23-alpine3.20
WORKDIR /UserService
COPY . .
RUN npm ci --omit=dev
EXPOSE 3000
CMD ["node", "user_service.js"]