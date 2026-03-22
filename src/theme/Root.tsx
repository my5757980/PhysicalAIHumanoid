import React from 'react';
import ChatWidget from '../components/ChatWidget';

/**
 * Root.tsx — Docusaurus swizzle wrapper (src/theme/Root.tsx).
 *
 * Docusaurus auto-discovers this file and wraps EVERY page with it,
 * injecting the ChatWidget into the bottom-right corner site-wide.
 *
 * No imports from Docusaurus internals are needed — the children prop
 * passes through the normal page render tree untouched.
 */
export default function Root({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
