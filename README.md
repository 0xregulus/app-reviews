## Test users
- user/user123
- admin/admin123


## Stanalone server
`$ docker build -t app-review-server .`

`$ docker run -p 8000:8000 --name app-review-server app-review-server`

## Stanalone client
`$ docker build -t app-review-client .`

`$ docker run -p 80:80 --name app-review-client app-review-client`

## WIP
docker-compose
