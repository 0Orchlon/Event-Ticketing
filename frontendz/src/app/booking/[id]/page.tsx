'use client';

import { useState } from 'react';

export default function BookPage() {
  const [userid, setUserid] = useState('');
  const [ticketid, setTicketid] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('Booking...');

    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'book_ticket',
        userid,
        ticketid,
      }),
    });

    const data = await res.json();

    if (res.ok) {
      setMessage('✅ Booking successful!');
    } else {
      setMessage(`❌ ${data.error || 'Booking failed'}`);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-xl shadow-md text-black">
      <h1 className="text-2xl font-bold mb-4">Book a Ticket</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">User ID</label>
          <input
            type="text"
            value={userid}
            onChange={(e) => setUserid(e.target.value)}
            className="w-full mt-1 p-2 border rounded"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Ticket ID</label>
          <input
            type="text"
            value={ticketid}
            onChange={(e) => setTicketid(e.target.value)}
            className="w-full mt-1 p-2 border rounded"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Book Ticket
        </button>
        {message && <p className="text-center text-sm mt-2">{message}</p>}
      </form>
    </div>
  );
}
