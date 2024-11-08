FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY app.html /usr/share/nginx/html
EXPOSE 80
RUN apk add apache2-utils
RUN htpasswd -cb  /etc/nginx/.htpasswd user  123456
CMD ["nginx", "-g", "daemon off;"]