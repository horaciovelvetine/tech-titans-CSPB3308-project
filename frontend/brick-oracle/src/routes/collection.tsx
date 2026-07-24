import { createFileRoute } from '@tanstack/react-router';
import { requireAuth } from '../auth/require-auth';
import { CollectionPage } from '../pages/collection-page';

export const Route = createFileRoute('/collection')({
	beforeLoad: requireAuth,
	component: CollectionPage,
});
