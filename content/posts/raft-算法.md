+++
title = "Raft 算法"
author = ["Kidddddddd"]
lastmod = 2025-01-20T13:17:08+08:00
categories = ["Technolgic"]
draft = true
+++

## Summary {#summary}

主要通过 raft 论文的解读，理解 raft 一致性算法

Raft 是一种用来管理日志复制的一致性算法，脱胎于 **Paxos** 但是比 **Paxos** 更容易理解

将一致性算法细分为了 3 个子问题，并对每个子问题进行了详细提供明确的说明

-   选主
-   日志复制
-   安全性


## 论文的内容概述 {#论文的内容概述}


### 复制状态机 Section2 {#复制状态机-section2}

通常的 RSM 是通过日志复制来实现的，而保证复制日志的一致性则依赖一致性算法，常见的一致性算法系统通常包括以下几点特性

-   安全性，一般再不考虑拜占庭问题下，出现的 网络延迟、分区、丢包重复问题不会导致系统出现异常结果
-   高可用，多数节点存活状态下，系统可用
-   不依赖时间来保障一致性
-   多数一致性，少数响应缓慢节点不影响整体性能


### Paxos 的问题 Section3 {#paxos-的问题-section3}

这部分主要介绍了 Paxos 在时间中的问题
Paxos 主要有两个障碍

1.  难以理解
    即使是最简单的 `Paxos` 单决议的子集，都是难以理解的
2.  没有为实际实现提供一个良好的基础

其次是复杂度很高，难以用于实践


### Raft 的设计目标 Section4 {#raft-的设计目标-section4}

Raft 的设计目标

1.  **为构建实际的实现提供良好的基础**
2.  **可理解**

Raft 为提高课理解性做出的两个方式

1.  细分问题
    1.  Leader Election（选主）
    2.  Log replication (日志复制)
    3.  Safety (安全性)
    4.  Membership change (成员变更)
2.  简化状态空间


### Raft 一致性算法 Section5-8 {#raft-一致性算法-section5-8}


### 评估Raft 与相关工作   Section9-10 {#评估raft-与相关工作-section9-10}

Section9 主要通过一些数据证明 raft 的易于理解、正确性以及性能的说明

Section10 主要是简单的介绍了一写与 raft 相关或类似的项目 `VR` ， `zookeeper`


## Raft 一致性算法 {#raft-一致性算法}

[Raft 算法概述](/Users/zhangyang/Documents/org/pages/fleeting/20250119T233828--raft-算法概述__distributed_raft.org)

[Raft 算法的关键属性](/Users/zhangyang/Documents/org/pages/fleeting/20250119T234732--raft-算法的关键属性__distributed_raft.org)

Raft 一致性算法细分为了一下 3 个子问题

1.  **Leader election**: 当现有的 Leader 失败时，需要选举出一个新 Leader
2.  **Log replication**: Leader 必须接受来自客户端的日志条目，并将其复制到集群中，并保证其他日志与自己的日志保持一致。
3.  **Safety**: 如果一个服务确认了给定所以的日志，其他服务绝对不会使用相同的索引


### [Raft basic](/Users/zhangyang/Documents/org/pages/fleeting/20250120T002025--raft-basic__distributed_raft.org) {#raft-basic--users-zhangyang-documents-org-pages-fleeting-20250120t002025-raft-basic-distributed-raft-dot-org}


### [Raft Leader Election](/Users/zhangyang/Documents/org/pages/fleeting/20250120T004750--raft-leader-election__distributed_raft.org) {#raft-leader-election--users-zhangyang-documents-org-pages-fleeting-20250120t004750-raft-leader-election-distributed-raft-dot-org}


### [Raft Log Replication](/Users/zhangyang/Documents/org/pages/fleeting/20250120T022250--raft-log-replication__distributed_raft.org) {#h:92f74b1f-7464-490a-b7a2-d16dc5d6331c}


### [Raft Safety](/Users/zhangyang/Documents/org/pages/fleeting/20250120T025440--raft-safety__distributed_raft.org) {#raft-safety--users-zhangyang-documents-org-pages-fleeting-20250120t025440-raft-safety-distributed-raft-dot-org}


### [Raft Follower 与 Candidate 崩溃](/Users/zhangyang/Documents/org/pages/fleeting/20250120T031002--raft-follower-与-candidate-崩溃__raft.org) {#h:af8257a7-7fe3-46df-b55f-9beeab11fab7}


### [Raft Timing](/Users/zhangyang/Documents/org/pages/fleeting/20250120T032307--raft-timing__distributed_raft.org) {#h:b63d806c-b776-4ca3-a1a0-a1eb368aee0c}


### [Raft cluster membership chages](/Users/zhangyang/Documents/org/pages/fleeting/20250120T033303--raft-cluster-membership-chages__distributed_raft.org) {#h:985f0309-5a0c-48ba-8f43-5e08f457789c}


### [Raft Log Compaction](/Users/zhangyang/Documents/org/pages/fleeting/20250120T034759--raft-log-compaction__distributed_raft.org) {#h:ce64fe8c-54ac-4671-bfa9-0cdd53afa07f}


### [Raft Client interaction](/Users/zhangyang/Documents/org/pages/fleeting/20250120T035447--raft-client-interaction__distributed_raft.org) {#h:62874502-bade-439a-829f-83147f1c309e}
