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
    <main className="p-6 md:p-12 bg-gradient-to-b from-white via-gray-50 to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 min-h-screen transition-colors duration-300">
      <h1 className="text-4xl md:text-5xl font-extrabold text-center text-gray-800 dark:text-white drop-shadow-md mb-10">
        🎟️ Upcoming Events
      </h1>

      <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {events.map((event: any) => (
          <div
            key={event.eventid}
            onClick={() => router.push(`/events/${event.eventid}`)}
            className="group bg-white dark:bg-gray-800 rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden border dark:border-gray-700"
          >
            {event.images.length > 0 && (
              <img
                src={`http://localhost:8000${event.images[0]}`}
                alt={event.name}
                className="w-full h-56 object-cover transition-transform duration-300 group-hover:scale-105"
              />
            )}
            <div className="p-5">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                {event.name}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-300 mt-2">
                {new Date(event.start_time).toLocaleString()}
              </p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
