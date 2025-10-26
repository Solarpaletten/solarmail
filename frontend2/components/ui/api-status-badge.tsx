"use client";

import { useEffect, useState } from "react";
import { Badge } from "./badge";
import { Wifi, WifiOff } from "lucide-react";
import { api } from "@/lib/api";

interface ApiStatusBadgeProps {
  showLabel?: boolean;
  className?: string;
}

export function ApiStatusBadge({ showLabel = true, className }: ApiStatusBadgeProps) {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkStatus = async () => {
    setIsChecking(true);
    try {
      const online = await api.ping();
      setIsOnline(online);
    } catch {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    // Initial check
    checkStatus();

    // Check every 30 seconds
    const interval = setInterval(checkStatus, 30000);

    return () => clearInterval(interval);
  }, []);

  if (isOnline === null) {
    return (
      <Badge variant="secondary" className={className}>
        <Wifi className="mr-1 h-3 w-3 animate-pulse" />
        {showLabel && "Checking..."}
      </Badge>
    );
  }

  return (
    <Badge
      variant={isOnline ? "success" : "destructive"}
      className={className}
      title={isOnline ? "API Connected" : "API Disconnected"}
    >
      {isOnline ? (
        <Wifi className="mr-1 h-3 w-3" />
      ) : (
        <WifiOff className="mr-1 h-3 w-3" />
      )}
      {showLabel && (isOnline ? "Online" : "Offline")}
    </Badge>
  );
}
