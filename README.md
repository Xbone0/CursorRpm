```markdown
# Cursor Linux RPM 构建指南

## 环境要求
- 确保已安装 rpmbuild 工具链：
  ```bash
  sudo dnf install rpm-build -y  # RHEL/CentOS/Fedora
  # 或
  sudo apt install rpm -y      # Debian/Ubuntu
  ```

## 目录准备
创建标准 RPM 构建目录结构：
```bash
mkdir -pv ~/rpmbuild/{BUILD,SPECS,BUILDROOT,SOURCES,RPMS,SRPMS}
```

## 文件准备
1. 将 AppImage 文件放入资源目录：
   ```bash
   cp Cursor-*-x86_64.AppImage ~/rpmbuild/SOURCES/
   ```
2. 放置 spec 文件到规范目录：
   ```bash
   mv cursor.spec ~/rpmbuild/SPECS/
   ```

## 构建流程
完成上述准备后，执行构建命令：
```bash
./build.sh
```

## 构建结果
生成的 RPM 包将位于：
```
~/rpmbuild/RPMS/x86_64/
```
同时将于rpmbuild下生成 zip 包：

## 关于构建deb包，请参考：
```
https://gist.github.com/jonson/7720118c3deb8bba470f61466dac906a
```
