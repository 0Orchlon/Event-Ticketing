
// src/app/tickets/page.tsx
"use client";
import { useEffect, useState } from "react";

export default function MyTickets() {
  const [tickets, setTickets] = useState<any[]>([]);

  useEffect(() => {
    const userid = 1; // Replace with actual logged-in user ID
    fetch("http://localhost:8000/eventapi/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "get_user_tickets", userid }),
    })
      .then((res) => res.json())
      .then(setTickets);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">My Tickets</h1>
      <ul className="space-y-4">
        {tickets.map((t) => (
          <li key={t.bookingid} className="border p-4 rounded shadow">
            <p className="font-semibold">{t.event_name}</p>
            <p>Seat: {t.seat}</p>
            <p>Status: {t.payment_status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
