+++
title = "从 0 构造一个 BST"
author = ["Kidddddddd"]
lastmod = 2024-11-27T16:48:55+08:00
tags = ["leetcode"]
categories = ["Algorithm"]
draft = false
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

<div id="echarts-container" style="width: 100%; height: 600px;"></div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.3.3/dist/echarts.min.js"></script>
<script>
var myChart = echarts.init(document.getElementById('echarts-container'));
let treeData = [
          {
            name: '26',
            children: [
              {
                name: '5',
                children: [
                  { name: '3', children: [{ name: 'null' } ,{name : '4'}] },
                  {
                    name: '22',
                    children: [
                      {
                        name: '20',
                        children: [{ name: 'null' },{name:'21'}]
                      },
                      {
                        name: 'null'
                      }
                    ]
                  }
                ]
              },
              {
                name: '28',
                children: [{ name: '27' }, { name: '32' }]
              }
            ]
          }
];
myChart.setOption(
  (option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove'
    },
    series: [
      {
        type: 'tree',
        data: treeData,
        left: '2%',
        right: '2%',
        top: '8%',
        bottom: '20%',
        symbol: 'circle',
        symbolSize: 50,
        label: {
          position: 'inside',
          rotate: 0,
          verticalAlign: 'middle',
          align: 'middle',
          fontSize: 11
        },
        leaves: {
          label: {
            position: 'inside',
            rotate: 0,
            verticalAlign: 'middle',
            align: 'middle'
          }
        },
        initialTreeDepth: Infinity, // 设置树的初始展开深度为无限，展开所有节点
        expandAndCollapse: false, // 禁用展开和折叠功能，确保所有节点默认展开
        orient: 'TB', // 默认是纵向布局，从上到下
        layout: 'force', // 设置布局方式为正交方式
        nodePadding: 10, // 节点间的间距，防止节点重叠
        emphasis: {
          focus: 'descendant'
        },
        animationDurationUpdate: 750
      }
    ]
  })
);
</script>

remove 是 BST 实现中最复杂的操作，如果要删除的节点，同时拥有左右子节点的情况，光想想就会很复杂

我们先来思考一个简单的特殊操作，找到树中的最大/最小值，删除树中的最大最小值

我们代码中只实现删除最小值的方式，如上图，我们从 `root` 出发，在左子树上遍历，在递归的过程中，我们更新左子树的指针为删除后返回的节点

1.  左子树不为空，则不是最小值，则继续遍历左子树
2.  左子树为空，则返回右子树；右子树不为空，则父节点的左指针指向了删除节点的右子树；右子树为空，则父节点的左指针指向了null

<!--listend-->

```java
    public void delMin() {
        delMin(root);
    }

    private Node delMin(Node node) {
        if (node.left == null) {
            return node.right;
        }
        node.left = delMin(node.left);
        node.size = size(node.left) + size(node.right) + 1;
        return node;
    }
```

现在从特殊到一般情况，考虑删除任意节点

从逻辑上讲，我们首先需要递归的找到需要删除的目标 `key`

先思考一下 BST 的一个特性，就是中序遍历是有序的，如下图，中序遍历的就是 `[3,4,5,21,20,22,16,27,28,32]` ,假如我们删除 `5` ，那么 `5` 在树中的位置，需要一个元素填充过来，继续保证二叉树的有序性，很显然，这个节点放 `4,19` 是可以继续保证节点的有序性的，这俩节点分别是被删除节点的前驱节点与后继节点

现在我们考虑一下如何删除

1.  我们先递归的从 `root` 开始，找到删除的目标节点 `x`
2.  我们用一个临时变量 `tmp` 来指向 `x`
3.  将 `x.right` 指向 `delMin` 的返回值，即 **删除后所有节点大于删除节点的子二叉树**
4.  将 `x.left` 指向 `tmp.left` ，即 **删除后所有节点小于删除节点的子二叉树**

<!--listend-->

```java
    @Override
    public void remove(K k) {
        remove(root, k);
    }

    private Node remove(Node x, K k) {
        final int cmp = x.k.compareTo(k);
        if (cmp < 0) {
            //IMPORTANT 这里是递归的设置 x 节点的 left 指针，不能直接 return
            x.left = remove(x.left, k);
        } else if (cmp > 0) {
            x.right = remove(x.right, k);
        } else {
            //找到了 要删除的节点
            if (x.left == null) {
                //左子树为空，直接返回右子树 图中 删除 3 的 case
                return x.right;
            }
            if (x.right == null) {
                //右子树为空，直接返回左子树 图中删除 22 的 case
                return x.left;
            }
            //左右都不为空
            Node tmp = x;
            x = findMin(x.right);
            x.right = delMin(x.right);
            x.left = tmp.left;
        }
        x.size = size(x.left) + size(x.right) + 1;
        return x;
    }
```


### 总结 {#总结}

以上基本完成了一个 BST 的基本实现，BST 被诟病的问题是平衡性的问题，极端情况下，会退化为链表，生成上很少有实际使用，但是作为一种基础数据结构，是简单且在大部分情况下足够高效的，效率上可能比不过红黑树，但是实现复杂度上，BST 要简单很多当然使用 Java 的情况下，我们基本不太可能自己构建一个 BST ，内置的 HashMap,TreeMap 已经实现了很高效的查找表，不过还是需要理解算法的基本逻辑与做法；

一个小💡

BST 的问题是不平衡导致的效率退化，那么我是不是可以来定期的对 BST 进行一个异步的 rebalance ？来周期性的保证树的平衡性，保证算法效率不会退化的太过分

但是很显然如果要异步处理，每次 rebalance 都需要 O(n) 的时间与空间，还需要考虑 rebalance 期间的数据读写的同步问题，这样实现的复杂度又很高了，不如找到一种更高效的平衡方式，把 rebalance 的操作均摊到每次操作中


### 完整代码 {#完整代码}

```java
interface Bst<K extends Comparable<K>, V> {

    V find(K k);

    void insert(K k, V v);

    void remove(K k);

    int size();

    void delMin();

    V findMin();

}

public class BstTree<K extends Comparable<K>, V> implements Bst<K, V> {

    private Node root;

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
        node.size = size(node.left) + size(node.right) + 1;
        return node;
    }

    @Override
    public void remove(K k) {
        remove(root, k);
    }

    private Node remove(Node x, K k) {
        final int cmp = x.k.compareTo(k);
        if (cmp < 0) {
            //IMPORTANT 这里是递归的设置 x 节点的 left 指针，不能直接 return
            x.left = remove(x.left, k);
        } else if (cmp > 0) {
            x.right = remove(x.right, k);
        } else {
            //找到了 要删除的节点
            if (x.left == null) {
                //左子树为空，直接返回右子树 图中 删除 3 的 case
                return x.right;
            }
            if (x.right == null) {
                //右子树为空，直接返回左子树 图中删除 22 的 case
                return x.left;
            }
            //左右都不为空
            Node tmp = x;
            x = findMin(x.right);
            x.right = delMin(x.right);
            x.left = tmp.left;
        }
        x.size = size(x.left) + size(x.right) + 1;
        return x;
    }

    @Override
    public int size() {
        return size(root);
    }

    @Override
    public void delMin() {
        delMin(root);
    }

    private Node delMin(Node node) {
        if (node.left == null) {
            return node.right;
        }
        node.left = delMin(node.left);
        node.size = size(node.left) + size(node.right) + 1;
        return node;
    }

    @Override
    public V findMin() {
        if (root == null) {
            return null;
        }
        return findMin(root).v;
    }

    public Node findMin(Node n) {
        if (n.left == null) {
            return n;
        }
        return findMin(n.left);
    }

    private int size(Node n) {
        return n.size;
    }

    private class Node {
        K k;
        V v;
        Node left;
        Node right;
        int size;

        public Node(K k, V v) {
            this.k = k;
            this.v = v;
            this.size = 1;
        }
    }
}
```


## Reference {#reference}

实现思路参考了 《算法（第四版）》中 二叉查找树 的部分，书中的相关章节讨论了很多关于 BST 效率的问题，其他章节对一些基础算法都有详细的介绍与解析，以及丰富的测试用例与习题，推荐指数：🌟🌟🌟🌟🌟

这个算法的实现，可以解决下列

[701. 二叉搜索树中的插入操作 - 力扣（LeetCode）](https://leetcode.cn/problems/insert-into-a-binary-search-tree/)
[450. 删除二叉搜索树中的节点 - 力扣（LeetCode）](https://leetcode.cn/problems/delete-node-in-a-bst/)
[669. 修剪二叉搜索树 - 力扣（LeetCode）](https://leetcode.cn/problems/trim-a-binary-search-tree/description/)
[108. 将有序数组转换为二叉搜索树 - 力扣（LeetCode）](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/)
