import { useState } from 'react';
import type { FormEvent } from 'react';
import { Modal } from '../../components/modal/modal';
import type { CollectionPartDTO } from '../../types/collection-part';
import './add-part-modal.css';

interface AddPartModalProps {
	isOpen: boolean;
	onClose: () => void;
	onAdd: (part: Omit<CollectionPartDTO, 'id'>) => void;
}

interface CatalogPart {
	part_num: string;
	name: string;
	color_name: string;
}

// TODO: replace with a catalog search API call (GET /api/parts?q=...)
const MOCK_CATALOG: CatalogPart[] = [
	{ part_num: '3001', name: 'Brick 2 x 4', color_name: 'Red' },
	{ part_num: '3001', name: 'Brick 2 x 4', color_name: 'Blue' },
	{ part_num: '3001', name: 'Brick 2 x 4', color_name: 'White' },
	{ part_num: '3002', name: 'Brick 2 x 3', color_name: 'Red' },
	{ part_num: '3003', name: 'Brick 2 x 2', color_name: 'Blue' },
	{ part_num: '3004', name: 'Brick 1 x 2', color_name: 'Yellow' },
	{ part_num: '3005', name: 'Brick 1 x 1', color_name: 'Black' },
	{ part_num: '3020', name: 'Plate 2 x 4', color_name: 'Yellow' },
	{ part_num: '3021', name: 'Plate 2 x 3', color_name: 'White' },
	{ part_num: '3022', name: 'Plate 2 x 2', color_name: 'Black' },
	{ part_num: '3023', name: 'Plate 1 x 2', color_name: 'Red' },
	{ part_num: '3024', name: 'Plate 1 x 1', color_name: 'Blue' },
];

function catalogKey(part: CatalogPart): string {
	return `${part.part_num}-${part.color_name}`;
}

const EMPTY_FORM = {
	quantity: 1,
};

export function AddPartModal({ isOpen, onClose, onAdd }: AddPartModalProps) {
	const [query, setQuery] = useState('');
	const [isLookupOpen, setIsLookupOpen] = useState(false);
	const [selectedPart, setSelectedPart] = useState<CatalogPart | null>(null);
	const [form, setForm] = useState(EMPTY_FORM);

	const matches =
		query.trim() === ''
			? []
			: MOCK_CATALOG.filter(
					p =>
						p.name.toLowerCase().includes(query.toLowerCase()) ||
						p.part_num.toLowerCase().includes(query.toLowerCase()) ||
						p.color_name.toLowerCase().includes(query.toLowerCase())
				).slice(0, 8);

	const isValid = selectedPart !== null && form.quantity > 0;

	function reset() {
		setQuery('');
		setIsLookupOpen(false);
		setSelectedPart(null);
		setForm(EMPTY_FORM);
	}

	function handleClose() {
		reset();
		onClose();
	}

	function handleQueryChange(value: string) {
		setQuery(value);
		setSelectedPart(null);
		setIsLookupOpen(true);
	}

	function handleSelectPart(part: CatalogPart) {
		setSelectedPart(part);
		setQuery(`${part.part_num}: ${part.name} (${part.color_name})`);
		setIsLookupOpen(false);
	}

	function handleSubmit(e: FormEvent) {
		e.preventDefault();
		if (!selectedPart || !isValid) return;

		onAdd({
			part_num: selectedPart.part_num,
			name: selectedPart.name,
			color_name: selectedPart.color_name,
			quantity: form.quantity,
		});
		reset();
	}

	return (
		<Modal
			isOpen={isOpen}
			onClose={handleClose}
			title='Add Part'
			footer={
				<>
					<button type='button' className='add-part-btn add-part-btn-secondary' onClick={handleClose}>
						Cancel
					</button>
					<button type='submit' form='add-part-form' className='add-part-btn add-part-btn-primary' disabled={!isValid}>
						Add
					</button>
				</>
			}>
			<form id='add-part-form' className='add-part-form' onSubmit={handleSubmit}>
				<label className='add-part-field'>
					<span>Part</span>
					<div className='add-part-combobox'>
						<input
							type='text'
							role='combobox'
							aria-expanded={isLookupOpen && matches.length > 0}
							aria-autocomplete='list'
							value={query}
							onChange={e => handleQueryChange(e.target.value)}
							onFocus={() => setIsLookupOpen(true)}
							onBlur={() => setIsLookupOpen(false)}
							placeholder='Search part number, name, or color…'
							autoComplete='off'
							required
						/>
						{isLookupOpen && query.trim() !== '' && (
							<ul className='add-part-combobox-list'>
								{matches.length === 0 && <li className='add-part-combobox-empty'>No matching parts</li>}
								{matches.map(part => (
									<li key={catalogKey(part)}>
										<button
											type='button'
											className='add-part-combobox-option'
											onMouseDown={e => {
												e.preventDefault();
												handleSelectPart(part);
											}}>
											<span className='add-part-combobox-option-num'>{part.part_num}</span>
											<span>{part.name}</span>
											<span className='add-part-combobox-option-color'>{part.color_name}</span>
										</button>
									</li>
								))}
							</ul>
						)}
					</div>
				</label>

				<label className='add-part-field'>
					<span>Quantity</span>
					<input
						type='number'
						min={1}
						value={form.quantity}
						onChange={e => setForm(prev => ({ ...prev, quantity: Number(e.target.value) }))}
						required
					/>
				</label>
			</form>
		</Modal>
	);
}
