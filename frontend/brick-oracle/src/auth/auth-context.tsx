import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { loginRequest, registerRequest } from './auth-api';
import {
	clearSession,
	getSessionToken,
	getStoredUser,
	setSession,
} from './storage';
import type { RouterAuthContext, User } from './types';
import { AuthReactContext } from './auth-react-context';

interface AuthProviderProps {
	children: ReactNode;
	onAuthChange: () => void;
}

export function AuthProvider({ children, onAuthChange }: AuthProviderProps) {
	const [user, setUser] = useState<User | null>(() => getStoredUser());

	const login = useCallback(
		async (email: string, password: string) => {
			const session = await loginRequest(email, password);
			setSession(session.token, session.user);
			setUser(session.user);
			onAuthChange();
		},
		[onAuthChange],
	);

	const register = useCallback(
		async (email: string, username: string, password: string) => {
			const session = await registerRequest(email, username, password);
			setSession(session.token, session.user);
			setUser(session.user);
			onAuthChange();
		},
		[onAuthChange],
	);

	const logout = useCallback(() => {
		clearSession();
		setUser(null);
		onAuthChange();
	}, [onAuthChange]);

	const value = useMemo<RouterAuthContext>(
		() => ({
			isAuthenticated: Boolean(user && getSessionToken()),
			user,
			login,
			logout,
			register,
		}),
		[user, login, logout, register],
	);

	return (
		<AuthReactContext.Provider value={value}>
			{children}
		</AuthReactContext.Provider>
	);
}
