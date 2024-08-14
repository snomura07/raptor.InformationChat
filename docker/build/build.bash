#!/bin/bash

YML_NAME=build

# スクリプトを実行するディレクトリに移動
cd "$(dirname "$0")"

# no-cacheオプションを初期化
NO_CACHE_OPTION=""

# スクリプトに渡された引数をチェック
if [ "$1" == "--no-cache" ]; then
    NO_CACHE_OPTION="--no-cache"
fi

# Docker Composeを使用してビルドおよび起動
docker compose -f $YML_NAME.yml build $NO_CACHE_OPTION

# ビルドと起動のステータスを表示
if [ $? -eq 0 ]; then
    echo "Dockerイメージのビルドに成功しました。"
else
    echo "ビルドまたは起動に失敗しました。"
fi

# img名表示
IMAGE_NAME=$(yq e '.services.system.image' $YML_NAME.yml)
if [ $? -eq 0 ]; then
    echo "Dockerイメージ名: $IMAGE_NAME"
else
    echo "イメージ名の抽出に失敗しました。"
fi
