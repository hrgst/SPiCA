# Japanese (Windows)

オフラインで使えるWikiシステムです。
markdown に対応しています。

## サポート環境

- Windows
- Python 3.10.x

## インストール方法

1. [リリースページ](https://github.com/hrgst/SwiftFlow/releases) に移動します。
2. 最新のリリースの`Source code (zip)`をダウンロードします。
3. zipファイルを展開します。
4. Powershellを起動します。
5. 展開したディレクトリに移動します。（`requirements.txt`があるディレクトリ）
6. `python -m pip install -r requirements.txt` を実行します。  
    （ライブラリのインストール）
7. `python .\src\run.py` を実行する

# ネットワーク設定を変更する

`settings.yaml` を変更してください。

```yaml
network:
    host: ホスト名または、外部に公開する場合は0.0.0.0
    port: ポート番号
    protocol: http （しか対応していません。）
    prefix: URLのoriginの後に付くprefix（任意）
```

# English (Windows)

This is an offline-usable Wiki system.
It supports markdown.

## Supported Environment

- Windows
- Python 3.10.x

## Installation

1. Go to the [release page](https://github.com/hrgst/SwiftFlow/releases).
2. Download the latest release as `Source code (zip)`.
3. Extract the zip file.
4. Launch PowerShell.
5. Navigate to the extracted directory (the one containing `requirements.txt`).
6. Execute `python -m pip install -r requirements.txt`.  
    (Installing required libraries)
7. Run `python .\src\run.py`.

# Changing Network Settings

Modify `settings.yaml`.

```yaml
network:
    host: Hostname or 0.0.0.0 for external publish
    port: Port number
    protocol: http (only supported)
    prefix: Prefix to append after URL origin (optional)
```
