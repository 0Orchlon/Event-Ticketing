
// src/app/admin/bookings/page.tsx
'use client';
import useSWR from 'swr';

export default function BookingsPage() {
  const { data, error } = useSWR('bookings', async () => {
    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'all_bookings' }) // You must implement this in backend
    });
    return res.json();
  });

  if (error) return <div>Error loading bookings</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">All Bookings</h1>
      <ul className="space-y-2">
        {data.map((booking: any) => (
          <li key={booking.bookingid} className="border p-4 rounded">
            <p>Booking ID: {booking.bookingid}</p>
            <p>User ID: {booking.userid}</p>
            <p>Seat: {booking.seat}</p>
            <p>Status: {booking.payment_status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
