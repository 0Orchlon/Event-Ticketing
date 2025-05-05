// src/app/events/[id]/page.tsx - Event Detail
"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/eventapi/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "event_detail", eventid: id }),
    })
      .then((res) => res.json())
      .then(setEvent);
  }, [id]);

  if (!event) return <p className="p-6">Loading...</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-2">{event.name}</h1>
      <p>{event.description}</p>
      <p className="text-gray-600">
        {event.start_time} - {event.end_time}
      </p>
    </div>
  );
}
