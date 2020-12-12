# birthday-cat
### 誕生日おめでとうにゃ！！！
あなたがログインしているDiscordに優しさを追加してみませんか？

Discordで動く誕生日Botです。`app/data/birthday.json`に登録した誕生日にお祝いしてくれます。
誕生日だけでなく、欲しいものリストを登録することができるので仲間同士でお祝いしあいましょう。

きっと素敵な時間が訪れます。

環境を合わせるためDockerにて運用してください。

### Quick Start
1.`Docker`, `Docker-Compose`をインストールしてください。
    **Docker**
    https://docs.docker.jp/compose/install.html
    **Docker-Compose**
    https://docs.docker.jp/engine/installation/index.html

2.git cloneしてください。    

```
$ git clone https://github.com/nodokamome/birthday-cat.git
```

3.環境変数を設定し、ビルドしてください。
`app/src/.env.sample`を参考に同じディレクトリに`.env`を作成し、Discordの設定を追加してください。

**Docker Build**
```
$ cd birthday-cat
$ docker-compose up --build -d
```

### あなたのDiscordに幸せが訪れます。
`Botにコマンド`がいくつかありますので、`$help`で呼び出してみてください。
