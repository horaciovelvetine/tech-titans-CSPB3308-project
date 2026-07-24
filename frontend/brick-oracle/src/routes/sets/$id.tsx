import { createFileRoute } from '@tanstack/react-router';
import { SetDetailPage } from '../../pages/sets/set-detail-page';

export const Route = createFileRoute('/sets/$id')({
	component: SetDetailPage,
});
