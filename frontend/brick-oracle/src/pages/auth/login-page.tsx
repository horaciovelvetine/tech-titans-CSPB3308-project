import { type FormEvent, useState } from 'react';
import { Link, getRouteApi, useNavigate } from '@tanstack/react-router';
import { useAuth } from '../../auth/use-auth';

const routeApi = getRouteApi('/auth/');

export function LoginPage() {
	const { redirect } = routeApi.useSearch();
	const navigate = useNavigate();
	const { login } = useAuth();
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	async function handleSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault();
		setError(null);
		setIsSubmitting(true);

		try {
			await login(email, password);
			await navigate({ to: redirect ?? '/collection' });
		} catch (submitError) {
			setError(
				submitError instanceof Error ? submitError.message : 'Sign in failed.',
			);
		} finally {
			setIsSubmitting(false);
		}
	}

	return (
		<section className='auth-panel'>
			<h1>Sign in</h1>
			<p className='auth-lead'>
				Welcome back. Sign in to manage your collection.
			</p>

			<form
				className='auth-form'
				onSubmit={handleSubmit}>
				<label>
					Email
					<input
						autoComplete='email'
						name='email'
						required
						type='email'
						value={email}
						onChange={event => setEmail(event.target.value)}
					/>
				</label>

				<label>
					Password
					<input
						autoComplete='current-password'
						name='password'
						required
						type='password'
						value={password}
						onChange={event => setPassword(event.target.value)}
					/>
				</label>

				{error ?
					<p className='auth-error'>{error}</p>
				:	null}

				<button
					disabled={isSubmitting}
					type='submit'>
					{isSubmitting ? 'Signing in…' : 'Sign in'}
				</button>
			</form>

			<p className='auth-switch'>
				Need an account?{' '}
				<Link
					to='/auth/register'
					search={{ redirect }}>
					Create one
				</Link>
			</p>
		</section>
	);
}
