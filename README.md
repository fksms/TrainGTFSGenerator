## 利用方法

### MacOS

#### 事前準備

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

#### スクリプトの実行

このリポジトリをクローン
Submoduleを追加しているので`--recursive --shallow-submodules`を指定
```sh
git clone --recursive --shallow-submodules https://github.com/fksms/TrainGTFSGenerator.git
```

ディレクトリを移動
```sh
cd TrainGTFSGenerator
```

必要なパッケージをインストール
```sh
poetry install
```

実行
```sh
poetry run python src/main.py
```