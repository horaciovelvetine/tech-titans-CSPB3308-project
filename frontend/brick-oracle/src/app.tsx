// App root: AuthProvider holds session state, RouterShell passes it into TanStack Router.
// When auth changes, router.invalidate() re-runs route guards (e.g. requireAuth).
import { RouterProvider } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools';
import { AuthProvider } from './auth/auth-context';
import { router } from './router';
import { useAuth } from './auth/use-auth';

function RouterShell() {
	const auth = useAuth();

	return (
		<>
			<RouterProvider
				context={{ auth }}
				router={router}
			/>
			{import.meta.env.DEV ?
				<TanStackRouterDevtools
					initialIsOpen={false}
					router={router}
				/>
			:	null}
		</>
	);
}

export function App() {
	return (
		<AuthProvider onAuthChange={() => router.invalidate()}>
			<RouterShell />
		</AuthProvider>
	);
}
