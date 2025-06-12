# シラヤマ作業管理アプリ プロジェクト概要
Copylight T.Saito

**Ver 4-1**
## 今バージョンの特徴(修正点)

- 作業伝票
    - 作業コードの名称を記載
    - 入力のリスト選択(更新されない)
    - 個人伝票表示のところを個人のみ表示できるようにする
    - 全体伝票を最新順に表示する
    - 全体の作業伝票を集計者・管理者側で修正、削除できるようにする
    - 全体の作業伝票にフィルタ機能を実装
- 一般社員の指示表入力・集計を可能にする
- ドキュメントのリンク添付

# インストーリングスクリプト
ユーザのhomeディレクトリ上に作成(chmod 775 で変更して実行)
```sh
#!/bin/bash
#initialize.sh
# Installing ushiku_apps
if [ ! -d "ushiku_apps" ]; then
    echo "! Installing ushiku_apps "
    git clone -b branchname ~URL~
fi

read -p prompt "initializing >"
if [ $prompt = "S" ] or [ $prompt = "s" ]; then
    echo "! moving noapps and initializing ushiku command"
    mv ~/clones/ushiku_apps/other_noapp ~/
    mv ~/other_noapp/bash/setup.sh ~/
    mv ~/other_noapp/bash/guide_setup.txt ~/
    chmod 775 ~/setup.sh
    set alias ushiku = '~/setup.sh'
    source ~/.bashrc

elif [ $prompt = "V" ] or [ $prompt = "v" ]; then
    echo "! Ver1 Ushiku Initializing"
else
    echo "! Closed."
    exit 0
```