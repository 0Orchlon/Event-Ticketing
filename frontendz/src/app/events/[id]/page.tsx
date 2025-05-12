'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function EventDetails() {
  const params = useParams();
  const id = params?.id as string;

  const [event, setEvent] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      body: JSON.stringify({ action: 'event_detail', eventid: id }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((data) => setEvent(data))
      .catch((err) => {
        setError('Failed to fetch event details.');
        console.error('Error:', err);
      });
  }, [id]);

  if (error) return <div className="text-red-400 bg-gray-900 min-h-screen p-8">{error}</div>;
  if (!event) return <div className="text-gray-400 bg-gray-900 min-h-screen p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white px-6 py-8">
      <div className="mb-4 flex justify-between items-center">
        <a href="/" className="text-blue-400 hover:underline">
          ← Back
        </a>
        <a
          href={`${id}/seat-select`}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Pay Tickets
        </a>
      </div>

      <div className="bg-gray-800 p-6 rounded shadow-lg max-w-3xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">{event.name}</h1>

        <div>
          <p className="text-lg font-medium">Description:</p>
          <p className="text-gray-300">{event.description}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <p>
            <strong>Start:</strong>{' '}
            {new Date(event.start_time).toLocaleString()}
          </p>
          <p>
            <strong>End:</strong>{' '}
            {new Date(event.end_time).toLocaleString()}
          </p>
          <p className="md:col-span-2">
            <strong>Venue:</strong> {event.venue}
          </p>
        </div>

        <div>
          <strong>Images:</strong>
          <div className="flex gap-3 mt-3 flex-wrap">
            {event.images?.map((img: string, idx: number) => (
              <img
                key={idx}
                src={`http://localhost:8000${img}`}
                alt={`Event Image ${idx + 1}`}
                className="w-32 h-32 object-cover rounded shadow hover:scale-105 hover:shadow-xl transition-transform duration-200"
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
