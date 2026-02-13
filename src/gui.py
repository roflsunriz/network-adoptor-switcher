"""GUI実装モジュール."""

import logging
import tkinter as tk
from tkinter import messagebox, ttk

from src.models.models import NetworkAdapter
from src.network_manager import NetworkManager, NetworkManagerError

logger = logging.getLogger(__name__)


class NetworkAdapterGUI:
    """ネットワークアダプター切り替えGUI."""

    def __init__(self, root: tk.Tk) -> None:
        """GUIを初期化."""
        self.root = root
        self.root.title("ネットワークアダプター切り替えツール")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.network_manager = NetworkManager()

        # 管理者権限チェック
        if not self.network_manager.is_admin():
            messagebox.showerror(
                "エラー",
                "このアプリケーションは管理者権限で実行する必要があります。\n"
                "管理者として実行してください。",
            )
            self.root.quit()
            return

        self.ethernet_adapter: NetworkAdapter | None = None
        self.wifi_adapter: NetworkAdapter | None = None

        self._create_widgets()
        self._refresh_status()

    def _create_widgets(self) -> None:
        """ウィジェットを作成."""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # タイトル
        title_label = ttk.Label(
            main_frame,
            text="ネットワークアダプター切り替え",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # イーサネット情報フレーム
        ethernet_frame = ttk.LabelFrame(main_frame, text="イーサネット", padding="10")
        ethernet_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(ethernet_frame, text="名前:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.ethernet_name_label = ttk.Label(ethernet_frame, text="読込中...")
        self.ethernet_name_label.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(ethernet_frame, text="状態:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.ethernet_status_label = ttk.Label(ethernet_frame, text="読込中...")
        self.ethernet_status_label.grid(row=1, column=1, sticky=tk.W, pady=2)

        # Wi-Fi情報フレーム
        wifi_frame = ttk.LabelFrame(main_frame, text="Wi-Fi", padding="10")
        wifi_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(wifi_frame, text="名前:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.wifi_name_label = ttk.Label(wifi_frame, text="読込中...")
        self.wifi_name_label.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(wifi_frame, text="状態:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wifi_status_label = ttk.Label(wifi_frame, text="読込中...")
        self.wifi_status_label.grid(row=1, column=1, sticky=tk.W, pady=2)

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.ethernet_button = ttk.Button(
            button_frame,
            text="イーサネットに切り替え",
            command=self._switch_to_ethernet,
            width=25,
        )
        self.ethernet_button.grid(row=0, column=0, padx=5)

        self.wifi_button = ttk.Button(
            button_frame,
            text="Wi-Fiに切り替え",
            command=self._switch_to_wifi,
            width=25,
        )
        self.wifi_button.grid(row=0, column=1, padx=5)

        # 更新ボタン
        refresh_button = ttk.Button(
            main_frame,
            text="状態を更新",
            command=self._refresh_status,
        )
        refresh_button.grid(row=4, column=0, columnspan=2, pady=10)

        # ステータスバー
        self.status_bar = ttk.Label(
            main_frame,
            text="準備完了",
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    def _update_status_display(self) -> None:
        """アダプター情報の表示を更新."""
        if self.ethernet_adapter:
            self.ethernet_name_label.config(text=self.ethernet_adapter.name)
            status_text = self.ethernet_adapter.status.value
            if self.ethernet_adapter.is_enabled():
                self.ethernet_status_label.config(
                    text=f"{status_text} (有効)", foreground="green"
                )
            else:
                self.ethernet_status_label.config(
                    text=f"{status_text} (無効)", foreground="red"
                )
        else:
            self.ethernet_name_label.config(text="見つかりません")
            self.ethernet_status_label.config(text="N/A", foreground="gray")

        if self.wifi_adapter:
            self.wifi_name_label.config(text=self.wifi_adapter.name)
            status_text = self.wifi_adapter.status.value
            if self.wifi_adapter.is_enabled():
                self.wifi_status_label.config(
                    text=f"{status_text} (有効)", foreground="green"
                )
            else:
                self.wifi_status_label.config(
                    text=f"{status_text} (無効)", foreground="red"
                )
        else:
            self.wifi_name_label.config(text="見つかりません")
            self.wifi_status_label.config(text="N/A", foreground="gray")

        # ボタンの有効/無効を制御
        both_adapters_found = (
            self.ethernet_adapter is not None and self.wifi_adapter is not None
        )
        self.ethernet_button.config(
            state=tk.NORMAL if both_adapters_found else tk.DISABLED
        )
        self.wifi_button.config(state=tk.NORMAL if both_adapters_found else tk.DISABLED)

    def _refresh_status(self) -> None:
        """アダプター状態を更新."""
        try:
            self.status_bar.config(text="アダプター情報を取得中...")
            self.root.update()

            self.ethernet_adapter = self.network_manager.find_ethernet_adapter()
            self.wifi_adapter = self.network_manager.find_wifi_adapter()

            self._update_status_display()
            self.status_bar.config(text="更新完了")
            logger.info("アダプター情報を更新しました")

        except NetworkManagerError as e:
            logger.error(f"アダプター情報更新エラー: {e}")
            messagebox.showerror("エラー", f"アダプター情報の取得に失敗しました\n{e}")
            self.status_bar.config(text="更新失敗")

    def _switch_to_ethernet(self) -> None:
        """イーサネットに切り替え."""
        try:
            if not self.ethernet_adapter or not self.wifi_adapter:
                messagebox.showwarning(
                    "警告", "イーサネットまたはWi-Fiアダプターが見つかりません"
                )
                return

            # 確認ダイアログ
            result = messagebox.askyesno(
                "確認",
                f"Wi-Fi ({self.wifi_adapter.name}) を無効化し、\n"
                f"イーサネット ({self.ethernet_adapter.name}) を有効化します。\n\n"
                "よろしいですか？",
            )

            if not result:
                return

            self.status_bar.config(text="イーサネットに切り替え中...")
            self.root.update()

            self.network_manager.switch_to_ethernet()

            messagebox.showinfo("成功", "イーサネットに切り替えました")
            self._refresh_status()

        except NetworkManagerError as e:
            logger.error(f"イーサネット切り替えエラー: {e}")
            error_msg = f"イーサネットへの切り替えに失敗しました\n{e}"
            messagebox.showerror("エラー", error_msg)
            self.status_bar.config(text="切り替え失敗")

    def _switch_to_wifi(self) -> None:
        """Wi-Fiに切り替え."""
        try:
            if not self.ethernet_adapter or not self.wifi_adapter:
                messagebox.showwarning(
                    "警告", "イーサネットまたはWi-Fiアダプターが見つかりません"
                )
                return

            # 確認ダイアログ
            result = messagebox.askyesno(
                "確認",
                f"イーサネット ({self.ethernet_adapter.name}) を無効化し、\n"
                f"Wi-Fi ({self.wifi_adapter.name}) を有効化します。\n\n"
                "よろしいですか？",
            )

            if not result:
                return

            self.status_bar.config(text="Wi-Fiに切り替え中...")
            self.root.update()

            self.network_manager.switch_to_wifi()

            messagebox.showinfo("成功", "Wi-Fiに切り替えました")
            self._refresh_status()

        except NetworkManagerError as e:
            logger.error(f"Wi-Fi切り替えエラー: {e}")
            messagebox.showerror("エラー", f"Wi-Fiへの切り替えに失敗しました\n{e}")
            self.status_bar.config(text="切り替え失敗")

    def run(self) -> None:
        """GUIを起動."""
        self.root.mainloop()
