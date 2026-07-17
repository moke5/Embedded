

```
                 用户指定目录
                      |
                      v
              目录遍历模块
              (opendir/readdir)
                      |
                      v
          筛选 .bmp 图片文件
                      |
                      v
              创建图片链表
              (保存图片路径)
                      |
                      v
              遍历链表
                      |
                      v
              BMP解析模块
              (读取像素数据)
                      |
                      v
              LCD显示模块
              (mmap显存)
                      |
                      v
                   LCD屏幕
```























