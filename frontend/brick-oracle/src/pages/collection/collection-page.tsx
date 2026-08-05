import { useState } from 'react';
import type { CollectionPartDTO } from '../../types/collection-part';
import { AddPartModal } from './add-part-modal';
import './collection-page.css';

const MOCK_PARTS: CollectionPartDTO[] = [
	{ id: '1', part_num: '3001', name: 'Brick 2 x 4', color_name: 'Red', quantity: 24 },
	{ id: '2', part_num: '3003', name: 'Brick 2 x 2', color_name: 'Blue', quantity: 8 },
	{ id: '3', part_num: '3020', name: 'Plate 2 x 4', color_name: 'Yellow', quantity: 16 },
];

export function CollectionPage() {
	const [parts, setParts] = useState<CollectionPartDTO[]>(MOCK_PARTS);
	const [selected, setSelected] = useState<Set<string>>(new Set());
	const [isAddOpen, setIsAddOpen] = useState(false);

	const hasSelection = selected.size > 0;

	function toggleSelected(id: string) {
		setSelected(prev => {
			const next = new Set(prev);
			if (next.has(id)) {
				next.delete(id);
			} else {
				next.add(id);
			}
			return next;
		});
	}

	function onAddClick() {
		setIsAddOpen(true);
	}

	function handleAddPart(part: Omit<CollectionPartDTO, 'id'>) {
		setParts(prev => [...prev, { ...part, id: crypto.randomUUID() }]);
		setIsAddOpen(false);
	}

	return (
		<main className='collection-page'>
			<div className='collection-toolbar'>
				<button className='toolbar-btn'>Upload</button>
				<button className='toolbar-btn' onClick={onAddClick}>
					Add
				</button>
				<button className='toolbar-btn' disabled={!hasSelection}>
					Edit
				</button>
				<button className='toolbar-btn' disabled={!hasSelection}>
					Delete
				</button>
			</div>

			<table className='collection-table'>
				<thead>
					<tr>
						<th className='select-col' />
						<th>Bricks</th>
						<th>Quantity</th>
						<th>Part ID</th>
						<th>Color</th>
					</tr>
				</thead>
				<tbody>
					{parts.map(part => (
						<tr key={part.id}>
							<td className='select-col'>
								<input
									type='checkbox'
									checked={selected.has(part.id)}
									onChange={() => toggleSelected(part.id)}
								/>
							</td>
							<td>{part.name}</td>
							<td>{part.quantity}</td>
							<td>{part.part_num}</td>
							<td>{part.color_name}</td>
						</tr>
					))}
				</tbody>
			</table>

			<AddPartModal isOpen={isAddOpen} onClose={() => setIsAddOpen(false)} onAdd={handleAddPart} />
		</main>
	);
}
