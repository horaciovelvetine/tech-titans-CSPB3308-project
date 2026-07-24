// Root route: wraps every page in SiteLayout (header, nav, footer). Child routes render in <Outlet />.
import { createRootRouteWithContext } from '@tanstack/react-router';
import type { RouterAuthContext } from '../auth/types';
import { SiteLayout } from '../pages/site-layout';

export const Route = createRootRouteWithContext<{ auth: RouterAuthContext }>()({
	component: SiteLayout,
});
