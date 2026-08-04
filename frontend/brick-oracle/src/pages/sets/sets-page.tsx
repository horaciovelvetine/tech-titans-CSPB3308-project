import { useEffect, useState } from 'react';
import { Link } from '@tanstack/react-router';
import './sets-page.css';

// These values are passed straight through to the API's `sort` parameter.
type SortMode = 'name' | 'year-desc' | 'pieces-desc';

type ThemeOption = {
	id: number;
	name: string;
};

type LegoSet = {
	set_num: string;
	name: string | null;
	year: number | null;
	num_parts: number | null;
	img_url: string | null;
};

const PAGE_SIZE = 25;

export function SetsPage() {
	const [theme, setTheme] = useState('all');
	const [themes, setThemes] = useState<ThemeOption[]>([]);
	const [sets, setSets] = useState<LegoSet[]>([]);
	const [maxPieces, setMaxPieces] = useState('all');
	const [sortMode, setSortMode] = useState<SortMode>('name');
	const [page, setPage] = useState(1);
	const [hasMore, setHasMore] = useState(false);
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		fetch('/api/sets/themes')
			.then(r => (r.ok ? r.json() : []))
			.then((data: ThemeOption[]) => setThemes(data))
			.catch(() => setThemes([]));
	}, []);

	useEffect(() => {
		const controller = new AbortController();
		const query = new URLSearchParams({ page: String(page), page_size: String(PAGE_SIZE) });
		if (theme !== 'all') {
			query.set('theme', theme);
		}
		if (maxPieces !== 'all') {
			query.set('max_parts', maxPieces);
		}
		query.set('sort', sortMode);

		setIsLoading(true);
		fetch(`/api/sets/?${query.toString()}`, { signal: controller.signal })
			.then(r => (r.ok ? r.json() : []))
			.then((data: LegoSet[]) => {
				// Page 1 replaces the list (filters or sort changed); later pages append.
				setSets(prev => (page === 1 ? data : [...prev, ...data]));
				// The API returns a bare array with no total, so a short page means the end.
				setHasMore(data.length === PAGE_SIZE);
				setIsLoading(false);
			})
			.catch(() => {
				if (controller.signal.aborted) {
					return;
				}
				setHasMore(false);
				setIsLoading(false);
			});

		return () => controller.abort();
	}, [theme, maxPieces, sortMode, page]);

	// Filters and sorting both change which sets land on which page, so any
	// change to them restarts paging from the top.
	const resetPaging = () => {
		setSets([]);
		setPage(1);
	};

	// Handles changes to the theme filter
	const handleThemeChange = (nextTheme: string) => {
		setTheme(nextTheme);
		resetPaging();
	};

	// Handles changes to the max pieces filter
	const handleMaxPiecesChange = (nextMaxPieces: string) => {
		setMaxPieces(nextMaxPieces);
		resetPaging();
	};

	// Handles changes to the sort mode
	const handleSortChange = (nextSortMode: SortMode) => {
		setSortMode(nextSortMode);
		resetPaging();
	};

	return (
		<main className='sets-browser-page'>
			<section className='sets-browser-hero'>
				<div>
					<h1>Browse LEGO sets</h1>
					<p className='sets-browser-copy'>Explore a catalog of LEGO sets and figures.</p>
				</div>
			</section>

			<section className='sets-browser-filters' aria-label='Set filters'>
				<label className='filter-field'>
					<span>Theme</span>
					<select value={theme} onChange={e => handleThemeChange(e.target.value)}>
						<option value='all'>All themes</option>
						{themes.map(option => (
							<option key={option.id} value={option.name}>
								{option.name}
							</option>
						))}
					</select>
				</label>

				<label className='filter-field'>
					<span>Max pieces</span>
					<select value={maxPieces} onChange={e => handleMaxPiecesChange(e.target.value)}>
						<option value='all'>Any size</option>
						<option value='1000'>Up to 1,000</option>
						<option value='3000'>Up to 3,000</option>
						<option value='5000'>Up to 5,000</option>
					</select>
				</label>

				<label className='filter-field'>
					<span>Sort</span>
					<select value={sortMode} onChange={e => handleSortChange(e.target.value as SortMode)}>
						<option value='name'>Name A-Z</option>
						<option value='year-desc'>Newest first</option>
						<option value='pieces-desc'>Most pieces</option>
					</select>
				</label>
			</section>

			<section className='sets-grid-panel'>
				<div className='sets-grid' role='list'>
					{sets.map(set => (
						<article className='set-card' role='listitem' key={set.set_num}>
							{/* The link sits inside the article so the card keeps its listitem
							    role and the anchor keeps its link role. */}
							<Link className='set-card-link' to='/sets/$id' params={{ id: set.set_num }}>
								{set.img_url ? (
									<img className='set-card-image' src={set.img_url} alt={set.name ?? 'LEGO set image'} />
								) : (
									<div className='set-card-image' />
								)}
								<div className='set-card-body'>
									<p className='set-card-theme'>{theme === 'all' ? 'All themes' : theme}</p>
									<h2 className='set-card-name'>{set.name ?? 'Unknown set'}</h2>
									<div className='set-card-meta'>
										<span>{set.year ?? '—'}</span>
										<span>{(set.num_parts ?? 0).toLocaleString()} pcs</span>
									</div>
								</div>
							</Link>
						</article>
					))}
				</div>

				{hasMore && (
					<button
						className='load-more-btn'
						type='button'
						disabled={isLoading}
						onClick={() => setPage(current => current + 1)}
					>
						{isLoading ? 'Loading…' : 'Load more'}
					</button>
				)}
			</section>
		</main>
	);
}
