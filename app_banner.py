from rich.console import Console

console = Console()
program_version, date_of_program_change = "0.0.4", "01.01.2025"  # Версия программы, дата изменения


def banner() -> None:
    """Банер программы составлен с помощью https://manytools.org/hacker-tools/ascii-banner/"""
    console.print("|_   _|__| |___ __ _ _ _ __ _ _ __   / __|___ _ __  _ __  ___ _ _| |_ __ _| |_ ___ _ _ / __| _ \_   _|", style="bold red", justify="center")
    console.print("| |/ -_) / -_) _` | '_/ _` | '  \ | (__/ _ \ '  \| '  \/ -_) ' \  _/ _` |  _/ _ \ '_| (_ |  _/ | |  ", style="bold red", justify="center")
    console.print("|_|\___|_\___\__, |_| \__,_|_|_|_|_\___\___/_|_|_|_|_|_\___|_||_\__\__,_|\__\___/_|__\___|_|   |_|  ", style="bold red", justify="center")
    console.print(" |___/              |___|                                            |___|   ",style="bold red", justify="center")
    console.print("Telegram: https://t.me/PyAdminRU", style="bold red", justify="center")
    # Для удобства чтения, разделяем полосками https://rich.readthedocs.io/en/stable/console.html
    # Разнообразие консоли с модулем rich (python -m rich) - возможности модуля
    console.rule(f"[bold red]TELEGRAM_SMM_BOT версия программы: {program_version} "
                 f"(Дата изменения {date_of_program_change})")
    # Разнообразие консоли с модулем rich (пишем текст посередине)

if __name__ == "__main__":
    banner()
