import { type FormEvent, useState } from 'react';
import { Link, getRouteApi, useNavigate } from '@tanstack/react-router';
import { useAuth } from '../../auth/use-auth';

const routeApi = getRouteApi('/auth/register');

export function RegisterPage() {
	const { redirect } = routeApi.useSearch();
	const navigate = useNavigate();
	const { register } = useAuth();
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	async function handleSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault();
		setError(null);
		setIsSubmitting(true);

		try {
			await register(email, username, password);
			await navigate({ to: redirect ?? '/collection' });
		} catch (submitError) {
			setError(
				submitError instanceof Error ?
					submitError.message
				:	'Registration failed.',
			);
		} finally {
			setIsSubmitting(false);
		}
	}

	return (
		<section className='auth-panel'>
			<h1>Create account</h1>
			<p className='auth-lead'>
				Register to save sets and track your collection.
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
					Username
					<input
						autoComplete='username'
						name='username'
						required
						type='text'
						value={username}
						onChange={event => setUsername(event.target.value)}
					/>
				</label>

				<label>
					Password
					<input
						autoComplete='new-password'
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
					{isSubmitting ? 'Creating account…' : 'Create account'}
				</button>
			</form>

			<p className='auth-switch'>
				Already have an account?{' '}
				<Link
					to='/auth'
					search={{ redirect }}>
					Sign in
				</Link>
			</p>
		</section>
	);
}
