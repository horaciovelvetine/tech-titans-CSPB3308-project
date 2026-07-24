// Route guard: use as beforeLoad on protected routes. Redirects unauthenticated users to login.
import { redirect } from '@tanstack/react-router';
import type { ParsedLocation } from '@tanstack/react-router';
import type { RouterAuthContext } from './types';

export function requireAuth({
	context,
	location,
}: {
	context: { auth: RouterAuthContext };
	location: ParsedLocation;
}) {
	if (!context.auth.isAuthenticated) {
		throw redirect({
			to: '/auth',
			search: {
				redirect: location.href,
			},
		});
	}
}
