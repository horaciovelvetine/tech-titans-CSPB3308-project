import { useState } from 'react';
import { useAuth } from '../auth/use-auth';
import './index-page.css';

const MOCK_TOTAL_SETS = 22_017;
const MOCK_BRICKS_IN_COLLECTION = 1_243;
const MOCK_SETS_BUILDABLE = 12;

const MOCK_SETS = [
	{ id: '75192-1', name: 'Millennium Falcon', year: 2017 },
	{ id: '10300-1', name: 'Back to the Future Time Machine', year: 2022 },
	{ id: '21325-1', name: 'Medieval Blacksmith', year: 2021 },
	{ id: '75313-1', name: 'AT-AT', year: 2021 },
	{ id: '10281-1', name: 'Bonsai Tree', year: 2021 },
	{ id: '10290-1', name: 'Pickup Truck', year: 2022 },
	{ id: '71374-1', name: 'Nintendo Entertainment System', year: 2020 },
	{ id: '42099-1', name: 'RC Tracked Racer', year: 2019 },
];

const PAGE_SIZE = 4;

export function IndexPage() {
	const { isAuthenticated } = useAuth();
	const [start, setStart] = useState(0);

	const visible = MOCK_SETS.slice(start, start + PAGE_SIZE);
	const canLeft = start > 0;
	const canRight = start + PAGE_SIZE < MOCK_SETS.length;

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
						onClick={() => setStart(s => Math.max(0, s - PAGE_SIZE))}
					>
						&#8249;
					</button>
					<div className='carousel-track'>
						{visible.map(set => (
							<div
								key={set.id}
								className='set-card'>
								<div className='set-card-img' />
								<p className='set-card-name'>{set.name}</p>
								<p className='set-card-year'>{set.year}</p>
							</div>
						))}
					</div>
					<button
						className='carousel-btn'
						disabled={!canRight}
						onClick={() => setStart(s => Math.min(MOCK_SETS.length - PAGE_SIZE, s + PAGE_SIZE))}
					>
						&#8250;
					</button>
				</div>
			</section>
		</main>
	);
}
