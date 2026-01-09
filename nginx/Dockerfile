FROM node:18-alpine AS frontend_builder

WORKDIR /app
COPY frontend/package*.json /app/
RUN npm ci
COPY frontend /app

ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

FROM nginx:1.25-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend_builder /app/dist /usr/share/nginx/html
