# git

## 



### 一、先减数据：git 克隆参数（不用下完整仓库）

#### 1. 浅克隆（只拿最新 1 条提交，砍掉全部历史）

```
# 只拉当前分支最新代码，不下载几十年提交记录
git clone --depth=1 https://github.com/xxx/xxx.git
```

适合：只编译运行、不需要查历史提交、不用回滚旧版本。

#### 2. 单分支克隆（不下载所有分支）

```
# 仅克隆 main 分支，不拉取 dev/test 等其他分支
git clone --single-branch -b main https://github.com/xxx/xxx.git
```

#### 3. 组合最强精简（日常最常用）

```
git clone --depth=1 --single-branch --no-tags https://github.com/xxx/xxx.git
```

`--no-tags`：不下载版本标签，再省一点流量。



