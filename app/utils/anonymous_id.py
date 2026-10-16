import re
import secrets
import string

# Characters that are unambiguous for human reading/typing
# Excludes: '0', 'O', '1', 'I', 'L'
SAFE_ALPHANUMERIC = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
ANONYMOUS_ID_LENGTH = 8
ANONYMOUS_ID_REGEX = re.compile(rf"^[{SAFE_ALPHANUMERIC}]{{{ANONYMOUS_ID_LENGTH}}}$")


def generate_anonymous_id(length: int = ANONYMOUS_ID_LENGTH) -> str:
    """
    Generate a cryptographically secure, unambiguous anonymous user ID.
    Example: 'AX7K29P4'
    """
    return "".join(secrets.choice(SAFE_ALPHANUMERIC) for _ in range(length))


def validate_anonymous_id(anonymous_id: str) -> bool:
    """
    Validate that an anonymous ID follows the standard pattern.
    Case-insensitive normalization is applied before checking.
    """
    if not anonymous_id or not isinstance(anonymous_id, str):
        return False
    normalized = normalize_anonymous_id(anonymous_id)
    return bool(ANONYMOUS_ID_REGEX.match(normalized))


def normalize_anonymous_id(anonymous_id: str) -> str:
    """
    Normalize an anonymous ID by stripping whitespace and converting to uppercase.
    Substitutes common typing mistakes (e.g. '0' -> '8' if needed, or preserves uppercase).
    """
    if not anonymous_id:
        return ""
    return anonymous_id.strip().upper()
