"""PyInstaller用ビルド設定生成スクリプト."""

import PyInstaller.__main__
import sys
from pathlib import Path

# プロジェクトルート
project_root = Path(__file__).parent

# アイコンファイルのパス（存在する場合）
icon_path = project_root / "icon.ico"
icon_arg = [f"--icon={icon_path}"] if icon_path.exists() else []

# PyInstallerの引数
args = [
    str(project_root / "src" / "main.py"),
    "--name=NetworkAdapterSwitcher",
    "--onefile",  # 単一の実行ファイル
    "--windowed",  # コンソールウィンドウを表示しない
    "--clean",  # ビルド前にキャッシュをクリア
    f"--distpath={project_root / 'dist'}",
    f"--workpath={project_root / 'build'}",
    f"--specpath={project_root}",
    "--add-data=src;src",  # srcディレクトリを含める
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.messagebox",
    "--uac-admin",  # 管理者権限を要求
    *icon_arg,
]

if __name__ == "__main__":
    print("PyInstallerでビルドを開始します...")
    print(f"引数: {' '.join(args)}")
    PyInstaller.__main__.run(args)
    print("\nビルド完了!")
    print(f"実行ファイル: {project_root / 'dist' / 'NetworkAdapterSwitcher.exe'}")
