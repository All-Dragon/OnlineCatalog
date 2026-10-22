export {};

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        platform: string;
        ready: () => void;
        expand: () => void;
      };
    };
  }
}