+++
title = "JVM C1 C2 占用 CPU 问题排查"
author = ["Kidddddddd"]
date = 2024-02-28T15:41:00+08:00
lastmod = 2025-02-16T22:28:52+08:00
tags = ["java", "jvm"]
categories = ["Tech"]
draft = false
+++

## Summary {#summary}

记一次 CPU 高占用的排查过程

由于 CodeCache 设置过小导致 C2 Compile 占用 CPU 的问题排查过程及原因分析

<!--more-->


## 事件 {#事件}

邮件服务收到告警，服务挂掉了，连到机器上查看发现服务还在运行，但是请求不能正常响应，服务卡死

`TOP` 命令观察发现 CPU 持续维持在 200+ 以上，遂重启实例，重启实例以后，服务恢复，但是 CPU 占用还是会周期性的飙升到 100+

但是很快 CPU 就会降低到正常值，过一会又飙起来了


## 排查 CPU 高的基本过程 <span class="tag"><span class="ATTACH">ATTACH</span></span> {#排查-cpu-高的基本过程}

先用 `top -Hp pid` 查看线程信息

{{< figure src="/51/41c5d6-ae06-420f-8288-9ad5ad31a8c0/_20240227_194922screenshot.png" >}}

```bash
> printf "%x\n" 72
48
```

由于容器内没有 arthas ，先用 `jstack` 观察一下

```bash
jstack 28 | grep "0x48"
"C2 CompilerThread1" #9 daemon prio=9 os_prio=0 tid=0x00007fa258d0f000 nid=0x48 waiting on condition [0x0000000000000000]
```

发现是 C2 编译线程，而且那几个线程 id 都是连续的，大概率都是 C2 相关的几个线程

```bash
jstack 28 | grep "C2"
"C2 CompilerThread7" #15 daemon prio=9 os_prio=0 tid=0x00007fa258d24800 nid=0x4e waiting on condition [0x0000000000000000]
"C2 CompilerThread6" #14 daemon prio=9 os_prio=0 tid=0x00007fa258d22800 nid=0x4d waiting on condition [0x0000000000000000]
"C2 CompilerThread5" #13 daemon prio=9 os_prio=0 tid=0x00007fa258d20000 nid=0x4c waiting on condition [0x0000000000000000]
"C2 CompilerThread4" #12 daemon prio=9 os_prio=0 tid=0x00007fa258d1e000 nid=0x4b waiting on condition [0x0000000000000000]
"C2 CompilerThread3" #11 daemon prio=9 os_prio=0 tid=0x00007fa258d13800 nid=0x4a waiting on condition [0x0000000000000000]
"C2 CompilerThread2" #10 daemon prio=9 os_prio=0 tid=0x00007fa258d11800 nid=0x49 waiting on condition [0x0000000000000000]
"C2 CompilerThread1" #9 daemon prio=9 os_prio=0 tid=0x00007fa258d0f000 nid=0x48 waiting on condition [0x0000000000000000]
"C2 CompilerThread0" #8 daemon prio=9 os_prio=0 tid=0x00007fa258d0d000 nid=0x47 waiting on condition [0x0000000000000000]
```

```bash
printf "%d\n" 0x4e
78
```

所以定位到的是 C2 导致的 CPU 高占用


## 分析 {#分析}

C2 是 JVM 用来进行 JIT 编译的线程，其过程是把 `byteCode` 编译为 `nativeCode` 的线程

按道理是不应该长时间占用 `CPU` 资源来执行代码编译操作，找了一圈资料，发现基本有一下几个解决办法


### 什么都不做 {#什么都不做}

偶发的情况下，确实可以什么都不做，只会是一个短期的影响


### 关闭分层编译 {#关闭分层编译}

通过控制 `--TieredCompilation` 参数，可以强制关闭 C2 分层编译，但是肯定会对性能有影响

这是作为最后的方案


### 其他 {#其他}

预热等方案，但是与我遇到的实际情况不符
还有一个利用 GBD 排查的，但是只是一个排查过程，可以给到一个启发思路，但是没有最终解决问题


## 解决 {#解决}

在线下环境依然能稳定复现，想在线下环境装个 arthas , 偶然的情况下，突然发现 C2 占用是有一定规则的，每次有请求进来的时候，C2 就会开始执行编译

可以稳定复现，于是排查 JVM 参数

发现 `-XX:ReservedCodeCacheSize=32m` 修改到 `512m` 后 C2 的 CPU 占用降低


## 问题探究 {#问题探究}

从现象看，应该跟 `CodeCache` 有关系，但是具体原因暂时不清楚，先跟踪一下 `CodeCache` 的情况

<details>
<div class="details">

ID    NAME                             GROUP            PRIORITY    STATE      %CPU       DELTA_TIME TIME        INTERRUPTE DAEMON
-1    C2 CompilerThread4               -                -1          -          3.24       0.161      1:2.351     false      true
-1    C2 CompilerThread1               -                -1          -          3.15       0.157      0:59.482    false      true
-1    C2 CompilerThread7               -                -1          -          1.01       0.050      0:57.240    false      true
-1    C2 CompilerThread0               -                -1          -          0.52       0.026      0:57.014    false      true
-1    C2 CompilerThread2               -                -1          -          0.35       0.017      1:2.947     false      true
-1    C1 CompilerThread8               -                -1          -          0.3        0.014      0:10.679    false      true
-1    C1 CompilerThread9               -                -1          -          0.29       0.014      0:10.745    false      true
-1    C2 CompilerThread6               -                -1          -          0.28       0.013      1:3.782     false      true
-1    C2 CompilerThread3               -                -1          -          0.27       0.013      0:58.764    false      true
309   SimplePauseDetectorThread_0      main             5           TIMED_WAIT 0.27       0.013      0:4.131     false      true
310   SimplePauseDetectorThread_1      main             5           TIMED_WAIT 0.26       0.012      0:4.213     false      true
311   SimplePauseDetectorThread_2      main             5           TIMED_WAIT 0.25       0.012      0:4.163     false      true
Memory                       used      total     max      usage     GC
heap                         1067M     4096M     4096M    26.05%    gc.g1_young_generation.count      34
g1_eden_space                470M      948M      -1       49.58%    gc.g1_young_generation.time(ms)   2926
g1_survivor_space            128M      128M      -1       100.00%   gc.g1_old_generation.count        0
g1_old_gen                   469M      3020M     4096M    11.45%    gc.g1_old_generation.time(ms)     0
nonheap                      175M      192M      -1       90.94%
code_cache                   20M       28M       32M      64.11%
metaspace                    137M      145M      -1       94.45%
compressed_class_space       16M       18M       1024M    1.65%
direct                       136K      136K      -        100.00%
mapped                       0K        0K        -        0.00%
Runtime
os.name                                                             Linux
os.version                                                          3.10.0-1160.92.1.el7.x86_64
java.version                                                        1.8.0_60
java.home                                                           /home/work/1.8.0_60/jre
systemload.average                                                  0.14
processors                                                          16
timestamp/uptime                                                    Wed Feb 28 10:54:33 CST 2024/2052s
ID    NAME                             GROUP            PRIORITY    STATE      %CPU       DELTA_TIME TIME        INTERRUPTE DAEMON
-1    C2 CompilerThread0               -                -1          -          15.87      0.793      0:57.807    false      true
-1    C2 CompilerThread6               -                -1          -          11.8       0.590      1:4.372     false      true
-1    C2 CompilerThread1               -                -1          -          3.85       0.192      0:59.675    false      true
-1    C2 CompilerThread2               -                -1          -          1.74       0.086      1:3.034     false      true
-1    C2 CompilerThread4               -                -1          -          1.37       0.068      1:2.420     false      true
-1    C2 CompilerThread7               -                -1          -          1.14       0.057      0:57.297    false      true
-1    C2 CompilerThread3               -                -1          -          0.8        0.040      0:58.804    false      true
-1    C2 CompilerThread5               -                -1          -          0.53       0.026      0:56.526    false      true
309   SimplePauseDetectorThread_0      main             5           TIMED_WAIT 0.3        0.014      0:4.146     false      true
311   SimplePauseDetectorThread_2      main             5           TIMED_WAIT 0.29       0.014      0:4.177     false      true
310   SimplePauseDetectorThread_1      main             5           TIMED_WAIT 0.28       0.014      0:4.227     false      true
-1    C1 CompilerThread9               -                -1          -          0.27       0.013      0:10.759    false      true
Memory                       used      total     max      usage     GC
heap                         1067M     4096M     4096M    26.05%    gc.g1_young_generation.count      34
g1_eden_space                470M      948M      -1       49.58%    gc.g1_young_generation.time(ms)   2926
g1_survivor_space            128M      128M      -1       100.00%   gc.g1_old_generation.count        0
g1_old_gen                   469M      3020M     4096M    11.45%    gc.g1_old_generation.time(ms)     0
nonheap                      174M      192M      -1       90.64%
code_cache                   19M       28M       32M      62.31%
metaspace                    137M      145M      -1       94.45%
compressed_class_space       16M       18M       1024M    1.65%
direct                       136K      136K      -        100.00%
mapped                       0K        0K        -        0.00%
</div>
</details>

可以观察到的现象有一下几点

1.  系统空闲时，C2 还是会持续性的执行 JIT 编译，平均每个线程占用在 2% 左右
2.  系统响应时，C2 线程的 CPU 会急剧上升
3.  `code_cache` 一直在 50%-80% 之间浮动
4.  C2 在容器里的线程数有 8 个，但是 CPU 实际在 POD 指定的 CPU 是 4 核心

调整 `-XX:ReservedCodeCacheSize=1024m`

<details>
<div class="details">

ID    NAME                             GROUP            PRIORITY    STATE      %CPU       DELTA_TIME TIME        INTERRUPTE DAEMON
311   SimplePauseDetectorThread_0      main             5           TIMED_WAIT 0.21       0.010      0:3.103     false      true
313   SimplePauseDetectorThread_2      main             5           TIMED_WAIT 0.21       0.010      0:3.077     false      true
312   SimplePauseDetectorThread_1      main             5           TIMED_WAIT 0.2        0.009      0:3.164     false      true
111   ee-ext-count-1                   main             5           TIMED_WAIT 0.07       0.003      0:1.493     false      false
82    Timer-for-arthas-dashboard-eaff5 system           5           RUNNABLE   0.07       0.003      0:1.088     false      true
-1    VM Periodic Task Thread          -                -1          -          0.05       0.002      0:1.112     false      true
-1    Unknown Thread                   -                -1          -          0.05       0.002      0:1.054     false      true
68    trace-collector                  main             5           TIMED_WAIT 0.04       0.002      0:1.264     false      false
299   ee-ext-12                        main             5           TIMED_WAIT 0.03       0.001      0:0.016     false      false
47    activiti-acquire-timer-jobs      main             5           TIMED_WAIT 0.03       0.001      0:0.370     false      false
41    SimplePauseDetectorThread_0      system           9           TIMED_WAIT 0.02       0.001      0:0.636     false      true
198   ee-ext-core-client-15            main             5           WAITING    0.02       0.001      0:0.015     false      false
Memory                       used      total     max      usage     GC
heap                         906M      4096M     4096M    22.13%    gc.g1_young_generation.count      27
g1_eden_space                324M      948M      -1       34.18%    gc.g1_young_generation.time(ms)   2492
g1_survivor_space            128M      128M      -1       100.00%   gc.g1_old_generation.count        0
g1_old_gen                   454M      3020M     4096M    11.10%    gc.g1_old_generation.time(ms)     0
nonheap                      202M      209M      -1       96.85%
code_cache                   63M       63M       1024M    6.18%
metaspace                    124M      129M      -1       95.97%
compressed_class_space       15M       16M       1024M    1.47%
direct                       80K       80K       -        100.00%
mapped                       0K        0K        -        0.00%
Runtime
</div>
</details>

C2 的 `CPU` 显著降低 `code_cache` 维持的 63M 左右,会随着系统运行过程逐步增加

问题很明显了， `code_cache` 不足会导致 C2 持续的编译操作,长时间占用 CPU ，导致程序响应缓慢

Oracle 官方文档中有如下一段内容

<details>
<div class="details">

Keep in mind that the codecache starts relatively small and then grows as needed as new methods are compiled.Sometimes compiled methods are freed from the codecache, especially when the maximum size of the codecache is constrained. The memory used by free methods can be reused for newly compiled methods, allowing additional methods to be compiled without growing the codecache further.
-- [15 Codecache Tuning (Release 8)](https://docs.oracle.com/javase/8/embedded/develop-apps-platforms/codecache.htm)
</div>
</details>

意味这在当 限制了 codecache 的情况下，已经被编译的代码会被从 codecache 中释放出来，这大概就是当 `ReservedCodeCacheSize=32m` 的时候，C2 会持续性占用 CPU 的缘故，由于 codecache 最大值的限制，导致了 JIT 编译的代码被从 codecache 释放出来，而后有由于有新的请求，导致部分代码又通过 C2 执行 JIT 编译，如此往复循环，导致 C2 周期性的高占用 CPU


## Refrence {#refrence}


### [Java C2 CompilerThread 长期占用 CPU 过高，如何查找原因？ | HeapDump性能社区](https://heapdump.cn/question/2499643) {#java-c2-compilerthread-长期占用-cpu-过高-如何查找原因-heapdump性能社区}


### [Analyzing a stuck HotSpot C2 compilation | by Vladimir Sitnikov | netcracker ...](https://medium.com/netcracker/analyzing-a-stuck-hotspot-c2-compilation-85e0ca230744) {#analyzing-a-stuck-hotspot-c2-compilation-by-vladimir-sitnikov-netcracker-dot-dot-dot}


### [jvm编译器参数及踩坑-弃用C2 | Zong's blog](https://www.lstop.pub/2021/09/07/jvm%E7%BC%96%E8%AF%91%E5%99%A8%E5%8F%82%E6%95%B0%E5%8F%8A%E8%B8%A9%E5%9D%91/) {#jvm编译器参数及踩坑-弃用c2-zong-s-blog}


### [【问题排查系列】C2 compilerthread 带来的CPU抖动问题 - 掘金](https://juejin.cn/post/6991655671783489544) {#问题排查系列-c2-compilerthread-带来的cpu抖动问题-掘金}


### [聊聊jvm的Code Cache - 简书](https://www.jianshu.com/p/b064274536ed) {#聊聊jvm的code-cache-简书}


### [15 Codecache Tuning (Release 8)](https://docs.oracle.com/javase/8/embedded/develop-apps-platforms/codecache.htm) {#15-codecache-tuning--release-8}


### [Introduction to JVM Code Cache | Baeldung](https://www.baeldung.com/jvm-code-cache) {#introduction-to-jvm-code-cache-baeldung}
