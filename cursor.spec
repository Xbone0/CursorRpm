%global version_is_defined %{expand:%%{?version:1}%%{!?version:0}}

%if %{version_is_defined} == 0
%{error: 版本未指定！请通过 --define "version X.X.X" 传递版本号}
%endif

Name:           cursor
Version:        %{version}
Release:        1%{?dist}
Summary:        Cursor Code Editor
License:        Proprietary
URL:            https://cursor.sh/
Source0:        Cursor-%{version}-x86_64.AppImage

BuildArch:      x86_64
AutoReqProv:    yes
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

mkdir -p %{buildroot}/usr/share/applications
cat > %{buildroot}/usr/share/applications/cursor.desktop <<EOF
[Desktop Entry]
Name=Cursor
Comment=The AI Code Editor.
GenericName=Text Editor
Exec=/opt/Cursor/cursor %F
Icon=cursor
Type=Application
StartupNotify=false
StartupWMClass=Cursor
Categories=TextEditor;Development;IDE;
MimeType=application/x-cursor-workspace;
Actions=new-empty-window;
Keywords=cursor;
X-AppImage-Version=%{version}

[Desktop Action new-empty-window]
Name=New Empty Window
Name[de]=Neues leeres Fenster
Name[es]=Nueva ventana vacía
Name[fr]=Nouvelle fenêtre vide
Name[it]=Nuova finestra vuota
Name[ja]=新しい空のウィンドウ
Name[ko]=새 빈 창
Name[ru]=Новое пустое окно
Name[zh_CN]=新建空窗口
Name[zh_TW]=開新空視窗
Exec=/opt/Cursor/cursor --new-window %F
Icon=cursor
EOF
chmod +x %{buildroot}/usr/share/applications/cursor.desktop

for size in 22 24 32 48 64 128 256 512; do
  mkdir -p %{buildroot}/usr/share/icons/hicolor/${size}x${size}/apps
  install -D -m 644 squashfs-root/usr/share/icons/hicolor/${size}x${size}/apps/cursor.png \
        "%{buildroot}/usr/share/icons/hicolor/${size}x${size}/apps/cursor.png"
done

%post
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :

%postun
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :

%files
/opt/Cursor/
/usr/share/applications/cursor.desktop
/usr/share/icons/hicolor/*x*/apps/cursor.png

%changelog
* Mon Mar 31 2025 He Gao <10340396@zte.com.cn> - %{version}-%{release}
- Build RPM package for Cursor, version %{version}
