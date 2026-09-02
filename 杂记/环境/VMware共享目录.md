临时挂载共享文件夹

```bash
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other,nonempty
```



### 看虚拟机识别的磁盘大小

```shell
sudo fdisk -l /dev/sda

Disk /dev/sda: 80 GiB, 85899345920 bytes, 167772160 sectors
Disk model: VMware Virtual S
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe1c03ca8

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
/dev/sda2       1052670 41940991 40888322 19.5G  5 Extended
/dev/sda5       1052672 41940991 40888320 19.5G 83 Linux
```

