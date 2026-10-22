import type { ReactNode } from "react";
import Script from "next/script";

import { SiteFooter } from "./components/footer";
import { SiteHeader } from "./components/header";
import { TelegramBridge } from "./components/telegram";
import "./globals.css";

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body id="top">
        <Script
          src="https://telegram.org/js/telegram-web-app.js?64"
          strategy="beforeInteractive"
        />
        <TelegramBridge />
        <SiteHeader />
        {children}
        <SiteFooter />
      </body>
    </html>
  );
}
