'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

interface Seat {
  ticketid: number;
  seat: string;
  price: number;
  booked: boolean;
}

export default function SeatSelectPage() {
  const { id } = useParams();
  const [seats, setSeats] = useState<Seat[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'get_seats',
        eventid: id,
      }),
    })
      .then(res => res.json())
      .then(data => setSeats(data.seats))
      .catch(err => console.error('Fetch error:', err));
  }, [id]);

  return (
    <div className="p-4">
      <a href={`/events/${id}`}>Back</a>
      <h1 className="text-2xl font-bold mb-4">Select Seats for Event #{id}</h1>
      <div className="grid grid-cols-10 gap-2">
        {seats.map(seat => (
          <button
            key={seat.ticketid}
            disabled={seat.booked}
            className={`p-2 rounded ${
              seat.booked ? 'bg-gray-400' : 'bg-green-500 hover:bg-green-600'
            }`}
          >
            {seat.seat}
          </button>
        ))}
      </div>
    </div>
  );
}
