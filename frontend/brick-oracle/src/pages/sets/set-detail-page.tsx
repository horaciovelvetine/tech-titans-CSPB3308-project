import { useState, useEffect } from 'react';
import { getRouteApi } from '@tanstack/react-router';
import './set-detail-page.css';

const routeApi = getRouteApi('/sets/$id');

type Filter = 'all' | 'missing' | 'owned';

interface SetDTO {
	set_num: string;
	name: string;
	year: number | null;
	num_parts: number | null;
}

interface BrickDiffDTO {
	part_num: string;
	name: string;
	color_name: string;
	required_qty: number;
	owned_qty: number;
	img_url: string | null;
}

// TODO: replace with GET /api/sets/:id/diff?collection_id= once BE endpoint is ready
const MOCK_DIFF: BrickDiffDTO[] = [
	{ part_num: '3001', name: 'Brick 2x4', color_name: 'Red', required_qty: 4, owned_qty: 2, img_url: null },
	{ part_num: '3003', name: 'Brick 2x2', color_name: 'Blue', required_qty: 6, owned_qty: 6, img_url: null },
	{ part_num: '3004', name: 'Brick 1x2', color_name: 'White', required_qty: 8, owned_qty: 0, img_url: null },
	{ part_num: '3005', name: 'Brick 1x1', color_name: 'Black', required_qty: 12, owned_qty: 5, img_url: null },
	{ part_num: '3010', name: 'Brick 1x4', color_name: 'Yellow', required_qty: 3, owned_qty: 3, img_url: null },
	{ part_num: '3022', name: 'Plate 2x2', color_name: 'Green', required_qty: 5, owned_qty: 1, img_url: null },
	{ part_num: '3023', name: 'Plate 1x2', color_name: 'Red', required_qty: 10, owned_qty: 0, img_url: null },
	{ part_num: '3024', name: 'Plate 1x1', color_name: 'Blue', required_qty: 7, owned_qty: 7, img_url: null },
];

export function SetDetailPage() {
	const { id } = routeApi.useParams();
	const [set, setSet] = useState<SetDTO | null>(null);
	const [filter, setFilter] = useState<Filter>('all');

	useEffect(() => {
		fetch(`/api/sets/${id}`)
			.then(r => r.json())
			.then((data: SetDTO) => setSet(data))
			.catch(() => {});
	}, [id]);

	const filtered = MOCK_DIFF.filter(b => {
		if (filter === 'missing') return b.owned_qty < b.required_qty;
		if (filter === 'owned') return b.owned_qty >= b.required_qty;
		return true;
	});

	return (
		<main className='set-detail-page'>
			<div className='set-detail-header'>
				<h1>{set?.name ?? id}</h1>
				<div className='diff-filter'>
					{(['all', 'missing', 'owned'] as Filter[]).map(f => (
						<button
							key={f}
							className={`diff-filter-btn${filter === f ? ' active' : ''}`}
							onClick={() => setFilter(f)}>
							{f.charAt(0).toUpperCase() + f.slice(1)}
						</button>
					))}
				</div>
			</div>

			<div className='brick-grid'>
				{filtered.map(brick => {
					const status =
						brick.owned_qty >= brick.required_qty ? 'owned'
						: brick.owned_qty === 0 ? 'missing'
						: 'partial';
					return (
						<div
							key={`${brick.part_num}-${brick.color_name}`}
							className={`brick-card ${status}`}>
							{brick.img_url ? (
								<img
									className='brick-card-img'
									src={brick.img_url}
									alt={brick.name}
								/>
							) : (
								<div className='brick-card-img' />
							)}
							<p className='brick-card-name'>{brick.name}</p>
							<p className='brick-card-color'>{brick.color_name}</p>
							<p className='brick-card-qty'>{brick.owned_qty} / {brick.required_qty}</p>
						</div>
					);
				})}
			</div>
		</main>
	);
}
