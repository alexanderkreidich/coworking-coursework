"""Скрипт автоматической съёмки скриншотов страниц приложения."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = Path("/Users/sasha/polytech/Курсовые/Course Web/docs/Крейдич_Александр_Дмитриевич_Раздел_2/images")
VIEWPORT = {"width": 1280, "height": 800}


def vhod(page, username, password):
    """Авторизация пользователя через форму входа."""
    page.goto(f"{BASE}/accounts/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    # Проверка успешного входа: на странице каталога должна быть кнопка выхода
    page.goto(f"{BASE}/resources/")
    page.wait_for_load_state("networkidle")
    assert "Выйти" in page.content(), f"Login failed for {username}"


def snimok(page, url, name):
    """Снимок страницы целиком (футер скрыт)."""
    page.goto(f"{BASE}{url}")
    page.wait_for_load_state("networkidle")
    # Скрываем футер с копирайтом, чтобы он не попадал в скриншоты для отчёта
    page.add_style_tag(content="footer { display: none !important; }")
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  ✓ {name}.png ({path.stat().st_size // 1024} KB)")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # === Контекст 1: гость (без авторизации) ===
        print("[Гость] Снимки публичных страниц")
        ctx = browser.new_context(viewport=VIEWPORT, locale="ru-RU")
        page = ctx.new_page()
        snimok(page, "/resources/", "skrin_katalog")
        snimok(page, "/subscriptions/", "skrin_tarify")
        snimok(page, "/accounts/login/", "skrin_vhod")
        snimok(page, "/accounts/register/", "skrin_registratsiya")
        snimok(page, "/accounts/password/reset/", "skrin_vosstanovlenie")
        snimok(page, "/resources/1/", "skrin_detali_resursa")
        ctx.close()

        # === Контекст 2: участник ===
        print("[Участник: ivanov] Снимки личного кабинета")
        ctx = browser.new_context(viewport=VIEWPORT, locale="ru-RU")
        page = ctx.new_page()
        vhod(page, "ivanov", "test12345")
        snimok(page, "/accounts/profile/", "skrin_lichnyj_kabinet")
        snimok(page, "/accounts/profile/edit/", "skrin_redaktirovanie_profilya")
        snimok(page, "/bookings/my/", "skrin_moi_bronirovaniya")
        snimok(page, "/bookings/create/1/", "skrin_forma_bronirovaniya")
        ctx.close()

        # === Контекст 3: администратор ===
        print("[Администратор: admin] Снимки админ-панелей")
        ctx = browser.new_context(viewport=VIEWPORT, locale="ru-RU")
        page = ctx.new_page()
        vhod(page, "admin", "test12345")
        snimok(page, "/resources/manage/", "skrin_admin_resursy")
        snimok(page, "/resources/manage/create/", "skrin_admin_sozdanie_resursa")
        snimok(page, "/bookings/all/", "skrin_admin_vse_bronirovaniya")
        snimok(page, "/stats/", "skrin_admin_statistika")
        ctx.close()

        browser.close()
    print("Готово.")


if __name__ == "__main__":
    main()
