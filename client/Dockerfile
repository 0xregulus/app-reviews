FROM nginx:alpine
RUN apk update && \
    apk upgrade && \
    apk add git nodejs && \
    rm -rf /var/cache/apk/* && \
    npm install -g bower grunt-cli && \
    echo '{ "allow_root": true }' > /root/.bowerrc

COPY /client/nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html
COPY /client/app/ .
RUN bower install
