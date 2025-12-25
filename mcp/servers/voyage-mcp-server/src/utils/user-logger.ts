import fs from 'fs';
import path from 'path';
import { mkdirp } from 'mkdirp';
import { LogEntry, LogEntrySchema } from '../types.js';

export class UserLogger {
  private userId: string;
  private baseLogDir: string;
  private logQueue: LogEntry[] = [];
  private flushTimeout: NodeJS.Timeout | null = null;
  private readonly FLUSH_INTERVAL = 1000;
  private readonly MAX_QUEUE_SIZE = 100;

  constructor(userId: string, baseLogDir: string = 'user_logs') {
    this.userId = userId;
    this.baseLogDir = baseLogDir;
    this.setupLogDirectory();
  }

  private setupLogDirectory() {
    const userDir = path.join(this.baseLogDir, this.userId);
    mkdirp.sync(userDir);
  }

  private getLogFilePath(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    const monthDir = path.join(this.baseLogDir, this.userId, year.toString(), month);
    mkdirp.sync(monthDir);

    return path.join(monthDir, `${day}.jsonl`);
  }

  log(event: Omit<LogEntry, 'timestamp'>): void {
    const logEntry: LogEntry = {
      timestamp: new Date().toISOString(),
      userId: this.userId,
      ...event
    };

    try {
      LogEntrySchema.parse(logEntry);
    } catch (error) {
      console.error('Invalid log entry structure:', error);
      return;
    }

    this.logQueue.push(logEntry);

    if (this.logQueue.length >= this.MAX_QUEUE_SIZE) {
      this.flushLogs();
    } else if (!this.flushTimeout) {
      this.flushTimeout = setTimeout(() => this.flushLogs(), this.FLUSH_INTERVAL);
    }
  }

  private flushLogs(): void {
    if (this.logQueue.length === 0) {
      this.flushTimeout = null;
      return;
    }

    try {
      const logPath = this.getLogFilePath();
      const jsonLines = this.logQueue
        .map(entry => JSON.stringify(entry))
        .join('\n') + '\n';

      fs.appendFileSync(logPath, jsonLines, 'utf-8');
    } catch (error) {
      console.error('Error writing logs:', error);
    } finally {
      this.logQueue = [];
      this.flushTimeout = null;
    }
  }

  getLogs(startDate: Date, endDate: Date): LogEntry[] {
    const logs: LogEntry[] = [];
    const startYear = startDate.getFullYear();
    const startMonth = startDate.getMonth() + 1;
    const endYear = endDate.getFullYear();
    const endMonth = endDate.getMonth() + 1;

    for (let year = startYear; year <= endYear; year++) {
      const monthStart = year === startYear ? startMonth : 1;
      const monthEnd = year === endYear ? endMonth : 12;

      for (let month = monthStart; month <= monthEnd; month++) {
        const monthDir = path.join(
          this.baseLogDir,
          this.userId,
          year.toString(),
          month.toString().padStart(2, '0')
        );

        if (!fs.existsSync(monthDir)) continue;

        const files = fs.readdirSync(monthDir);
        for (const file of files) {
          if (!file.endsWith('.jsonl')) continue;

          const filePath = path.join(monthDir, file);
          const day = parseInt(file.replace('.jsonl', ''));
          const fileDate = new Date(year, month - 1, day);

          if (fileDate >= startDate && fileDate <= endDate) {
            try {
              const content = fs.readFileSync(filePath, 'utf-8');
              const lines = content.split('\n').filter(line => line.trim());

              for (const line of lines) {
                try {
                  const log = JSON.parse(line);
                  if (LogEntrySchema.safeParse(log).success) {
                    logs.push(log);
                  }
                } catch (e) {
                  console.error('Error parsing log line');
                }
              }
            } catch (err) {
              console.error(`Error reading log file ${filePath}:`);
            }
          }
        }
      }
    }

    return logs.sort((a, b) =>
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );
  }

  rotateLogs(keepDays: number = 30): void {
    try {
      const now = new Date();
      const cutoff = new Date(now);
      cutoff.setDate(now.getDate() - keepDays);

      const userDir = path.join(this.baseLogDir, this.userId);
      if (!fs.existsSync(userDir)) return;

      const years = fs.readdirSync(userDir);
      for (const year of years) {
        const yearPath = path.join(userDir, year);
        if (!fs.statSync(yearPath).isDirectory()) continue;

        const months = fs.readdirSync(yearPath);
        for (const month of months) {
          const monthPath = path.join(yearPath, month);
          if (!fs.statSync(monthPath).isDirectory()) continue;

          const days = fs.readdirSync(monthPath);
          for (const day of days) {
            if (!day.endsWith('.jsonl')) continue;

            const dayStr = day.replace('.jsonl', '');
            const fileDate = new Date(
              parseInt(year),
              parseInt(month) - 1,
              parseInt(dayStr)
            );

            if (fileDate < cutoff) {
              const filePath = path.join(monthPath, day);
              try {
                fs.unlinkSync(filePath);
              } catch (e) {
                console.error(`Error deleting log file ${filePath}:`);
              }
            }
          }

          try {
            if (fs.readdirSync(monthPath).length === 0) {
              fs.rmdirSync(monthPath);
            }
          } catch (e) {
            console.error(`Error cleaning empty month directory`);
          }
        }

        try {
          if (fs.existsSync(yearPath) && fs.readdirSync(yearPath).length === 0) {
            fs.rmdirSync(yearPath);
          }
        } catch (e) {
          console.error(`Error cleaning empty year directory`);
        }
      }
    } catch (error) {
      console.error('Error rotating logs:', error);
    }
  }
}
