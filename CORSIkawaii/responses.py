def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'current simulation':
        return '16 PeV'
    else:
        return 'Command not found'
