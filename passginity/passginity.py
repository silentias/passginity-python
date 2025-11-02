import secrets

eng_alphabet: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_alphabet: str = "0123456789"
sym_alphabet: str = "!@#$%^&*()_+-=[]{};':,.<>/?"

ambiguous: set[str] = {'0', 'O', '1', 'I', 'l'}


def pass_generate(
    length: int = 12, 
    eng_alp: bool = True, 
    num_alp: bool = True, 
    sym_alp: bool = True, 
    exclude_ambiguous: bool = False
) -> str:
    """
    Generates a cryptographically strong password of the specified length.

    Args:
        length (int): Password length. Must be a positive integer. Default is 12.
        eng_alp (bool): Whether to include Latin letters (a-z, A-Z). Default is True.
        num_alp (bool): Whether to include numbers (0-9). Defaults to True.
        sym_alp (bool): Whether to include special characters (!@#$%^&*...). Defaults to True.
        exclude_ambiguous (bool): Whether to exclude easily confused characters: 0/O, 1/I/l. Defaults to False.

    Returns:
        str: Generated password.

    Raises:
        ValueError: If length < 1 or all alphabets are disabled.

    Example:
        >>> pass_generate(length=10, exclude_ambiguous=True)
        'Kx9m$Rt7qW'
    """

    alphabet: str = ""

    if length < 1:
        raise ValueError("The password length must be at least 1.")
    if eng_alp:
        alphabet += eng_alphabet
    if num_alp:
        alphabet += num_alphabet
    if sym_alp:
        alphabet += sym_alphabet

    if not alphabet:
        raise ValueError("At least one character set must be included: letters, numbers, or symbols.")
    
    if exclude_ambiguous:
        alphabet = ''.join(c for c in alphabet if c not in ambiguous)

    return ''.join(secrets.choice(alphabet) for _ in range(length))