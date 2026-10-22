"use client";

import { useEffect } from "react";

export function TelegramBridge() {
  useEffect(() => {
    const webApp = window.Telegram?.WebApp;

    if (!webApp || webApp.platform === "unknown") {
      return;
    }

    webApp.ready();
    webApp.expand();
  }, []);

  return null;
}