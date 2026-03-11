'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Briefcase, TrendingUp, Bot } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { href: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { href: '/portfolio', icon: Briefcase, label: 'Portfolio' },
  { href: '/stocks/AAPL', icon: TrendingUp, label: 'Stocks' },
  { href: '/agents', icon: Bot, label: 'Agents' },
];

function isRouteActive(pathname: string, href: string): boolean {
  if (href === '/') return pathname === '/';
  const segment = `/${href.split('/')[1]}`;
  return pathname.startsWith(segment);
}

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 flex-shrink-0 border-r border-border bg-card flex flex-col">
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <TrendingUp className="w-4 h-4 text-primary" />
          </div>
          <div>
            <p className="text-sm font-semibold">HedgeFund AI</p>
            <p className="text-xs text-muted-foreground">Simulator</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ href, icon: Icon, label }) => {
          const active = isRouteActive(pathname, href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
                active
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground',
              )}
            >
              <Icon className="w-4 h-4" />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-2 px-3 py-2">
          <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
            <span className="text-xs text-primary font-medium">U</span>
          </div>
          <div>
            <p className="text-xs font-medium">Demo User</p>
            <p className="text-xs text-muted-foreground">demo@hedgefund.ai</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
