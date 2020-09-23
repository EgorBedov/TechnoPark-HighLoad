FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /etc/nginx
COPY  http-test-suite/httptest /etc/nginx/static/httptest

EXPOSE 8081
