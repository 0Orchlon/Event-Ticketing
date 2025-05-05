// src/app/events/page.tsx - Events List
"use client";
import { useEffect, useState } from "react";
import { fetchEvents } from "@/lib/api";
import Link from "next/link";

export default function EventsPage() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    fetchEvents().then(setEvents);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">All Events</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {events.map((event) => (
          <Link
            key={event.eventid}
            href={`/events/${event.eventid}`}
            className="border p-4 rounded shadow"
          >
            <h2 className="text-xl font-semibold">{event.name}</h2>
            <p className="text-sm text-gray-600">{event.start_time}</p>
            <p>{event.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
