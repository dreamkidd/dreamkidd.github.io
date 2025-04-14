+++
title = "RAGFlow ollama 部署本地知识库"
author = ["Kidddddddd"]
date = 2025-04-14T13:10:00+08:00
lastmod = 2025-04-14T13:18:01+08:00
categories = ["Technolgic"]
draft = false
+++

## Ollama 部署本地大模型 {#ollama-部署本地大模型}

Ollama 的优势

-   轻量级
-   本地化
-   多模型支持

安装 ollama

在 [Ollama](https://ollama.com) 下载安装

或者通过 `brew` 安转

`brew install ollama --cask`


## 部署 Deepseek-R1 {#部署-deepseek-r1}

`ollama run deepseek-r1:32b`


## 部署 RAGFLOW {#部署-ragflow}

> IMPORTANT
>
> -   While we also test RAGFlow on ARM64 platforms, we do not maintain RAGFlow Docker images for ARM. However, you can build an image yourself on a linux/arm64 or darwin/arm64 host machine as well.
> -   For ARM64 platforms, please upgrade the xgboost version in pyproject.toml to 1.6.0 and ensure unixODBC is properly installed.

RAGFlow 没有提供 ARM 平台的 Docker 镜像，需要自行本地构建

构建过程参考 [Build RAGFlow Docker image | RAGFlow](https://ragflow.io/docs/dev/build_docker_image)

> IMPORTANT
>
> -   While we also test RAGFlow on ARM64 platforms, we do not maintain RAGFlow Docker images for ARM. However, you can build an image yourself on a linux/arm64 or darwin/arm64 host machine as well.
> -   For ARM64 platforms, please upgrade the xgboost version in pyproject.toml to 1.6.0 and ensure unixODBC is properly installed.

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/
uv run download_deps.py
docker build -f Dockerfile.deps -t infiniflow/ragflow_deps .
docker build -f Dockerfile -t infiniflow/ragflow:nightly .
```

1.  国内的话，可以先修改一下 `Dockerfile` 中的 `ARG NEED_MIRROR` 可以把 0 修改成 1 ,使用国内的软件源。

2.  修改 `docker/.env` 的 `RAGFLOW_IMAGE` 配置，值改成构建好的 镜像名 `ragflow:nightly`
3.  运行服务
    ```bash
          cd docker
          docker compose -f docker-compose-macos.yml up -d
    ```
4.  构建完成以后，可以访问 `127.0.0.1:80` 来运行 RAGFlow


## 配置 RAGFlow <span class="tag"><span class="ATTACH">ATTACH</span></span> {#配置-ragflow}

配置本地模型文件的时候需要注意下

RAGFlow 是通过 `bridge` 方式桥接的，访问宿主服务，使用 `host.docker.internal:port` 可以访问到宿主服务

{{< figure src="/41/3b8fca-6dad-491c-8f91-8bdacf25fa78/_20250414_130738screenshot.png" >}}
