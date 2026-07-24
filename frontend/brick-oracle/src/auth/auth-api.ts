import type { AuthSession } from './types';

export async function loginRequest(
	email: string,
	password: string,
): Promise<AuthSession> {
	const response = await fetch('/api/auth/login', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password }),
	});

	if (!response.ok) {
		throw new Error('Sign in failed. Check your email and password.');
	}

	return response.json() as Promise<AuthSession>;
}

export async function registerRequest(
	email: string,
	username: string,
	password: string,
): Promise<AuthSession> {
	const response = await fetch('/api/auth/register', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, username, password }),
	});

	if (!response.ok) {
		throw new Error('Registration failed. Please try again.');
	}

	return response.json() as Promise<AuthSession>;
}
