"""Interactive cleanup for the Instagram account configured in ./instagram.
No credentials, 2FA code, user lists, or session tokens are written to disk.

Main file: ./instagram

"""
from pathlib import Path
from typing import Iterable

import instagrapi
from instagrapi.exceptions import TwoFactorRequired  # type: ignore[import-not-found]


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "instagram"

# Conservative signals for accounts whose stated identity promotes harmful or
# illicit computing activity. Generic technology accounts are not included.
ADVERSE_TECH_TERMS = (
    "malware", "ransomware", "carding", "phishing", "cracking",
    "cracker", "ddos", "botnet", "keylogger", "spyware", "exploit",
    "pirataria", "pirate", "fraude", "golpe", "scam", "hackeado",
)


def read_config() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    if not values.get("INSTAGRAM_USERNAME") or not values.get("INSTAGRAM_PASSWORD"):
        raise RuntimeError("O arquivo instagram não contém usuário e senha válidos.")
    return values


def login(client: instagrapi.Client, username: str, password: str) -> None:
    # Used by Instagram's account-verification challenge (email/SMS).
    client.challenge_code_handler = lambda _username, _choice: input(
        "Código solicitado pelo Instagram (email/SMS): "
    ).strip()
    try:
        ok = client.login(username, password)
    except TwoFactorRequired:
        code = input("Código 2FA do Instagram: ").strip()
        ok = client.login(username, password, verification_code=code)
    if not ok:
        raise RuntimeError("O Instagram não confirmou o login.")


def adverse_tech_accounts(users: Iterable) -> list:
    matches = []
    for user in users:
        identity = f"{user.username} {user.full_name}".lower()
        if any(term in identity for term in ADVERSE_TECH_TERMS):
            matches.append(user)
    return matches


def main() -> None:
    config = read_config()
    client = instagrapi.Client()
    login(client, config["INSTAGRAM_USERNAME"], config["INSTAGRAM_PASSWORD"])
    print("Login confirmado. Carregando conexões e caixas de entrada...")

    following = client.user_following(str(client.user_id), amount=0)
    followers = client.user_followers(str(client.user_id), amount=0)
    not_following_back = [u for uid, u in following.items() if uid not in followers]
    adverse = adverse_tech_accounts(following.values())

    targets = {str(u.pk): u for u in not_following_back}
    for user in adverse:
        targets[str(user.pk)] = user

    print(
        f"Encontrados: {len(not_following_back)} que não seguem de volta; "
        f"{len(adverse)} com sinais explícitos de conteúdo tecnológico nocivo; "
        f"{len(targets)} deixará de seguir."
    )
    confirmation = input("Digite LIMPAR para confirmar as ações irreversíveis: ").strip()
    if confirmation != "LIMPAR":
        print("Nada foi alterado.")
        return

    unfollowed = 0
    for user in targets.values():
        if client.user_unfollow(str(user.pk)):
            unfollowed += 1

    # Official mobile endpoint used by the Instagram app to clear all recent searches.
    search_result = client.private_request(
        "fbsearch/clear_search_history/", {"_uuid": client.uuid}, with_signature=False
    )
    searches_cleared = search_result.get("status") == "ok"

    # Hide removes the conversation from this account's inbox; it does not
    # delete the other participant's copy. Fetch all available inbox views.
    threads = {}
    for box in (None, "primary", "general"):
        for thread in client.direct_threads(amount=0, box=box):
            threads[str(thread.id)] = thread
    hidden = 0
    for thread in threads.values():
        if client.direct_thread_hide(int(thread.id)):
            hidden += 1

    print("Concluído.")
    print(f"Deixou de seguir: {unfollowed}")
    print(f"Histórico de buscas limpo: {'sim' if searches_cleared else 'não confirmado'}")
    print(f"Conversas do Direct removidas da sua caixa de entrada: {hidden}")


if __name__ == "__main__":
    main()
