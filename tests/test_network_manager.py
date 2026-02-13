"""NetworkManagerのテスト."""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.network_manager import NetworkManager, NetworkManagerError
from src.models.models import AdapterStatus, AdapterType, NetworkAdapter


class TestNetworkManager:
    """NetworkManagerのテストクラス."""

    def test_is_admin_true(self) -> None:
        """管理者権限がある場合のテスト."""
        with patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=1):
            assert NetworkManager.is_admin() is True

    def test_is_admin_false(self) -> None:
        """管理者権限がない場合のテスト."""
        with patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=0):
            assert NetworkManager.is_admin() is False

    def test_is_admin_error(self) -> None:
        """管理者権限チェックでエラーが発生した場合のテスト."""
        with patch(
            "ctypes.windll.shell32.IsUserAnAdmin", side_effect=Exception("Test error")
        ):
            assert NetworkManager.is_admin() is False

    @pytest.mark.parametrize(
        "interface_desc,expected_type",
        [
            ("Intel(R) Wi-Fi 6 AX200", AdapterType.WIFI),
            ("Realtek PCIe GbE Family Controller", AdapterType.ETHERNET),
            ("Intel(R) Ethernet Connection", AdapterType.ETHERNET),
            ("Unknown Device", AdapterType.UNKNOWN),
        ],
    )
    def test_parse_adapter_type(
        self, interface_desc: str, expected_type: AdapterType
    ) -> None:
        """アダプタータイプの判定テスト."""
        manager = NetworkManager()
        result = manager._parse_adapter_type(interface_desc)
        assert result == expected_type

    @pytest.mark.parametrize(
        "status_str,expected_status",
        [
            ("Up", AdapterStatus.UP),
            ("Disabled", AdapterStatus.DISABLED),
            ("Disconnected", AdapterStatus.DISCONNECTED),
            ("Unknown", AdapterStatus.UNKNOWN),
            ("Invalid", AdapterStatus.UNKNOWN),
        ],
    )
    def test_parse_status(
        self, status_str: str, expected_status: AdapterStatus
    ) -> None:
        """ステータス文字列の変換テスト."""
        manager = NetworkManager()
        result = manager._parse_status(status_str)
        assert result == expected_status

    def test_get_adapters_success_multiple(self) -> None:
        """複数アダプターの取得成功テスト."""
        manager = NetworkManager()

        mock_adapters = [
            {
                "Name": "Ethernet",
                "InterfaceDescription": "Realtek PCIe GbE Family Controller",
                "Status": "Up",
            },
            {
                "Name": "Wi-Fi",
                "InterfaceDescription": "Intel(R) Wi-Fi 6 AX200",
                "Status": "Disabled",
            },
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(mock_adapters)
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            adapters = manager.get_adapters()

            assert len(adapters) == 2
            assert adapters[0].name == "Ethernet"
            assert adapters[0].adapter_type == AdapterType.ETHERNET
            assert adapters[0].status == AdapterStatus.UP
            assert adapters[1].name == "Wi-Fi"
            assert adapters[1].adapter_type == AdapterType.WIFI
            assert adapters[1].status == AdapterStatus.DISABLED

    def test_get_adapters_success_single(self) -> None:
        """単一アダプターの取得成功テスト."""
        manager = NetworkManager()

        mock_adapter = {
            "Name": "Ethernet",
            "InterfaceDescription": "Realtek PCIe GbE Family Controller",
            "Status": "Up",
        }

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(mock_adapter)
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            adapters = manager.get_adapters()

            assert len(adapters) == 1
            assert adapters[0].name == "Ethernet"
            assert adapters[0].adapter_type == AdapterType.ETHERNET

    def test_get_adapters_command_error(self) -> None:
        """コマンド実行エラーのテスト."""
        manager = NetworkManager()

        with patch(
            "subprocess.run",
            side_effect=Exception("Command failed"),
        ):
            with pytest.raises(NetworkManagerError):
                manager.get_adapters()

    def test_find_ethernet_adapter(self) -> None:
        """イーサネットアダプター検索のテスト."""
        manager = NetworkManager()

        mock_adapters = [
            NetworkAdapter(
                name="Ethernet",
                interface_description="Realtek PCIe GbE Family Controller",
                status=AdapterStatus.UP,
                adapter_type=AdapterType.ETHERNET,
            ),
            NetworkAdapter(
                name="Wi-Fi",
                interface_description="Intel(R) Wi-Fi 6 AX200",
                status=AdapterStatus.DISABLED,
                adapter_type=AdapterType.WIFI,
            ),
        ]

        with patch.object(manager, "get_adapters", return_value=mock_adapters):
            ethernet = manager.find_ethernet_adapter()
            assert ethernet is not None
            assert ethernet.name == "Ethernet"
            assert ethernet.adapter_type == AdapterType.ETHERNET

    def test_find_wifi_adapter(self) -> None:
        """Wi-Fiアダプター検索のテスト."""
        manager = NetworkManager()

        mock_adapters = [
            NetworkAdapter(
                name="Ethernet",
                interface_description="Realtek PCIe GbE Family Controller",
                status=AdapterStatus.UP,
                adapter_type=AdapterType.ETHERNET,
            ),
            NetworkAdapter(
                name="Wi-Fi",
                interface_description="Intel(R) Wi-Fi 6 AX200",
                status=AdapterStatus.DISABLED,
                adapter_type=AdapterType.WIFI,
            ),
        ]

        with patch.object(manager, "get_adapters", return_value=mock_adapters):
            wifi = manager.find_wifi_adapter()
            assert wifi is not None
            assert wifi.name == "Wi-Fi"
            assert wifi.adapter_type == AdapterType.WIFI

    def test_enable_adapter_no_admin(self) -> None:
        """管理者権限なしでのアダプター有効化テスト."""
        manager = NetworkManager()

        with patch.object(manager, "is_admin", return_value=False):
            with pytest.raises(NetworkManagerError, match="管理者権限が必要です"):
                manager.enable_adapter("Ethernet")

    def test_enable_adapter_success(self) -> None:
        """アダプター有効化成功のテスト."""
        manager = NetworkManager()

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""

        with patch.object(manager, "is_admin", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                manager.enable_adapter("Ethernet")  # エラーが発生しないことを確認

    def test_disable_adapter_no_admin(self) -> None:
        """管理者権限なしでのアダプター無効化テスト."""
        manager = NetworkManager()

        with patch.object(manager, "is_admin", return_value=False):
            with pytest.raises(NetworkManagerError, match="管理者権限が必要です"):
                manager.disable_adapter("Wi-Fi")

    def test_disable_adapter_success(self) -> None:
        """アダプター無効化成功のテスト."""
        manager = NetworkManager()

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""

        with patch.object(manager, "is_admin", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                manager.disable_adapter("Wi-Fi")  # エラーが発生しないことを確認

    def test_switch_to_ethernet_success(self) -> None:
        """イーサネット切り替え成功のテスト."""
        manager = NetworkManager()

        ethernet_adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Realtek PCIe GbE Family Controller",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        wifi_adapter = NetworkAdapter(
            name="Wi-Fi",
            interface_description="Intel(R) Wi-Fi 6 AX200",
            status=AdapterStatus.DISABLED,
            adapter_type=AdapterType.WIFI,
        )

        with patch.object(
            manager, "find_ethernet_adapter", return_value=ethernet_adapter
        ):
            with patch.object(manager, "find_wifi_adapter", return_value=wifi_adapter):
                with patch.object(manager, "disable_adapter") as mock_disable:
                    with patch.object(manager, "enable_adapter") as mock_enable:
                        manager.switch_to_ethernet()

                        mock_disable.assert_called_once_with("Wi-Fi")
                        mock_enable.assert_called_once_with("Ethernet")

    def test_switch_to_ethernet_no_ethernet(self) -> None:
        """イーサネットアダプターがない場合のテスト."""
        manager = NetworkManager()

        wifi_adapter = NetworkAdapter(
            name="Wi-Fi",
            interface_description="Intel(R) Wi-Fi 6 AX200",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.WIFI,
        )

        with patch.object(manager, "find_ethernet_adapter", return_value=None):
            with patch.object(manager, "find_wifi_adapter", return_value=wifi_adapter):
                with pytest.raises(
                    NetworkManagerError, match="イーサネットアダプターが見つかりません"
                ):
                    manager.switch_to_ethernet()

    def test_switch_to_wifi_success(self) -> None:
        """Wi-Fi切り替え成功のテスト."""
        manager = NetworkManager()

        ethernet_adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Realtek PCIe GbE Family Controller",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        wifi_adapter = NetworkAdapter(
            name="Wi-Fi",
            interface_description="Intel(R) Wi-Fi 6 AX200",
            status=AdapterStatus.DISABLED,
            adapter_type=AdapterType.WIFI,
        )

        with patch.object(
            manager, "find_ethernet_adapter", return_value=ethernet_adapter
        ):
            with patch.object(manager, "find_wifi_adapter", return_value=wifi_adapter):
                with patch.object(manager, "disable_adapter") as mock_disable:
                    with patch.object(manager, "enable_adapter") as mock_enable:
                        manager.switch_to_wifi()

                        mock_disable.assert_called_once_with("Ethernet")
                        mock_enable.assert_called_once_with("Wi-Fi")

    def test_switch_to_wifi_no_wifi(self) -> None:
        """Wi-Fiアダプターがない場合のテスト."""
        manager = NetworkManager()

        ethernet_adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Realtek PCIe GbE Family Controller",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        with patch.object(
            manager, "find_ethernet_adapter", return_value=ethernet_adapter
        ):
            with patch.object(manager, "find_wifi_adapter", return_value=None):
                with pytest.raises(
                    NetworkManagerError, match="Wi-Fiアダプターが見つかりません"
                ):
                    manager.switch_to_wifi()
