+++
title = "ox-hugo 集成 mermaid"
author = ["Kidddddddd"]
date = 2025-02-16T22:19:00+08:00
lastmod = 2025-02-16T22:24:54+08:00
tags = ["hugo"]
categories = ["emacs"]
draft = false
mermaid = true
+++

## Memo 主题下的配置 {#memo-主题下的配置}

现在的 Blog 主题基于 [Hugo 主题 MemE 文档 | reuixiy](https://io-oi.me/tech/documentation-of-hugo-theme-meme/) 来做的，看了下文档，天然的原生支持 Mermaid , 就不用针对 hugo 做太多定制化的东西，需要注意 导出的配置的 `Front Matter` 有 `mermaid true` 的配置即可

我们用的是 ox-hugo ， 我们需要在自定义 FRONT_MATTER

```org
:EXPORT_HUGO_CUSTOM_FRONT_MATTER: :mermaid true
```

其次在 org-bable 中，对 mermaid 进行如下配置

```org
#+begin_src mermaid :exports code :results raw :hugo-shortcode mermaid
graph TD;
A-->B;
A-->C;
B-->D;
C-->D;
```


## 示例 {#示例}

如上的配置，就能正常转为 mermaid 图

```mermaid
graph TD;
A-->B;
A-->C;
B-->D;
C-->D;
```
