import { useMemo, useState } from 'react';
import './sets-page.css';

type SortMode = 'featured' | 'year-desc' | 'pieces-desc' | 'name';

// Creates LEGO set object to mock data
interface LegoSet {
	id: string;
	name: string;
	theme: string;
	year: number;
	pieces: number;
}

// Build Mock sets
const MOCK_SETS: LegoSet[] = Array.from({ length: 30 }, (_, index) => {
	const themes = ['Architecture', 'Star Wars', 'Ideas', 'Icons', 'Creator Expert', 'Technic'] as const;
	const theme = themes[index % themes.length];
	const year = 2018 + (index % 8);
	const pieces = 300 + ((index + 1) * 125);

	return {
		id: `mock-${index + 1}`,
		name: `Mock Set ${index + 1}`,
		theme,
		year,
		pieces,
	};
});

// Themes will be built from the real data, Mock for now.
const THEMES = ['all', 'Architecture', 'Star Wars', 'Ideas', 'Icons', 'Creator Expert', 'Technic'] as const;
const DEFAULT_VISIBLE_COUNT = 25;
const LOAD_MORE_COUNT = 25;

export function SetsPage() {
	const [theme, setTheme] = useState<(typeof THEMES)[number]>('all');
	const [maxPieces, setMaxPieces] = useState('all');
	const [sortMode, setSortMode] = useState<SortMode>('featured');
	const [visibleCount, setVisibleCount] = useState(DEFAULT_VISIBLE_COUNT);

	const filteredSets = useMemo(() => {
		let nextSets = [...MOCK_SETS];

		if (theme !== 'all') {
			nextSets = nextSets.filter(set => set.theme === theme);
		}

		if (maxPieces !== 'all') {
			const limit = Number(maxPieces);
			nextSets = nextSets.filter(set => set.pieces <= limit);
		}

		switch (sortMode) {
			case 'year-desc':
				nextSets.sort((a, b) => b.year - a.year);
				break;
			case 'pieces-desc':
				nextSets.sort((a, b) => b.pieces - a.pieces);
				break;
			case 'name':
				nextSets.sort((a, b) => a.name.localeCompare(b.name));
				break;
			default:
				nextSets.sort((a, b) => a.name.localeCompare(b.name));
		}

		return nextSets;
	}, [maxPieces, sortMode, theme]);

	const visibleSets = filteredSets.slice(0, visibleCount);
	const hasMore = visibleCount < filteredSets.length;

	return (
		<main className='sets-browser-page'>
			<section className='sets-browser-hero'>
				<div>
					<h1>Browse LEGO sets</h1>
					<p className='sets-browser-copy'>Explore a simple mock catalog of LEGO sets.</p>
				</div>
			</section>

			
			<section className='sets-browser-filters' aria-label='Set filters'>
				<label className='filter-field'>
					<span>Theme</span>
					<select value={theme} onChange={e => setTheme(e.target.value as (typeof THEMES)[number])}>
						{THEMES.map(option => (
							<option key={option} value={option}>
								{option === 'all' ? 'All themes' : option}
							</option>
						))}
					</select>
				</label>

				<label className='filter-field'>
					<span>Max pieces</span>
					<select value={maxPieces} onChange={e => setMaxPieces(e.target.value)}>
						<option value='all'>Any size</option>
						<option value='1000'>Up to 1,000</option>
						<option value='3000'>Up to 3,000</option>
						<option value='5000'>Up to 5,000</option>
					</select>
				</label>

				<label className='filter-field'>
					<span>Sort</span>
					<select value={sortMode} onChange={e => setSortMode(e.target.value as SortMode)}>
						<option value='featured'>Featured</option>
						<option value='year-desc'>Newest first</option>
						<option value='pieces-desc'>Most pieces</option>
						<option value='name'>Name A-Z</option>
					</select>
				</label>
			</section>

			<section className='sets-grid-panel'>
				<div className='sets-grid' role='list'>
					{visibleSets.map(set => (
						<article className='set-card' role='listitem' key={set.id}>
							<div className='set-card-image' />
							<div className='set-card-body'>
								<p className='set-card-theme'>{set.theme}</p>
								<h2 className='set-card-name'>{set.name}</h2>
								<div className='set-card-meta'>
									<span>{set.year}</span>
									<span>{set.pieces.toLocaleString()} pcs</span>
								</div>
							</div>
						</article>
					))}
				</div>

				{filteredSets.length === 0 && (
					<p className='sets-empty-state'>No sets match the selected filters yet.</p>
				)}

				{hasMore && (
					<button
						className='load-more-btn'
						type='button'
						onClick={() => setVisibleCount(count => count + LOAD_MORE_COUNT)}
					>
						Load more
					</button>
				)}
			</section>
		</main>
	);
}
