"use client";
import { useState } from "react";
import { createEvent } from "@/lib/api";

export default function CreateEvent() {
  const [form, setForm] = useState({
    ename: "",
    edesc: "",
    edateb: "",
    edatee: "",
    vid: "1",
  });
  const [images, setImages] = useState<File[]>([]);
  const [seats, setSeats] = useState<{ seat: string; price: number }[]>([]);
  const [newSeat, setNewSeat] = useState({ seat: "", price: "", count: 0 });

  const handleAddSeat = () => {
    if (newSeat.seat && newSeat.price) {
      setSeats([...seats, { seat: newSeat.seat, price: parseFloat(newSeat.price) }]);
      setNewSeat({ seat: "", price: "" });
    }
  };

  const handleRemoveSeat = (index: number) => {
    setSeats(seats.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("action", "create_event");

    // Add form fields
    Object.entries(form).forEach(([key, value]) => formData.append(key, value));

    // Add images
    images.forEach((file) => formData.append("images", file));

    // Add seat data
    formData.append("seats", JSON.stringify(seats));

    try {
      await createEvent(formData);
      alert("Event created successfully!");
    } catch {
      alert("Failed to create event");
    }
  };

  return (
    <>
      <a href="/admin/events">Back</a>
      <form onSubmit={handleSubmit} className="p-6 space-y-4 max-w-xl">
        <h1 className="text-2xl font-bold">Create Event</h1>
        <input
          type="text"
          placeholder="Name"
          className="w-full p-2 border rounded"
          value={form.ename}
          onChange={(e) => setForm({ ...form, ename: e.target.value })}
          required
        />
        <textarea
          placeholder="Description"
          className="w-full p-2 border rounded"
          value={form.edesc}
          onChange={(e) => setForm({ ...form, edesc: e.target.value })}
          required
        />
        <input
          type="datetime-local"
          className="w-full p-2 border rounded"
          value={form.edateb}
          onChange={(e) => setForm({ ...form, edateb: e.target.value })}
          required
        />
        <input
          type="datetime-local"
          className="w-full p-2 border rounded"
          value={form.edatee}
          onChange={(e) => setForm({ ...form, edatee: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Venue ID"
          className="w-full p-2 border rounded"
          value={form.vid}
          onChange={(e) => setForm({ ...form, vid: e.target.value })}
          required
        />
        <input
          type="file"
          accept="image/*"
          multiple
          className="w-full"
          onChange={(e) => setImages(Array.from(e.target.files || []))}
        />

        {/* Seat Input */}
        <div className="space-y-2 mt-4">
  <h2 className="text-lg font-semibold">Auto-generate Seats</h2>
  <div className="flex gap-2">
    <input
      type="number"
      placeholder="Number of Seats"
      className="p-2 border rounded w-1/2"
      value={newSeat.count || ""}
      onChange={(e) =>
        setNewSeat({ ...newSeat, count: parseInt(e.target.value) })
      }
    />
    <input
      type="number"
      placeholder="Price"
      className="p-2 border rounded w-1/2"
      value={newSeat.price}
      onChange={(e) => setNewSeat({ ...newSeat, price: e.target.value })}
    />
    <button
      type="button"
      className="bg-purple-600 text-white px-2 rounded"
      onClick={() => {
        const num = parseInt(newSeat.count);
        const price = parseFloat(newSeat.price);
        const autoSeats: { seat: string; price: number }[] = [];

        for (let i = 0; i < num && i < 26; i++) {
          const seatName = String.fromCharCode(65 + i) + "1"; // A1, B1, ...
          autoSeats.push({ seat: seatName, price });
        }

        setSeats([...seats, ...autoSeats]);
      }}
    >
      Generate
    </button>
  </div>
</div>
<button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Create
        </button>
      </form>
    </>
  );
}
