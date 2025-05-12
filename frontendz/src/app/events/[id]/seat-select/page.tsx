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
  const [selected, setSelected] = useState<number[]>([]);
  const [userid, setUserid] = useState<number | null>(null); // simulate login
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  // const [price, setPrice] = useState<Price>([]);

  useEffect(() => {
    // Simulate checking for login
    const storedUser = localStorage.getItem('userid');
    if (storedUser) setUserid(Number(storedUser));

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

  const toggleSeat = (ticketid: number) => {
    setSelected(prev =>
      prev.includes(ticketid)
        ? prev.filter(id => id !== ticketid)
        : [...prev, ticketid]
    );
  };

  const handlePurchase = async () => {
  if (selected.length === 0) return alert('No seats selected.');
  if (!userid && email.trim() === '') return alert('Please provide your email.');

  setLoading(true); // Start loading

  const body: any = {
    action: 'buy_seats',
    eventid: id,
    ticketids: selected,
  };
  if (userid) body.userid = userid;
  else body.email = email.trim();

  try {
    const response = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const result = await response.json();

    if (result.status === 200) {
      alert('Seats booked successfully!');
      setSelected([]);
      const updated = await fetch('http://localhost:8000/eventapi/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'get_seats', eventid: id }),
      });
      const data = await updated.json();
      setSeats(data.seats);
    } else {
      alert('Booking failed: ' + result.message);
    }
  } catch (err) {
    alert('Booking error');
    console.error(err);
  } finally {
    setLoading(false); // Stop loading
  }
};

  const totalPrice = selected
  .map(id => seats.find(seat => seat.ticketid === id)?.price || 0)
  .reduce((acc, price) => acc + price, 0);
  const seatPrice = seats.find(seat => !seat.booked)?.price ?? '—';
if (loading) {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-xl font-semibold animate-pulse text-purple-600">
        Booking your seats...
      </div>
    </div>
  );
}

  return (
    <div className="p-4">
      <a href={`/events/${id}`}>Back</a>
      <h1 className="text-2xl font-bold mb-4">Select Seats for Event #{id}</h1>
      <h2 className='text-lg font-medium md-2'>1 Seat price: {seatPrice}</h2>
      <h2 className="text-lg font-medium mb-2">Selected Seats: {selected.length}</h2>
      <h2 className="text-lg font-medium mb-4">Total Price: ₮{totalPrice}</h2>
      <div className="space-y-2 mb-4">
  {Array.from({ length: Math.ceil(seats.length / 10) }, (_, i) => (
    <div key={i} className="flex gap-2">
      {seats.slice(i * 10, i * 10 + 10).map(seat => (
        <button
          key={seat.ticketid}
          disabled={seat.booked}
          onClick={() => toggleSeat(seat.ticketid)}
          className={`p-2 rounded border text-white text-sm w-24 text-center ${
            seat.booked
              ? 'bg-gray-400 cursor-not-allowed'
              : selected.includes(seat.ticketid)
              ? 'bg-blue-600'
              : 'bg-green-500 hover:bg-green-600'
          }`}
        >
          {seat.seat}<br />₮{seat.price}
        </button>
      ))}
    </div>
  ))}
</div>


      {!userid && (
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="mb-4 p-2 border rounded w-full max-w-sm"
        />
      )}

      <button
        onClick={handlePurchase}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Confirm Purchase
      </button>
    </div>
  );
}
