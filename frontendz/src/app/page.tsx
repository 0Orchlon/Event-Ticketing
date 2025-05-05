// src/app/page.tsx
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [events, setEvents] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const loadEvents = async () => {
      const formData = new FormData();
      formData.append("action", "list_events");

      const res = await fetch("http://localhost:8000/eventapi/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        console.error("Failed to fetch events");
        return;
      }

      const data = await res.json();
      setEvents(data);
    };

    loadEvents();
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-4xl font-bold text-center">Upcoming Events</h1>
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        {events.map((event: any) => (
          <div
            key={event.eventid}
            className="border rounded-lg p-4 cursor-pointer hover:shadow"
            onClick={() => router.push(`/events/${event.eventid}`)}
          >
            {event.images.length > 0 && (
              <img
                src={`http://localhost:8000${event.images[0]}`}
                alt={event.name}
                className="w-full h-48 object-cover rounded mb-2"
              />
            )}
            <h2 className="text-xl font-semibold">{event.name}</h2>
            <p className="text-sm text-gray-600">{new Date(event.start_time).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
