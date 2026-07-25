import { useState, useRef, useEffect } from 'react';
import { Link, Outlet, useRouterState } from '@tanstack/react-router';
import { useAuth } from '../auth/use-auth';
import './site-layout.css';

type SearchTarget = 'sets' | 'bricks';

interface SearchResult {
	id: string;
	title: string;
	subtitle: string;
}

const MOCK_SETS: SearchResult[] = [
	{ id: '75192-1', title: 'Millennium Falcon', subtitle: '75192-1' },
	{ id: '10300-1', title: 'Back to the Future Time Machine', subtitle: '10300-1' },
	{ id: '21325-1', title: 'Medieval Blacksmith', subtitle: '21325-1' },
	{ id: '75313-1', title: 'AT-AT', subtitle: '75313-1' },
	{ id: '10281-1', title: 'Bonsai Tree', subtitle: '10281-1' },
	{ id: '71374-1', title: 'Nintendo Entertainment System', subtitle: '71374-1' },
];

const MOCK_BRICKS: SearchResult[] = [
	{ id: '3001', title: 'Brick 2x4', subtitle: '3001' },
	{ id: '3003', title: 'Brick 2x2', subtitle: '3003' },
	{ id: '3004', title: 'Brick 1x2', subtitle: '3004' },
	{ id: '3005', title: 'Brick 1x1', subtitle: '3005' },
	{ id: '3010', title: 'Brick 1x4', subtitle: '3010' },
];

function searchMock(query: string, target: SearchTarget): SearchResult[] {
	if (!query.trim()) return [];
	const pool = target === 'sets' ? MOCK_SETS : MOCK_BRICKS;
	return pool.filter(r =>
		r.title.toLowerCase().includes(query.toLowerCase()) ||
		r.subtitle.toLowerCase().includes(query.toLowerCase())
	);
}

export function SiteLayout() {
	const pathname = useRouterState({ select: state => state.location.pathname });
	const isAuthRoute = pathname.startsWith('/auth');
	const { isAuthenticated, user, logout } = useAuth();

	const [query, setQuery] = useState('');
	const [target, setTarget] = useState<SearchTarget>('sets');
	const [results, setResults] = useState<SearchResult[]>([]);
	const [open, setOpen] = useState(false);
	const searchRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		setResults(searchMock(query, target));
		setOpen(query.trim().length > 0);
	}, [query, target]);

	useEffect(() => {
		function handleClickOutside(e: MouseEvent) {
			if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
				setOpen(false);
			}
		}
		document.addEventListener('mousedown', handleClickOutside);
		return () => document.removeEventListener('mousedown', handleClickOutside);
	}, []);

	if (isAuthRoute) {
		return <Outlet />;
	}

	return (
		<>
			<header className='site-header'>
				<div className='header-top'>
					<Link
						to='/'
						className='header-logo'>
						Brick Oracle
					</Link>

					<div
						className='search-wrap'
						ref={searchRef}>
						<div className='search-bar'>
							<input
								className='search-input'
								type='text'
								placeholder='Search...'
								value={query}
								onChange={e => setQuery(e.target.value)}
								onFocus={() => query.trim() && setOpen(true)}
							/>
							<button
								className='search-icon-btn'
								type='button'
								onClick={() => setOpen(o => !o)}>
								🔍
							</button>
							<button
								className='search-target-btn'
								type='button'
								onClick={() => setTarget(t => (t === 'sets' ? 'bricks' : 'sets'))}>
								{target === 'sets' ? 'Sets' : 'Bricks'}
							</button>
						</div>

						{open && (
							<ul className='search-dropdown'>
								{results.length > 0 ? (
									results.map(r => (
										<li
											key={r.id}
											className='search-result-item'>
											<div className='search-result-thumb' />
											<div>
												<p className='search-result-title'>{r.title}</p>
												<p className='search-result-sub'>{r.subtitle}</p>
											</div>
										</li>
									))
								) : (
									<li className='search-result-empty'>No results</li>
								)}
							</ul>
						)}
					</div>

					<div className='header-user'>
						<span className='header-avatar'>☺</span>
						{isAuthenticated ? (
							<>
								<span className='header-username'>{user?.username}</span>
								<button
									type='button'
									className='header-btn'
									onClick={() => logout()}>
									Log out
								</button>
							</>
						) : (
							<Link
								search={{}}
								to='/auth'
								className='header-btn'>
								Login
							</Link>
						)}
					</div>
				</div>

				<nav className='header-nav'>
					<Link to='/'>Home</Link>
					<Link to='/collection'>My Collection</Link>
					<Link to='/sets'>Browse Sets</Link>
				</nav>
			</header>

			<Outlet />
			<footer className='site-footer'>Brick Oracle</footer>
		</>
	);
}
