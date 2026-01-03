'use client';

import { ChatInterface } from '@/components/ChatInterface';
import { ThemeToggle } from '@/components/ThemeToggle';
import { BackendStatus } from '@/components/BackendStatus';

export default function Home() {
  return (
    <main className="min-h-screen bg-background transition-colors">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-foreground mb-2">
              Mental Coach
            </h1>
            <p className="text-muted-foreground">
              Your supportive AI companion for stress, motivation, habits, and confidence
            </p>
            <div className="mt-2">
              <BackendStatus />
            </div>
          </div>
          <ThemeToggle />
        </header>
        <ChatInterface />
      </div>
    </main>
  );
}

