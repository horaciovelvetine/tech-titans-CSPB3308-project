import { Link, Outlet } from '@tanstack/react-router';

export function AuthLayout() {
	return (
		<main className='auth-layout'>
			<div className='auth-card'>
				<Link
					className='auth-brand'
					to='/'>
					Brick Oracle
				</Link>
				<Outlet />
			</div>
		</main>
	);
}
