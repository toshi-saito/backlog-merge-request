## Backlog Merge Request

### インストール

#### 設定ファイルの編集
    $ cp config/config.json.sample config/config.json
    $ vi config/config.json

#### cron設定
毎分 batch.pyが動くように設定してください。

#### サーバ起動
    ./server.py

http://localhost:8080/new

にアクセス。merge request作成画面が表示されます。
