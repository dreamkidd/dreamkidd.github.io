+++
title = "从 0 构造一个 BST"
author = ["Kidddddddd"]
lastmod = 2024-11-26T18:23:02+08:00
categories = ["Algorithm"]
draft = true
+++

## Summary {#summary}

BST 二叉搜索树，是一颗二叉树，其中的每个节点的值，都大于 **左子树的任意节点** 而小于 **右子树的任意节点**


## 基本结构 {#基本结构}

BST 是一个数据形态相对特殊的二叉树，二叉树本质是一种特化的链表结构，同时持有左右两个节点的指针，是一种天然的递归结构，

```java
class Node {
    int val;
    Node left;
    Node right;
}
```

扩展结构，我们针对 `Node` 的基本结构，进行一下扩展，支持 Key Value 格式的数据，更类似我们的 Map 结构，同时加入一个 `size` 属性，表示当前节点的子节点数量

我们利用泛型的上界来强制 K 必须是 Comparable 的字类

```java
class Node<K extend Comparable<K> , V> {
    K key;
    V value;
    Node<K extend Comparable, V> left;
    Node<K extend Comparable,V> right;
    int size;
}
```


## 算法抽象 {#算法抽象}

我们先最基本的需要提供 3 个抽象操作， `find()` , `insert()` , `remove()`

并且树内不允许存在重复 Key , 相同 Key 的 insert 操作，会覆盖之前的 value

```java
interface Bst<K extend Comparable<K>,V> {
    Value find(Key k);
    void insert(Key k,V v);
    void remove(Key k);
}
```

以上我们的准备工作基本完成了，后面的操作需要的时候我们在回来处理，基本模板如下：

```java
interface Bst<K extends Comparable<K>, V> {

    V find(K k);

    void insert(K k, V v);

    void remove(K k);
}

public class BstTree<K extends Comparable<K>, V> implements Bst<K, V> {

    private Node root;

    private class Node {
        K k;
        V v;
        Node left;
        Node right;
        int size;
    }
}
```


## 算法实现 {#算法实现}


### `find(K k)` {#find--k-k}

第一步先实现搜索算法 `find(K k)` , 如果我们找到 k ，则返回对应的 value ，否则我们返回 null , BST 的搜索是最简单的，我们从根节点开始搜索利用 `k` 与 Node 节点的 `kn` 进行比较，如果 `k < kn` , 则向左子树搜索，如果 `k > kn` 则向右子树搜索，如果 `k = kn` ，则返回节点 `value`

```java
    @Override
    public V find(K k) {
        final Node node = find(root, k);
        if (node != null) {
            return node.v;
        } else {
            return null;
        }
    }

    private Node find(Node n, K k) {
        if (n == null) {
            return null;
        }
        int cmp = k.compareTo(n.k);
        if (cmp < 0) {
            return find(n.left, k);
        } else if (cmp > 0) {
            return find(n.right, k);
        } else {
            return n;
        }
    }
```


### insert(K k,V v) {#insert--k-k-v-v}

插入也是比较简单的逻辑，我们从 `root` 节点开始，利用与 find 类似的逻辑找到可以插入节点的位置，构造一个新节点，然后进行插入。

```java
    @Override
    public void insert(K k, V v) {
        insert(root, k, v);
    }

    private Node insert(Node node, K k, V v) {
        if (node == null) {
            return new Node(k, v);
        }
        int cmp = k.compareTo(node.k);
        if (cmp < 0) {
            node.left = insert(node.left, k, v);
        } else if (cmp > 0) {
            node.right = insert(node.right, k, v);
        } else {
            node.v = v;
        }
        //插入的时候，需要更新一下 size
        node.size = size(node.left) + size(node.right) + 1;
        return node;
    }
```


### remove 实现 {#remove-实现}

remove 是 BST 实现中最复杂的逻辑，从逻辑上讲，我们首先需要递归的找到需要删除的目标 `key`  找到以后，删除这个节点就行，但是需要考虑的是，如果这个节点有子节点的情况下，我们应该怎么做

<div class="HTML">

&lt;div id="tree"&gt;&lt;/div&gt;

&lt;script src="<https://d3js.org/d3.v5.min.js>"&gt;&lt;/script&gt;
&lt;script&gt;
  var treeData = {
    "name": "1",
    "children": [
      {
        "name": "2",
        "children": [
          { "name": "4" },
          { "name": "5" }
        ]
      },
      {
        "name": "3",
        "children": [
          { "name": "6" },
          { "name": "7" }
        ]
      }
    ]
  };

var margin = { top: 20, right: 90, bottom: 30, left: 90 },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#tree").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var tree = d3.tree().size([height, width]);

var root = d3.hierarchy(treeData, function(d) { return d.children; });

tree(root);

var link = svg.selectAll(".link")
  .data(root.links())
  .enter().append("path")
  .attr("class", "link")
  .attr("d", d3.linkVertical()
    .x(function(d) { return d.x; })
    .y(function(d) { return d.y; })
  );

var node = svg.selectAll(".node")
  .data(root.descendants())
  .enter().append("g")
  .attr("class", "node")
  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

node.append("circle")
  .attr("r", 10);

  node.append("text")
    .attr("dy", -15)
    .attr("x", function(d) { return d.children ? -13 : 13; })
    .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
    .text(function(d) { return d.data.name; });
&lt;/script&gt;

</div>
