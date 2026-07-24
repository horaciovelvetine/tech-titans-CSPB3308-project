import { createFileRoute, redirect } from '@tanstack/react-router';
import { AuthLayout } from '../../pages/auth/auth-layout';
import type { AuthSearch } from '../../auth/types';

function parseAuthSearch(search: Record<string, unknown>): AuthSearch {
	return {
		redirect: typeof search.redirect === 'string' ? search.redirect : undefined,
	};
}

export const Route = createFileRoute('/auth')({
	validateSearch: parseAuthSearch,
	beforeLoad: ({ context, search }) => {
		if (context.auth.isAuthenticated) {
			throw redirect({ to: search.redirect ?? '/collection' });
		}
	},
	component: AuthLayout,
});
