import { useState, useEffect } from 'react';
import { Link } from '@tanstack/react-router';
import { useAuth } from '../auth/use-auth';
import type { SetDTO } from '../types/set';
import './index-page.css';

const MOCK_TOTAL_SETS = 22_017;
const MOCK_BRICKS_IN_COLLECTION = 1_243;
const MOCK_SETS_BUILDABLE = 12;
const PAGE_SIZE = 4;

export function IndexPage() {
	const { isAuthenticated } = useAuth();
	const [sets, setSets] = useState<SetDTO[]>([]);
	const [start, setStart] = useState(0);

	useEffect(() => {
		fetch('/api/sets/?page=1&page_size=12')
			.then(r => r.json())
			.then((data: SetDTO[]) => setSets(data))
			.catch(() => setSets([]));
	}, []);

	const visible = sets.slice(start, start + PAGE_SIZE);
	const canLeft = start > 0;
	const canRight = start + PAGE_SIZE < sets.length;

	return (
		<main className='index-page'>
			<section className='stat-cards'>
				<div className='stat-card'>
					<span className='stat-label'>Total Sets in Database</span>
					<span className='stat-value'>{MOCK_TOTAL_SETS.toLocaleString()}</span>
				</div>
				<div className='stat-card'>
					<span className='stat-label'>Bricks in Collection</span>
					<span className='stat-value'>
						{isAuthenticated ? MOCK_BRICKS_IN_COLLECTION.toLocaleString() : 'N/A'}
					</span>
				</div>
				<div className='stat-card'>
					<span className='stat-label'>Sets You Can Build</span>
					<span className='stat-value'>
						{isAuthenticated ? MOCK_SETS_BUILDABLE : 'N/A'}
					</span>
				</div>
			</section>

			<section className='carousel-section'>
				<h2>Sets</h2>
				<div className='carousel'>
					<button
						className='carousel-btn'
						disabled={!canLeft}
						onClick={() => setStart(s => Math.max(0, s - PAGE_SIZE))}>
						&#8249;
					</button>
					<div className='carousel-track'>
						{visible.map(set => (
							<Link
								key={set.set_num}
								to='/sets/$id'
								params={{ id: set.set_num }}
								className='set-card'>
								{set.img_url ? (
									<img
										className='set-card-img'
										src={set.img_url}
										alt={set.name}
									/>
								) : (
									<div className='set-card-img' />
								)}
								<p className='set-card-name'>{set.name}</p>
								<p className='set-card-year'>{set.year ?? '—'}</p>
							</Link>
						))}
					</div>
					<button
						className='carousel-btn'
						disabled={!canRight}
						onClick={() => setStart(s => Math.min(sets.length - PAGE_SIZE, s + PAGE_SIZE))}>
						&#8250;
					</button>
				</div>
			</section>
		</main>
	);
}
