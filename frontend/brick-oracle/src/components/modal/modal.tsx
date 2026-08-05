import { useEffect } from 'react';
import type { ReactNode } from 'react';
import { createPortal } from 'react-dom';
import './modal.css';

interface ModalProps {
	isOpen: boolean;
	onClose: () => void;
	title: string;
	children: ReactNode;
	footer?: ReactNode;
}

export function Modal({ isOpen, onClose, title, children, footer }: ModalProps) {
	useEffect(() => {
		if (!isOpen) return;
		function handleKeyDown(e: KeyboardEvent) {
			if (e.key === 'Escape') onClose();
		}
		document.addEventListener('keydown', handleKeyDown);
		return () => document.removeEventListener('keydown', handleKeyDown);
	}, [isOpen, onClose]);

	if (!isOpen) return null;

	return createPortal(
		<div
			className='modal-backdrop'
			onMouseDown={e => {
				if (e.target === e.currentTarget) onClose();
			}}>
			<div
				className='modal-panel'
				role='dialog'
				aria-modal='true'
				aria-label={title}>
				<div className='modal-header'>
					<h2 className='modal-title'>{title}</h2>
					<button
						type='button'
						className='modal-close-btn'
						aria-label='Close'
						onClick={onClose}>
						×
					</button>
				</div>
				<div className='modal-body'>{children}</div>
				{footer && <div className='modal-footer'>{footer}</div>}
			</div>
		</div>,
		document.body
	);
}
