import { createFileRoute } from '@tanstack/react-router';
import { SetsPage } from '../../pages/sets/sets-page';

export const Route = createFileRoute('/sets/')({
	component: SetsPage,
});
