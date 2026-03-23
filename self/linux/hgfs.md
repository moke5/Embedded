临时挂载共享文件夹

```bash
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other,nonempty
```

