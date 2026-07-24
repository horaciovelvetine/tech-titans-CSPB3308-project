import { useContext } from "react";
import type { RouterAuthContext } from "./types";
import { AuthReactContext } from "./auth-react-context";

export function useAuth(): RouterAuthContext {
	const context = useContext(AuthReactContext);
	if (!context) {
		throw new Error('useAuth must be used within AuthProvider');
	}

	return context;
}
