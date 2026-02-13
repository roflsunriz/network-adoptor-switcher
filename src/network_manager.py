"""ネットワークアダプター管理モジュール."""

import ctypes
import json
import logging
import subprocess
import sys

from src.models.models import AdapterStatus, AdapterType, NetworkAdapter

logger = logging.getLogger(__name__)

# Windows用のサブプロセスウィンドウ非表示フラグ
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


class NetworkManagerError(Exception):
    """ネットワークマネージャーのエラー."""

    pass


class NetworkManager:
    """ネットワークアダプターを管理するクラス."""

    @staticmethod
    def is_admin() -> bool:
        """管理者権限で実行されているかチェック."""
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception as e:
            logger.error(f"管理者権限チェックに失敗: {e}")
            return False

    @staticmethod
    def _parse_adapter_type(interface_desc: str) -> AdapterType:
        """インターフェース説明からアダプタータイプを判定."""
        desc_lower = interface_desc.lower()
        if "wi-fi" in desc_lower or "wireless" in desc_lower or "wifi" in desc_lower:
            return AdapterType.WIFI
        elif (
            "ethernet" in desc_lower
            or "gigabit" in desc_lower
            or "realtek" in desc_lower
            or "intel" in desc_lower
        ):
            # イーサネット系のキーワードをチェック
            return AdapterType.ETHERNET
        return AdapterType.UNKNOWN

    @staticmethod
    def _parse_status(status_str: str) -> AdapterStatus:
        """ステータス文字列をAdapterStatusに変換."""
        status_lower = status_str.lower().strip()
        if status_lower == "up":
            return AdapterStatus.UP
        elif status_lower == "disabled":
            return AdapterStatus.DISABLED
        elif status_lower == "disconnected":
            return AdapterStatus.DISCONNECTED
        return AdapterStatus.UNKNOWN

    def get_adapters(self) -> list[NetworkAdapter]:
        """全ネットワークアダプターの情報を取得."""
        try:
            # PowerShellコマンドでアダプター情報を取得
            # UTF-8エンコーディングを明示的に設定
            ps_command = (
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
                "$OutputEncoding = [System.Text.Encoding]::UTF8; "
                "Get-NetAdapter | "
                "Select-Object Name, InterfaceDescription, Status | "
                "ConvertTo-Json"
            )
            cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                ps_command,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                creationflags=CREATE_NO_WINDOW,
            )

            if result.returncode != 0:
                raise NetworkManagerError(
                    f"アダプター情報の取得に失敗: {result.stderr}"
                )

            # JSONパースして処理
            adapters_data = json.loads(result.stdout)

            # 単一アダプターの場合、リストに変換
            if isinstance(adapters_data, dict):
                adapters_data = [adapters_data]

            adapters: list[NetworkAdapter] = []
            for data in adapters_data:
                name = data.get("Name", "")
                interface_desc = data.get("InterfaceDescription", "")
                status_str = data.get("Status", "Unknown")

                adapter_type = self._parse_adapter_type(interface_desc)
                status = self._parse_status(status_str)

                adapters.append(
                    NetworkAdapter(
                        name=name,
                        interface_description=interface_desc,
                        status=status,
                        adapter_type=adapter_type,
                    )
                )

            return adapters

        except subprocess.CalledProcessError as e:
            logger.error(f"PowerShellコマンド実行エラー: {e}")
            raise NetworkManagerError(f"アダプター情報取得エラー: {e}") from e
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析エラー: {e}")
            raise NetworkManagerError(f"アダプター情報解析エラー: {e}") from e
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            raise NetworkManagerError(f"アダプター情報取得エラー: {e}") from e

    def find_ethernet_adapter(self) -> NetworkAdapter | None:
        """イーサネットアダプターを検索."""
        adapters = self.get_adapters()
        for adapter in adapters:
            if adapter.is_ethernet():
                return adapter
        return None

    def find_wifi_adapter(self) -> NetworkAdapter | None:
        """Wi-Fiアダプターを検索."""
        adapters = self.get_adapters()
        for adapter in adapters:
            if adapter.is_wifi():
                return adapter
        return None

    def enable_adapter(self, adapter_name: str) -> None:
        """指定したアダプターを有効化."""
        if not self.is_admin():
            raise NetworkManagerError("管理者権限が必要です")

        try:
            ps_command = (
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
                "$OutputEncoding = [System.Text.Encoding]::UTF8; "
                f"Enable-NetAdapter -Name '{adapter_name}' -Confirm:$false"
            )
            cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                ps_command,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                creationflags=CREATE_NO_WINDOW,
            )

            if result.returncode != 0:
                raise NetworkManagerError(
                    f"アダプター '{adapter_name}' の有効化に失敗: {result.stderr}"
                )

            logger.info(f"アダプター '{adapter_name}' を有効化しました")

        except subprocess.CalledProcessError as e:
            logger.error(f"アダプター有効化エラー: {e}")
            raise NetworkManagerError(
                f"アダプター '{adapter_name}' の有効化に失敗: {e}"
            ) from e

    def disable_adapter(self, adapter_name: str) -> None:
        """指定したアダプターを無効化."""
        if not self.is_admin():
            raise NetworkManagerError("管理者権限が必要です")

        try:
            ps_command = (
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
                "$OutputEncoding = [System.Text.Encoding]::UTF8; "
                f"Disable-NetAdapter -Name '{adapter_name}' -Confirm:$false"
            )
            cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                ps_command,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                creationflags=CREATE_NO_WINDOW,
            )

            if result.returncode != 0:
                raise NetworkManagerError(
                    f"アダプター '{adapter_name}' の無効化に失敗: {result.stderr}"
                )

            logger.info(f"アダプター '{adapter_name}' を無効化しました")

        except subprocess.CalledProcessError as e:
            logger.error(f"アダプター無効化エラー: {e}")
            raise NetworkManagerError(
                f"アダプター '{adapter_name}' の無効化に失敗: {e}"
            ) from e

    def switch_to_ethernet(self) -> None:
        """イーサネットに切り替え（Wi-Fi無効化、イーサネット有効化）."""
        ethernet = self.find_ethernet_adapter()
        wifi = self.find_wifi_adapter()

        if ethernet is None:
            raise NetworkManagerError("イーサネットアダプターが見つかりません")
        if wifi is None:
            raise NetworkManagerError("Wi-Fiアダプターが見つかりません")

        logger.info("イーサネットに切り替えます")
        self.disable_adapter(wifi.name)
        self.enable_adapter(ethernet.name)

    def switch_to_wifi(self) -> None:
        """Wi-Fiに切り替え（イーサネット無効化、Wi-Fi有効化）."""
        ethernet = self.find_ethernet_adapter()
        wifi = self.find_wifi_adapter()

        if ethernet is None:
            raise NetworkManagerError("イーサネットアダプターが見つかりません")
        if wifi is None:
            raise NetworkManagerError("Wi-Fiアダプターが見つかりません")

        logger.info("Wi-Fiに切り替えます")
        self.disable_adapter(ethernet.name)
        self.enable_adapter(wifi.name)
