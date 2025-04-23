---
title: OAuth 2.0
date: 2025-04-22 21:10:31
lastmod: 2025-04-22 21:12:53
tags:
  - tech/security
categories:
  - Technolgic
aliases: 
description: 测试
summary: 测试
author:
  - Kidddddddd
draft: true
---

# 核心认知

> [!info] Oauth 隐式授权
> 隐式授权的定义特征是令牌（ID 令牌或访问令牌）直接从 /authorize 终结点返回，而不是从 /token 终结点返回。

## 授权流程 

![[Pasted image 20250422191659.png]]

## 参数说明

### Request

| 参数名称          | 类型          | 示例                                                                     | 说明                                                               |
| ------------- | ----------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------- |
| response_type | REQUIRED    | token                                                                  | 固定值 'token'                                                      |
| client_id     | REQUIRED    | odoo                                                                   | 在 OAuth Provider 中的 client 标识                                    |
| redirect_uri  | OPTIONAL    | http://odoo.local:8069/auth_oauth/signin                               | OAuth Provider 完成 OAuth 重定向的目标端点                                 |
| scope         | OPTIONAL    | openid email profile                                                   | 用来在客户端与服务端标识 Token 的请求的权限范围,通常是以空格分隔                             |
| state         | RECOMMENDED | {"d": "odoo", "p": 4, "r": "http%3A%2F%2Fodoo.local%3A8069%2Fodoo%3F"} | 由客户端提供的一个不透明信息，在 OAuth Server 响应的时会返回给 Client，客户端用来校验以防止 CSRF 攻击 |

### Response

| 参数名称          | 类型                | 示例                                                    | 说明                                                                                             |
| ------------- | ----------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| access_token  | REQUIRED          | xxx.yyy.zzz                                           | authorization server 授权后提供的 Access Token                                                       |
| token_type    | REQUIRED          | Bearer                                                | Token 类型                                                                                       |
| expires_in    | RECOMMENDED       | 900                                                   | Access Token 的过期时间，以**秒**为单位                                                                   |
| scope         | REQUIRED/OPTIONAL | openid email profile                                  | 如果客户端请求中存在，则可选返回，否则必须返回 Token 的权限范围                                                            |
| state         | OPTIONAL/REQUIRED | {"d":"odoo","p":4,"r":"http://odoo.local:8069/odoo?"} | 如果客户端请求中存在此参数，在响应中需要原格式返回                                                                      |
| iss           | OICD REQUIRED     | http://keycloak.local:8080/realms/beem                | （issuer）是 JWT 载荷里的标准声明，用来标识签发方；Keycloak 额外把它当 URL 参数写到 fragment 里，以便前端快速获知 Token 的发行域（realm）信息 |
| session_state | Keycloak CUSTOM   | 08dda9bc-ee6a-4805-b839-00c04acb6bd5                  | Keycloak 的会话跟踪字段                                                                               |

## 安全性问题

标准的隐式授权

# 知识网络

> [!question] 关联知识网络
> - 对比：
> - 扩展：
> - 案例：

# 开放问题

# 参考文献

> [!cite]  参考文献
>  - [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
>  - [Microsoft 标识平台和 OAuth 2.0 隐式授权流](https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-implicit-grant-flow?utm_source=chatgpt.com)