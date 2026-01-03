'use client';

import { useEffect, useState } from 'react';
import { checkHealth } from '@/lib/api';

type Status = 'checking' | 'connected' | 'disconnected' | 'error';

export function BackendStatus() {
  const [status, setStatus] = useState<Status>('checking');
  const [openaiConfigured, setOpenaiConfigured] = useState(false);

  useEffect(() => {
    const verifyConnection = async () => {
      try {
        const health = await checkHealth();
        setStatus('connected');
        setOpenaiConfigured(health.openai_configured);
      } catch (error) {
        setStatus('disconnected');
        setOpenaiConfigured(false);
      }
    };

    // Check immediately
    verifyConnection();

    // Check every 10 seconds
    const interval = setInterval(verifyConnection, 10000);

    return () => clearInterval(interval);
  }, []);

  if (status === 'checking') {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" />
        <span>Checking backend...</span>
      </div>
    );
  }

  if (status === 'disconnected') {
    return (
      <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400">
        <div className="w-2 h-2 bg-red-500 rounded-full" />
        <span>Backend disconnected</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      <div className="w-2 h-2 bg-green-500 rounded-full" />
      <span className="text-green-600 dark:text-green-400">Backend connected</span>
      {!openaiConfigured && (
        <span className="text-yellow-600 dark:text-yellow-400 text-xs">
          (OpenAI key not configured)
        </span>
      )}
    </div>
  );
}

