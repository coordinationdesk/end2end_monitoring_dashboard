from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from maas_model.message import MAASBaseMessage


@dataclass
class EngineSession:
    """
    A base class to share data between engines
    """

    payload: Optional[MAASBaseMessage] = None

    session_dict: Dict[str, Any] = field(default_factory=lambda: {})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the session dictionnary

        Args:
            key: key
            default (any, optional): Default value if not present. Defaults to None.

        Returns:
            any: value of the key
        """
        return self.session_dict.get(key, default)

    def put(self, key: str, value: Any) -> None:
        """
        Put a value to the session dictionnary

        Args:
            key: key
            value: : matching value
        """
        self.session_dict[key] = value
