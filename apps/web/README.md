# Web-каталог

Next.js App Router. Публичная страница `/catalog` показывает названия и фотографии товаров, работает в браузере и Telegram Mini App без Telegram-авторизации.

## Структура

- `app/catalog/` - серверная страница каталога с динамическим рендерингом.
- `app/components/` - карточка, header, footer и клиентский TelegramBridge.
- `app/lib/` - адрес API и серверная загрузка товаров без кеширования.
- `app/styles/` - CSS Modules, `app/globals.css` - глобальные стили.
- `app/types/` - минимальные типы Telegram WebApp API.
- `app/health/route.ts` - GET `/health`, без обращения к API каталога.
- `next.config.ts` - standalone-сборка и rewrite изображений.

Страница получает товары на сервере; сервисный ключ и токен бота ей не нужны. Карточки и общий layout остаются Server Components. TelegramBridge выполняется на клиенте и вызывает `ready()`/`expand()` после монтирования. В обычном браузере каталог не зависит от наличия Telegram-контекста.

Браузер получает относительные image_url. При общем запуске `/api/` направляется Nginx в API; при прямом доступе к Next.js фотографию проксирует rewrite. Адрес API для rewrite фиксируется при сборке, адрес серверного fetch задаётся при запуске. В Docker оба используют `http://api:8000`.

Dockerfile устанавливает зависимости через `npm ci`, собирает приложение и переносит standalone-сервер, static и public в итоговый образ. Локальная установка Node.js для запуска через Docker не требуется.

Настройка окружения, HTTPS, запуск и проверки описаны в [главном README](../../README.md).
