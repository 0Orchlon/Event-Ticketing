
// src/app/admin/events/page.tsx
'use client';
import useSWR from 'swr';
import Link from 'next/link';

const fetcher = (url: string) => fetch(url).then(res => res.json());

export default function EventList() {
  const { data, error } = useSWR('http://localhost:8000/eventapi/', async () => {
    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'list_events' })
    });
    return res.json();
  });

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Events</h1>
      <Link
        href="/admin/events/create"
        className="text-green-600 underline mb-4 inline-block"
      >
        + Create Event
      </Link>
      <ul className="space-y-4">
        {data.map((event: any) => (
          <li key={event.eventid} className="border p-4 rounded shadow">
            <h2 className="font-semibold text-lg">{event.name}</h2>
            <p>{event.description}</p>
            <p>
              {new Date(event.start_time).toLocaleString()} -{' '}
              {new Date(event.end_time).toLocaleString()}
            </p>
            <div className="mt-2 space-x-4">
              <Link
                href={`/admin/events/${event.eventid}`}
                className="text-blue-600 underline"
              >
                Details
              </Link>
              <Link
                href={`/admin/events/${event.eventid}/edit`}
                className="text-yellow-600 underline"
              >
                Edit
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
