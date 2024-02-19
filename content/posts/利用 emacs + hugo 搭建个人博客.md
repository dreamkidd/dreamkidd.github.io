+++
title = "利用 emacs + hugo 搭建个人博客"
author = "ZhangYang"
lastmod = 2024-02-18T17:30:41+08:00
tags = ["emacs", "hugo"]
categories = ["tech"]
draft = false
+++

## 基础环境准备 {#基础环境准备}

基本依赖环境是 `emacs` `hugo` `git`


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

在 org 文件的头部设定好 `HUGO_BASE_DIR`

执行 `M-x org-hugo-exoirt-to-md` 即可导出 org 文件到指定的 hugo 目录下


## `ox-hugo` 工作流 {#ox-hugo-工作流}

ox-hugo 有支持以下两种工作流

1.  单 org 文件的工作流（推荐）
    -   通过 org 的 subtree 来导出单独的文章
    -   循环导出整个 subtree
2.  一个 org 文件一篇文章的工作流
    -   这样操作，就没法很好的利用 org 的标签，以及属性继承等特性，可以利用 `TODO` 关键字来标识草稿状态

那么就采用推荐的工作流来构建一个博客系统

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


### 暂时的基本的工作流想法 {#暂时的基本的工作流想法}

捕获到的博客想法，利用 `capture` 记录下来，

利用 `org-roam` 整理笔记以输出内容，等文章整理完成以后，利用 `org-refile-copy` 把整个文章的内容 refile 到 all-post 下

然后利用 :PROPERTIES: , 单独配置文章的 HUGO_SECTION 以及 TITLE 等属性即可完成博客的编写


## Reference {#reference}


### [The world’s fastest framework for building websites | Hugo](https://gohugo.io) {#the-world-s-fastest-framework-for-building-websites-hugo}


### [ox-hugo - Org to Hugo exporter](https://ox-hugo.scripter.co) {#ox-hugo-org-to-hugo-exporter}
