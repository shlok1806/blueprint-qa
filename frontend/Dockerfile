FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./
RUN npm install --production

ENV NODE_ENV=production
ENV PORT=5173
ENV API_URL=http://backend:8000

EXPOSE 5173

CMD ["node", "build"]
