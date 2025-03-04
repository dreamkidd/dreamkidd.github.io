---
title: "《Kafka权威指南（第2版）》 简评"
author: ["Kidddddddd"]
date: 2025-02-16T14:27:00+08:00
lastmod: 2025-02-16T22:10:14+08:00
categories: ["Reading"]
draft: false
mermaid: true
---

书名：《Kafka权威指南（第2版）》

作者：格温·沙皮拉 托德·帕利诺 拉吉尼·西瓦拉姆 克里特·佩蒂

评分： 🌟🌟🌟


## 简评 {#简评}

**O'Reilly** 家的技术书，总体风格都差不多，属于偏入门向的书籍，这本书也一样，能给我们一个基本的框架结构，对 `Kafka` 有一个基本程度的了解,并对其设计与优化思路有一个大体的掌控

重点看了 1 - 7 章 ，8 ，9 章主要面向 `Stream` , 10 - 13 章 偏 OP 一些，后边有需求在回头看看

Kafka 设计之初可能是一个分布式的消息队列，但是随着其不断的迭代更新，现在称其为一个 分布式日志系统更合适一些。

首先，分布式系统能遇到的问题,Kafka 也会遇到，分布式系统的本质是一种基于不同场景的取舍， Kafka 的设计思路，是把这些取舍，交还给了用户，这也就是 Kafka 为什么难的原因

把选择权交给用户，这会提高系统设计的复杂难度，相对的，用户使用起来也会相对的困难，需要了解相关的知识也更多，但是这可能恰恰是 Kafka 如此流行的原因，因为其适应性广，这就让 Kafka 走出了一条与其他消息队列不同的路

本书没有特别深入到很底层的实现，而是从设置，使用层面，来简单的介绍了我们使用 Kafaka 中，在不同场景下，需要进行的一些配置，需要做的一些实现以及一些比较好的实践方式。

所以如果对特别底层感兴趣的话，这本书并不适合，市面上也没有找到特别符合的书，可能之间看源码更合适一些


## DEMO {#demo}

```mermaid
graph TD;
A-->B;
A-->C;
B-->D;
C-->D;
```
