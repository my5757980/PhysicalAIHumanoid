/**
 * Chat API configuration.
 *
 * In development (localhost): points to local FastAPI server
 * In production: points to Railway-deployed backend
 *
 * Override via CHAT_API_BASE environment variable or docusaurus.config.ts customFields.
 */
export const CHAT_API_BASE = 'https://physicalaihumanoid-production.up.railway.app';
