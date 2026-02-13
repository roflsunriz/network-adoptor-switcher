"""ネットワークアダプター切り替えアプリケーションのメインエントリーポイント."""

import logging
import sys
import tkinter as tk
from pathlib import Path

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("network_adapter_switcher.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main() -> None:
    """アプリケーションのメイン処理."""
    try:
        logger.info("アプリケーション起動")

        # srcディレクトリをパスに追加
        src_path = Path(__file__).parent.parent
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from src.gui import NetworkAdapterGUI

        root = tk.Tk()
        app = NetworkAdapterGUI(root)
        app.run()

        logger.info("アプリケーション終了")

    except Exception as e:
        logger.exception(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
