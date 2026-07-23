// Creates the router from the auto-generated route tree (see routes/ and routeTree.gen.ts).
// context.auth is filled in at runtime by App; the Register block enables typed route links.
import { createRouter } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen';

export const router = createRouter({
	routeTree,
	context: {
		auth: undefined!,
	},
});

declare module '@tanstack/react-router' {
	interface Register {
		router: typeof router;
	}
}
