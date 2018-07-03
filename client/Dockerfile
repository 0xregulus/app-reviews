FROM nginx:alpine
RUN apk update && \
    apk upgrade && \
    apk add git nodejs && \
    rm -rf /var/cache/apk/* && \
    npm install -g bower grunt-cli && \
    echo '{ "allow_root": true }' > /root/.bowerrc

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html
COPY app/ .
RUN bower install

CMD ["nginx", "-g", "daemon off;"]
