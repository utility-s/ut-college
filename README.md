<<<<<<< HEAD
# UT福祉カレッジ LPサイト

株式会社UTILITY（UT福祉カレッジ）の「東京都強度行動障害支援者養成研修（基礎研修／実践研修）」LPサイトのソースコードです。
GitHub Pagesを利用してホスティングされています。

## GitHub Pagesでの公開手順

1. 本リポジトリの `Settings` > `Pages` を開きます。
2. `Build and deployment` の `Source` を `Deploy from a branch` に設定します。
3. `Branch` を `main` と `/ (root)` に設定し、`Save` をクリックします。
4. 数分待つと `https://utility-s.github.io/ut-college/` でサイトが公開されます。

## 内容の更新方法

`index.html` を直接編集することで内容を更新できます。以下の箇所は定期的な更新が想定されます。

### 次回開催日程の更新
`index.html` 内の `<!-- 次回開催日程（更新箇所） -->` というコメントを目印に、日程や募集状況を書き換えてください。

### 募集要項・フォームURLの更新
申込フォーム（Googleフォーム等）のURLが決定した場合、`index.html` の `href="#"` となっている箇所（`<!-- TODO: 外部フォームURL -->`）を新しいURLに書き換えてください。

## SEO・Google Search Console登録手順

1. [Google Search Console](https://search.google.com/search-console/about) にアクセスし、ログインします。
2. 「プロパティの追加」から「URLプレフィックス」を選択し、`https://utility-s.github.io/ut-college/` を入力して続行します。
3. 確認方法として「HTMLタグ」を選択し、表示された `<meta name="google-site-verification" content="..." />` をコピーします。
4. `index.html` の `<head>` 内にある `<!-- TODO: Google Search Console verification -->` の部分を上記メタタグに置き換え、コミット・プッシュします。
5. Search Consoleに戻り、「確認」ボタンを押して所有権を確認します。
6. 左側メニューの「サイトマップ」を開き、`sitemap.xml` と入力して送信します。

## 画像・ロゴの差し替え方法

本リポジトリの `images/` フォルダ内にある画像を同名で上書き保存し、コミット・プッシュしてください。

- `images/logo.png`: ヘッダーやフッターで表示されるロゴ画像
- `images/ogp.png`: SNS等でシェアされた際に表示される画像（推奨サイズ: 1200x630px）
- `favicon-96x96.png`: ブラウザのタブに表示されるアイコン（推奨サイズ: 96x96pxの正方形、Uマーク等）
- `apple-touch-icon.png`: スマホのホーム画面に追加した際のアイコン（推奨サイズ: 180x180pxの正方形）

※ファビコン等はルートディレクトリに配置されています。

## 独自ドメインへの移行 (将来)

独自ドメインを取得し移行する場合は、以下の手順を行います。

1. DNSプロバイダー側で、取得したドメインの `CNAME` レコードを `utility-s.github.io` に向けるよう設定します。
2. 本リポジトリの `Settings` > `Pages` にある `Custom domain` 欄に取得したドメインを入力し、`Save` します。
3. 念のため `Enforce HTTPS` にチェックが入っていることを確認します。
4. `sitemap.xml` と `robots.txt`、各種メタタグ・OGP・JSON-LD内のURL (`https://utility-s.github.io/ut-college/`) を新しいドメインに一括置換します。
=======
# ut-college
>>>>>>> 3b614fddf0026d1f70eb6f2cb2585f6d4643e847
