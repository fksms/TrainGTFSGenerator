## 利用方法

### MacOS

pipxのインストール
```sh
brew install pipx
```

Poetryのインストール
```sh
pipx install poetry
```

Poetryのパッケージインストール先をプロジェクトのルートフォルダに変更
```sh
poetry config virtualenvs.in-project true
```

必要なパッケージをインストール
```sh
poetry install
```

実行
```sh
poetry run python src/main.py
```