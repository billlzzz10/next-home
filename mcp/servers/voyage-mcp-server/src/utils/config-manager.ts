import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { AppConfig, ConfigSchema } from '../types.js';

export class ConfigManager {
  private configPath: string;
  private config: AppConfig;
  private envPrefix: string = 'MCP_';

  constructor(configPath: string = 'config/default.yaml') {
    this.configPath = configPath;
    this.config = this.loadConfig();
  }

  private loadConfig(): AppConfig {
    let configData: any = {};

    if (fs.existsSync(this.configPath)) {
      try {
        const ext = path.extname(this.configPath).toLowerCase();
        const fileContent = fs.readFileSync(this.configPath, 'utf-8');

        if (ext === '.json') {
          configData = JSON.parse(fileContent);
        } else if (ext === '.yaml' || ext === '.yml') {
          configData = yaml.load(fileContent) as any;
        }
      } catch (error) {
        console.error(`Error loading config file ${this.configPath}:`, error);
      }
    }

    const envConfig = this.loadFromEnv();
    const mergedConfig = this.mergeDeep(configData, envConfig);

    return ConfigSchema.parse(mergedConfig);
  }

  private loadFromEnv(): any {
    const envConfig: any = {};

    for (const [key, value] of Object.entries(process.env)) {
      if (key.startsWith(this.envPrefix)) {
        const cleanKey = key.substring(this.envPrefix.length);
        this.setNestedProperty(envConfig, cleanKey, this.parseEnvValue(value));
      }
    }

    return envConfig;
  }

  private parseEnvValue(value: string | undefined): any {
    if (!value) return undefined;
    try {
      return JSON.parse(value);
    } catch {
      if (value.toLowerCase() === 'true') return true;
      if (value.toLowerCase() === 'false') return false;
      if (!isNaN(Number(value))) return Number(value);
      return value;
    }
  }

  private setNestedProperty(obj: any, path: string, value: any): void {
    const keys = path.split('__');
    let current = obj;

    for (let i = 0; i < keys.length - 1; i++) {
      const key = keys[i];
      if (!current[key]) current[key] = {};
      current = current[key];
    }

    current[keys[keys.length - 1]] = value;
  }

  private mergeDeep(target: any, source: any): any {
    const output = { ...target };

    if (typeof target !== 'object' || typeof source !== 'object') {
      return source;
    }

    Object.keys(source).forEach(key => {
      if (
        typeof source[key] === 'object' &&
        source[key] !== null &&
        target[key] &&
        typeof target[key] === 'object'
      ) {
        output[key] = this.mergeDeep(target[key], source[key]);
      } else {
        output[key] = source[key];
      }
    });

    return output;
  }

  get<T>(path: string): T {
    return this.resolvePath(this.config, path) as T;
  }

  getAll(): AppConfig {
    return this.config;
  }

  update(updates: Partial<AppConfig>): AppConfig {
    const newConfig = this.mergeDeep(this.config, updates);
    this.config = ConfigSchema.parse(newConfig);
    return this.config;
  }

  private resolvePath(obj: any, path: string): any {
    return path.split('.').reduce((acc, part) => acc?.[part], obj);
  }
}
