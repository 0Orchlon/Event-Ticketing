// src/app/admin/bookings/page.tsx
'use client';
import useSWR from 'swr';

export default function BookingsPage() {
  const { data, error } = useSWR('bookings', async () => {
    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'all_bookings' })
    });
    return res.json();
  });

  if (error) return <div>Error loading bookings</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">All Bookings</h1>
      <ul className="space-y-2">
        {data.bookings.map((booking: any) => (
          <li key={booking.ticketid} className="border p-4 rounded">
            <p><strong>Ticket ID:</strong> {booking.ticketid}</p>
            <p><strong>User ID:</strong> {booking.userid || '—'}</p>
            <p><strong>Email:</strong> {booking.email || '—'}</p>
            <p><strong>Seat:</strong> {booking.seat}</p>
            <p><strong>Price:</strong> ₮{booking.price}</p>
            <p><strong>Booked:</strong> ✅</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
