## Backlog Merge Request

### インストール

#### 設定ファイルの編集
    $ cp config/config.json.sample config/config.json
    $ vi config/config.json

#### cron設定
毎分 batch.pyが動くように設定してください。

#### サーバ起動
    ./server.py

http://localhost:8080/

にアクセス。merge request作成画面が表示されます。

----
### merge request の動作フロー  
1. merge requestを作成する  
http://localhost:8080/  
に必要情報を入力し、submit  
対象のプロジェクトにMerge Reqyest... という課題が作成される。  

2. batch.pyが新しいマージリクエストを認識。  
あたらにcloneしマージ対象ブランチとの差分をbacklogにコメントする。  

3. マージOKになるまで、通常の課題としてやり取り。  
   登録してあるブランチにコミットがあった場合、自動的にdiffがコメントされる。  

4. マージする。（ここは手動）  
   課題を完了にする。=> batch.pyが課題の完了を検知し、監視対象外にする  




