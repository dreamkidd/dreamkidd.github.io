+++
title = "利用 emacs + hugo 搭建个人博客"
author = ["Kidddddddd"]
lastmod = 2024-02-19T11:13:39+08:00
tags = ["emacs", "hugo"]
categories = ["technolgic"]
draft = false
+++

## 基础环境准备 {#基础环境准备}

基本依赖环境是 \`emacs\` \`hugo\` \`git\`


### macos 下 hugo 的安装 {#macos-下-hugo-的安装}

```bash
brew install hugo
```

hugo 是基于 `go` 编写的，但是如果是非源码格式安装，应该不需要安装 `go` 依赖

安装完成以后，使用 `hugo version` 检查


### hugo Quick Start {#hugo-quick-start}

首先利用 hugo 创建一个站点, 这个命令默认创建的位置是当前命令执行的所在目录下的

```bash
hugo new site my-blog
cd my-blog
git init
```

默认的 site 的目录结构如下

<style>.org-center { margin-left: auto; margin-right: auto; text-align: center; }</style>

<div class="org-center">

├── archetypes
│   └── default.md
├── assets
├── content
├── data
├── hugo.toml
├── i18n
├── layouts
├── static
└── themes

</div>

安装一个基本的 theme

```bash
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml"
```

<style>.org-center { margin-left: auto; margin-right: auto; text-align: center; }</style>

<div class="org-center">

hugo server
Watching for changes in /Users/zhangyang/github/my-blog/{archetypes,assets,content,data,i18n,layouts,static,themes}
Watching for config changes in /Users/zhangyang/github/my-blog/hugo.toml, /Users/zhangyang/github/my-blog/themes/ananke/config.yaml
Start building sites …
hugo v0.122.0-b9a03bd59d5f71a529acb3e33f995e0ef332b3aa+extended darwin/arm64 BuildDate=2024-01-26T15:54:24Z VendorInfo=brew

|    |
|----|
| EN |

-------------------+-----
  Pages            |  7
  Paginator pages  |  0
  Non-page files   |  0
  Static files     |  1
  Processed images |  0
  Aliases          |  0
  Sitemaps         |  1
  Cleaned          |  0

Built in 33 ms
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at <http://localhost:1313/> (bind address 127.0.0.1)
Press Ctrl+C to stop

</div>

`hugo` 的基本环境搭建完成，访问 `http://localhost:1313` 查看一下效果

`hugo` 的基本环境已经完成，配置以及主题等优化后续在看看怎么处理


## `emacs` + `ox-hugo` {#emacs-plus-ox-hugo}

我的 emacs 用的是 `doom emacs` 进行的配置， `scp f f` 编辑 `init.el` , 在 org 的配置中，启用 `+hugo` 标识

```elisp
(org +hugo)
```

执行

```bash
doom sync
```

即可安装


### 关键属性 {#关键属性}

`ox-hugo` 在 org-mode 中的关键属性有两个

`HUGO_BASE_DIR` 以及 `HUGO_SECTION`

HUGO_BASE_DIR 用来指定生成的 md 文件的 base_dir

在 org 文件的头部设定好 `HUGO_BASE_DIR`

执行 `M-x org-hugo-exoirt-to-md` 即可导出 org 文件到指定的 hugo 目录下


## `ox-hugo` 工作流 {#ox-hugo-工作流}

ox-hugo 有支持以下两种工作流

1.  单 org 文件的工作流（推荐）
    -   通过 org 的 subtree 来导出单独的文章
    -   循环导出整个 subtree
2.  一个 org 文件一篇文章的工作流
    -   这样操作，就没法很好的利用 org 的标签，以及属性继承等特性，可以利用 `TODO` 关键字来标识草稿状态

<!--listend-->

```elisp
;; ox-hugo configuration
(with-eval-after-load 'org-capture
  (defun org-hugo-new-subtree-post-capture-template ()
        "Returns `org-capture' template string for new Hugo post
        See `org-capture-templates' for more information."
         (let* ((title (read-from-minibuffer "Post Title: ")) ;Prompt to enter the post title
           (fname (org-hugo-slug title)))
      (mapconcat #'identity
                 `(
                   ,(concat "* TODO " title)
                   ":PROPERTIES:"
                   ,(concat ":EXPORT_FILE_NAME: " fname)
                   ":END:"
                   "%?\n")          ;Place the cursor here finally
                 "\n")))

        (add-to-list 'org-capture-templates
               '("h"                ;`org-capture' binding + h
                 "Hugo post"
                 entry
                 ;; It is assumed that below file is present in `org-directory'
                 ;; and that it has a "Blog Ideas" heading. It can even be a
                 ;; symlink pointing to the actual location of all-posts.org!
                 (file+olp "all-posts.org" "INBOX")
                 (function org-hugo-new-subtree-post-capture-template))
        )
  )
```


#### 基本的工作流 {#基本的工作流}

捕获到的博客想法，利用 `capture` 记录下来，

利用 `org-roam` 整理笔记以输出内容，等文章整理完成以后，利用 `org-refile-copy` 把整个文章的内容 refile 到 all-post 下

然后利用 :PROPERTIES: , 单独配置文章的 HUGO_SECTION 以及 EXPORT_FILE_NAME 等属性即可完成博客的编写


### all-post 结构 {#all-post-结构}

\#+begin_details


#### INBOX {#inbox}

<!--list-separator-->

- <span class="org-todo todo TODO">TODO</span>  POST1 IDEA

<!--list-separator-->

- <span class="org-todo todo TODO">TODO</span>  POST2 IDEA


#### <span class="org-todo done DONE">DONE</span> FINISHED POST <span class="tag"><span class="_category">@category</span><span class="tag1">tag1</span><span class="tag2">tag2</span></span> {#finished-post}


#### <span class="org-todo done DONE">DONE</span> FINISHED POST2 <span class="tag"><span class="_category">@category</span><span class="tag1">tag1</span><span class="tag2">tag2</span></span> {#利用 emacs + hugo 搭建个人博客}

\#+end_details


## hugo 配置美化 {#hugo-配置美化}


### 主题美化 {#主题美化}

主题配置，准备环境中通过 \`git sub module\` 以及配置过相应的主题了，现在来切换一个新主题，美化一下 blog 以及优化一下配置

```bash
cd hugo-dir
git submodule add https://github.com/dillonzq/LoveIt.git themes/LoveIt
emacs hugo-toml
```

修改配置

```toml
baseURL = 'https://example.org/'

title = 'your title'

languageCode = 'zh-CN'
languageName = "简体中文"
hasCJKLanguage = true

theme = 'LoveIt'

[author]
    name = "author info"

[menu]
  [[menu.main]]
    weight = 1
    identifier = "posts"
    # 你可以在名称 (允许 HTML 格式) 之前添加其他信息, 例如图标
    pre = ""
    # 你可以在名称 (允许 HTML 格式) 之后添加其他信息, 例如图标
    post = ""
    name = "文章"
    url = "/posts/"
    # 当你将鼠标悬停在此菜单链接上时, 将显示的标题
    title = ""
  [[menu.main]]
    weight = 2
    identifier = "tags"
    pre = ""
    post = ""
    name = "标签"
    url = "/tags/"
    title = ""
  [[menu.main]]
    weight = 3
    identifier = "categories"
    pre = ""
    post = ""
    name = "分类"
    url = "/categories/"
    title = ""

[markup]
  # 语法高亮设置 (https://gohugo.io/content-management/syntax-highlighting)
  [markup.highlight]
    # false is required for LoveIt theme(https://github.com/dillonzq/LoveIt/issues/158)
    noClasses = false
```


### 更多主题 {#更多主题}

[Complete List | Hugo Themes](https://themes.gohugo.io)


## Blog 发布 {#blog-发布}


### 利用 Github Pages 发布 Blog <span class="tag"><span class="ATTACH">ATTACH</span></span> {#利用-github-pages-发布-blog}

1.  在 github 创建一个 \`username.github.io\` 的 \`repo\`

<!--listend-->

1.  在仓库的 **Settings -&gt; Pages** 里修改 Build and Deployment 的 **Source** 修改为 GitHub Actions

{{< figure src="/Users/zhangyang/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/_20240219_104007screenshot.png" >}}

1.  在本地的 hugo 代码库操作
    ```bash
          git remote add origin git@github.com:dreamkidd/dreamkidd.github.io.git
          git push --set-upstream origin main
          mkdir -p .github/workflows && touch .github/workflows/hugo.yaml
    ```

2.  将一下内容粘贴到 \`hugo.yaml\` 中

<!--listend-->

```yaml
# Sample workflow for building and deploying a Hugo site to GitHub Pages
name: Deploy Hugo site to Pages

on:
  # Runs on pushes targeting the default branch
  push:
    branches:
      - main

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

# Default to bash
defaults:
  run:
    shell: bash

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.122.0
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Install Dart Sass
        run: sudo snap install dart-sass
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4
      - name: Install Node.js dependencies
        run: "[[ -f package-lock.json || -f npm-shrinkwrap.json ]] && npm ci || true"
      - name: Build with Hugo
        env:
          # For maximum backward compatibility with Hugo modules
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  # Deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
```

1.  提交一下代码，查看效果

    PS: 提交代码务必把 \`.github\` 与 \`.gitmodules\` 加入 git 仓库

2.  在 repo 的 Actions 里查看 workflow 的结果是否正常

    {{< figure src="/Users/zhangyang/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/_20240219_111122screenshot.png" >}}

3.  以后每次提交，会自动进行构建发布


## Reference {#reference}


### [The world’s fastest framework for building websites | Hugo](https://gohugo.io) {#the-world-s-fastest-framework-for-building-websites-hugo}


### [ox-hugo - Org to Hugo exporter](https://ox-hugo.scripter.co) {#ox-hugo-org-to-hugo-exporter}


### [GitHub - dillonzq/LoveIt: ❤️A clean, elegant but advanced blog theme for Hugo...](https://github.com/dillonzq/LoveIt) {#github-dillonzq-loveit-️a-clean-elegant-but-advanced-blog-theme-for-hugo-dot-dot-dot}
