"""モデルの型定義テスト."""

import pytest

from src.models.models import AdapterStatus, AdapterType, NetworkAdapter


class TestNetworkAdapter:
    """NetworkAdapterのテストクラス."""

    def test_network_adapter_creation(self) -> None:
        """NetworkAdapterインスタンス作成のテスト."""
        adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Realtek PCIe GbE Family Controller",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        assert adapter.name == "Ethernet"
        assert adapter.interface_description == "Realtek PCIe GbE Family Controller"
        assert adapter.status == AdapterStatus.UP
        assert adapter.adapter_type == AdapterType.ETHERNET

    def test_is_enabled_true(self) -> None:
        """有効なアダプターのis_enabledテスト."""
        adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Test",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        assert adapter.is_enabled() is True

    def test_is_enabled_false(self) -> None:
        """無効なアダプターのis_enabledテスト."""
        adapter = NetworkAdapter(
            name="Wi-Fi",
            interface_description="Test",
            status=AdapterStatus.DISABLED,
            adapter_type=AdapterType.WIFI,
        )

        assert adapter.is_enabled() is False

    def test_is_ethernet_true(self) -> None:
        """イーサネットアダプターのis_ethernetテスト."""
        adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Test",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        assert adapter.is_ethernet() is True
        assert adapter.is_wifi() is False

    def test_is_wifi_true(self) -> None:
        """Wi-Fiアダプターのis_wifiテスト."""
        adapter = NetworkAdapter(
            name="Wi-Fi",
            interface_description="Test",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.WIFI,
        )

        assert adapter.is_wifi() is True
        assert adapter.is_ethernet() is False

    def test_network_adapter_immutable(self) -> None:
        """NetworkAdapterが不変であることのテスト."""
        adapter = NetworkAdapter(
            name="Ethernet",
            interface_description="Test",
            status=AdapterStatus.UP,
            adapter_type=AdapterType.ETHERNET,
        )

        with pytest.raises(Exception):  # frozenなのでAttributeErrorまたはFrozenInstanceError
            adapter.name = "NewName"  # type: ignore


class TestAdapterStatus:
    """AdapterStatusのテストクラス."""

    def test_adapter_status_values(self) -> None:
        """AdapterStatusの値テスト."""
        assert AdapterStatus.UP.value == "Up"
        assert AdapterStatus.DISABLED.value == "Disabled"
        assert AdapterStatus.DISCONNECTED.value == "Disconnected"
        assert AdapterStatus.UNKNOWN.value == "Unknown"


class TestAdapterType:
    """AdapterTypeのテストクラス."""

    def test_adapter_type_values(self) -> None:
        """AdapterTypeの値テスト."""
        assert AdapterType.ETHERNET.value == "Ethernet"
        assert AdapterType.WIFI.value == "Wi-Fi"
        assert AdapterType.UNKNOWN.value == "Unknown"
