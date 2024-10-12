+++
title = "Java 处理 heif 文件"
author = ["Kidddddddd"]
lastmod = 2024-10-12T17:38:11+08:00
tags = ["java"]
categories = ["technolgic"]
draft = false
+++

CLOSED: <span class="timestamp-wrapper"><span class="timestamp">[2024-10-12 六 17:11]</span></span>


## Summary {#summary}

一次用 Java 处理 `heif` 格式文件的碎碎念


## 背景 {#背景}

在维护我司的一个文档处理服务，主要是功能是把各种类型的文件，统一转成 pdf 添加水印，然后前端通过通过 `pdfview` 统一渲染 pdf ，实现各种文件在线预览的功能

底层用到的服务比较多，大部分文档是通过 `openoffice` 来实现，各种类型的图片资源是通过 `itext` 来支持的，但是 `itext` 的 `ImageData` 没法支持 `heif` 格式。需要单独支持一下 `heif` 转 pdf 功能


## 过程 {#过程}

先测试了下 openoffice 跟 itext  ，发现确实不能直接支持那剩下的方案优先考虑社区开源的 `java` 方案

但是看下来，也没有 pure java 的实现

`TwelveMonkeys` 是一个 Java 图片类型处理库，但是现在没有支持 `heif` 类型的图片

[haraldk/TwelveMonkeys#440 HEIF support](https://github.com/haraldk/TwelveMonkeys/issues/440)

看起来除非有人愿意实现或者资金支持，否则作者自己应该不会进行 HEIF 的支持了

然后 issue 里提到的 `NightMonkeys` 是基于 `libheif` 实现的，但是要求 Java22+ , 线上代码还停留在祖传的 Java8 ，这个库也没法直接用

[GitHub - gotson/NightMonkeys: Additional plug-ins and extensions for Java's I...](https://github.com/gotson/NightMonkeys)

那么基本就剩下 JNI 跟 调用命令两个方案了，相比之下，调用命令可能实现更简单一些，问题就只剩下怎么把 libheif 打入镜像了

`libheif` 底层依赖 `libde265`

由于各种网络环境的限制，已经一些其他，打镜像可谓是一波三折

基础镜像是一个基于 `centos7`

构建机器访问外网也有限制，没法直接通过 yum 安装

转而尝试自己编译，编译的时候，发现 yum 安装的 cmake 是 2.x  ，编译 libheif 需要 cmake 3.21 以上

又需要手动安装 `cmake`  好在 cmake 有提供现成的 `.sh` 脚本，直接加入到镜像里执行即可

```Dockerfile
FROM baseimage
MAINTAINER xxx
USER root

COPY repo.sh /root/repo.sh

RUN sh /root/repo.sh

RUN yum-config-manager --disable updates
RUN yum makecache
RUN yum groupinstall "Development Tools" -y
RUN yum install libjpeg-turbo-devel libpng-devel libtiff-devel -y

COPY cmake-3.29.8-linux-x86_64.sh /root/cmake-3.29.8-linux-x86_64.sh
RUN chmod +x /root/cmake-3.29.8-linux-x86_64.sh
RUN /root/cmake-3.29.8-linux-x86_64.sh --prefix=/usr/local --skip-license


RUN mkdir "/root/heif/"
COPY heif.sh /root/heif/heif.sh
COPY libde265-1.0.15.tar.gz /root/heif
COPY libheif-1.18.2.tar.gz /root/heif
RUN sh /root/heif/heif.sh
```

然后就是编译安装 `libde265` 以及 `libheif`

比较坑的是 ld 部分，不知道为啥这个镜像没法加载 `/usr/local/lib` 以及 `/usr/local/lib64` 下的动态库，导致命令安装成功，但是执行会报错，提示动态库加载不到

后来单独设置了一下，把 `/usr/local/lib` 以及 `/usr/local/lib64`  都加入到 `ld`  的文件夹下

```sh
base=/root/heif/
cd $base

tar zxvf libde265-1.0.15.tar.gz
tar zxvf libheif-1.18.2.tar.gz

cd $base/libde265-1.0.15
./autogen.sh
./configure
make && make install
echo "/usr/local/lib" > /etc/ld.so.conf.d/lib256.conf

cd $base/libheif-1.18.2
mkdir build
cd build
cmake --preset=release ..
make && make install

echo "/usr/local/lib64" > /etc/ld.so.conf.d/libheif.conf

ldconfig
```

构建好的镜像就加入了 `heif-convert` 命令，在 java 程序中，直接使用 `ProcessBuilder` 调用 `heif-convert`  即可


## 思考 {#思考}

这种方案并不能说是一个好方案，依赖底层环境，这种方案，换个环境就是个坑，但是在 docker 的加持下，这种方案可能算是一种比较快速的解决方案

整个过程中，确实没少问 GPT ，技术类问题， GPT 也不是真全知全能，也会睁着眼睛说瞎话，这个在使用的过程中，是需要自己去甄别测试的，但是确实能节约一些搜索时间。现在 GPT 对我来说差不多能替代 70% 在搜索引擎上的使用场景
