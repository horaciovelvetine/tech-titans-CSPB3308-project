import { Link, Outlet, useRouterState } from '@tanstack/react-router';
import { useAuth } from '../auth/use-auth';


export function SiteLayout() {
	const pathname = useRouterState({ select: state => state.location.pathname });
	const isAuthRoute = pathname.startsWith('/auth');
	const { isAuthenticated, user, logout } = useAuth();

	if (isAuthRoute) {
		return <Outlet />;
	}

	return (
		<>
			<header>
				<Link to='/'>Brick Oracle!</Link>
				<nav>
					<Link to='/sets'>Sets</Link>
					<Link to='/collection'>Collection</Link>
					{isAuthenticated ?
						<>
							<span>{user?.username}</span>
							<button
								type='button'
								onClick={() => logout()}>
								Log out
							</button>
						</>
					:	<Link
							search={{}}
							to='/auth'>
							Log in
						</Link>
					}
				</nav>
			</header>
			<Outlet />
			<footer>Footer!</footer>
		</>
	);
}
