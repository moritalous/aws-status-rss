# aws-status-rss

AWSのService Health Dashboard(https://status.aws.amazon.com/)から、東京リージョンに関係のありそうなRSSをピックアップし、一つのRSSファイルにまとめてS3に格納します。

LambdaとS3、CloudWatch Eventsでできています。

1. Lambdaレイヤーをつくる

```
docker run -v $PWD:/work amazonlinux:2 /bin/bash /work/createlayer.sh
```

2. Lambdaレイヤーをアップロード

3. Lambdaを作成

4. 環境変数をセット

| Key | Value |
| --- | --- |
| S3_BUCKET | RSSファイルを格納するS3バケット |
| S3_KEY | RSSファイルの名称 |