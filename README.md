## APIコール

```
curl -X POST -H "Content-Type: application/json" -d '{"message": "new message"}' http://localhost:5000/send
```
```
curl -X POST -H "Content-Type: application/json" -d '{"message": "new message"}' http://chat:5000/send
```

## raptor.mainからの接続

- docker networkを構築
```
docker network ls
docker network create RaptorLink
```
- 削除する場合
```
docker network rm RaptorLink
```
