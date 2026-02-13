"""ネットワークアダプター関連の型定義."""

from dataclasses import dataclass
from enum import Enum


class AdapterStatus(Enum):
    """ネットワークアダプターの状態."""

    UP = "Up"
    DISABLED = "Disabled"
    DISCONNECTED = "Disconnected"
    UNKNOWN = "Unknown"


class AdapterType(Enum):
    """ネットワークアダプターの種類."""

    ETHERNET = "Ethernet"
    WIFI = "Wi-Fi"
    UNKNOWN = "Unknown"


@dataclass(frozen=True)
class NetworkAdapter:
    """ネットワークアダプター情報."""

    name: str
    interface_description: str
    status: AdapterStatus
    adapter_type: AdapterType

    def is_enabled(self) -> bool:
        """アダプターが有効かどうかを返す."""
        return self.status == AdapterStatus.UP

    def is_ethernet(self) -> bool:
        """イーサネットアダプターかどうかを返す."""
        return self.adapter_type == AdapterType.ETHERNET

    def is_wifi(self) -> bool:
        """Wi-Fiアダプターかどうかを返す."""
        return self.adapter_type == AdapterType.WIFI
