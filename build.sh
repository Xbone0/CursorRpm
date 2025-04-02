#!/bin/bash
set -e  # 任何命令失败则终止脚本
rpmbuild_dir="$HOME/rpmbuild"
rm -rf "$rpmbuild_dir/BUILD"/*

# 查找 AppImage 文件
appimage_file=$(find "$rpmbuild_dir/SOURCES" -maxdepth 1 -name 'Cursor-*-x86_64.AppImage' | head -n1)
if [[ -z "$appimage_file" ]]; then
    echo "错误：未找到 Cursor AppImage 文件。" >&2
    exit 1
fi

# 提取版本号
version=$(basename "$appimage_file" | sed -E 's/Cursor-([0-9]+\.[0-9]+\.[0-9]+)-x86_64.AppImage/\1/')
if [[ -z "$version" ]]; then
    echo "错误：无法提取版本号。" >&2
    exit 1
fi

# 构建 RPM
echo "正在构建版本 $version 的 RPM 包..."
rpmbuild -ba "$rpmbuild_dir/SPECS/cursor.spec" \
    --define "version $version" \
    --define "_sourcedir $rpmbuild_dir/SOURCES"

# 自动获取生成的 RPM 路径
rpm_file=$(find "$rpmbuild_dir/RPMS" -name "cursor-${version}-*.rpm" | head -n1)
if [[ -z "$rpm_file" ]]; then
    echo "错误：未找到生成的 RPM 文件。" >&2
    exit 1
fi

# 打包为 ZIP
zip_name="cursor-${version}-x86_64.zip"
zip "$zip_name" "$rpm_file"
echo "已生成 ZIP 包: $zip_name"
