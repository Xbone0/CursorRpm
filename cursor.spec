Name:           cursor
Version:        0.47.9
Summary:        Cursor Code Editor
Release:        1%{?dist}
License:        Proprietary
URL:            https://cursor.sh/
Source0:        Cursor-0.47.9-x86_64.AppImage

BuildArch:      x86_64
AutoReqProv:    yes  # 启用自动依赖检测
Requires:       libX11, libXext, libxcb, libXrender, gtk3, glibc, libXScrnSaver, libXtst, libnotify, libatomic, libappindicator-gtk3, nss

%description
Cursor 是一款现代化的代码编辑器，基于 AI 增强，类似 VS Code。

%prep
chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract

%build
# 无需编译

%install
mkdir -p %{buildroot}/opt/Cursor
cp -r squashfs-root/usr/share/cursor/* %{buildroot}/opt/Cursor/
chmod +x %{buildroot}/opt/Cursor/cursor

# 设置快捷方式
install -D -m 644 squashfs-root/usr/share/applications/cursor.desktop \
    %{buildroot}/usr/share/applications/cursor.desktop
# 使用 sed 替换所有 Exec 条目
sed -i \
    -e 's#^Exec\s*=\s*cursor\([ \t]\)#Exec=/opt/Cursor/cursor\1#g' \       # 替换主 Exec
    -e 's#^Exec\s*=\s*cursor --new-window#Exec=/opt/Cursor/cursor --new-window#g' \  # 替换 Action Exec
    %{buildroot}/usr/share/applications/cursor.desktop
chmod +x %{buildroot}/usr/share/applications/cursor.desktop

# 安装图标
find squashfs-root/usr/share/icons/hicolor -maxdepth 1 -type d -name "*x*" | while read -r icon_dir; do
    size=$(basename "$icon_dir")
    install -D -m 755 "$icon_dir/apps/cursor.png" \
        "%{buildroot}/usr/share/icons/hicolor/${size}/apps/cursor.png"
done

%post
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :

%postun
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :

%files
/opt/Cursor/
/usr/share/applications/cursor.desktop
/usr/share/icons/hicolor/256x256/apps/cursor.png

%changelog
* Mon Mar 31 2025 He Gao <10340396@zte.com.cn> - 0.47.9-1
- 初始 RPM 包，修复路径和权限问题
