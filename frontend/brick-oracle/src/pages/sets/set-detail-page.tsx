import { getRouteApi } from '@tanstack/react-router';

const routeApi = getRouteApi('/sets/$id');

export function SetDetailPage() {
	const { id } = routeApi.useParams();

	return <div>Set detail: {id}</div>;
}
