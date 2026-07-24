import type { User } from './types';

const TOKEN_KEY = 'brick-oracle:session-token';
const USER_KEY = 'brick-oracle:user';

export function getSessionToken(): string | null {
	return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser(): User | null {
	const raw = localStorage.getItem(USER_KEY);
	if (!raw) return null;

	try {
		return JSON.parse(raw) as User;
	} catch {
		return null;
	}
}

export function setSession(token: string, user: User): void {
	localStorage.setItem(TOKEN_KEY, token);
	localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearSession(): void {
	localStorage.removeItem(TOKEN_KEY);
	localStorage.removeItem(USER_KEY);
}
