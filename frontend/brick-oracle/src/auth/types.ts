export interface User {
	id: string;
	username: string;
	email: string;
}

export interface AuthSession {
	token: string;
	user: User;
}

export interface RouterAuthContext {
	isAuthenticated: boolean;
	user: User | null;
	login: (email: string, password: string) => Promise<void>;
	logout: () => void;
	register: (
		email: string,
		username: string,
		password: string,
	) => Promise<void>;
}

export interface AuthSearch {
	redirect?: string;
}
