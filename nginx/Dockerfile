FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /etc/nginx
COPY  ./httptest /etc/nginx/static/httptest

EXPOSE 8080
