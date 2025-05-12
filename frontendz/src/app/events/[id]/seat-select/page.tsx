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
  const [userid, setUserid] = useState<number | null>(null);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
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
    setLoading(true);

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
      setLoading(false);
    }
  };

  const totalPrice = selected
    .map(id => seats.find(seat => seat.ticketid === id)?.price || 0)
    .reduce((acc, price) => acc + price, 0);
  const seatPrice = seats.find(seat => !seat.booked)?.price ?? '—';

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
        <div className="text-xl font-semibold animate-pulse text-purple-400">
          Booking your seats...
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto bg-gray-900 text-white min-h-screen">
      <a href={`/events/${id}`} className="text-blue-400 hover:underline mb-4 inline-block">← Back to event</a>
      <h1 className="text-2xl font-bold mb-2">Select Seats for Event #{id}</h1>
      <p className="text-md mb-1">1 Seat Price: ₮{seatPrice}</p>
      <p className="text-md mb-1">Selected Seats: {selected.length}</p>
      <p className="text-md mb-4 font-semibold">Total Price: ₮{totalPrice}</p>

      {/* Grid layout for seats */}
      <div className="grid grid-cols-10 gap-2 mb-6">
        {seats.map(seat => (
          <button
            key={seat.ticketid}
            disabled={seat.booked}
            onClick={() => toggleSeat(seat.ticketid)}
            className={`p-2 rounded border text-white text-xs text-center transition-all duration-200 h-16 ${
              seat.booked
                ? 'bg-gray-600 cursor-not-allowed'
                : selected.includes(seat.ticketid)
                ? 'bg-blue-600'
                : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {seat.seat}
            <br />₮{seat.price}
          </button>
        ))}
      </div>

      {/* Email input for guest user */}
      {!userid && (
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="mb-4 p-2 border border-gray-500 rounded w-full max-w-sm bg-gray-800 text-white"
        />
      )}

      {/* Confirm button */}
      <button
        onClick={handlePurchase}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Confirm Purchase
      </button>
    </div>
  );
}
