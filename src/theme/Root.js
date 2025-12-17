import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// Default implementation, that you can customize
function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}

export default Root;