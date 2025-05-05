// src/app/admin/page.tsx
export default function AdminDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <ul className="list-disc pl-5 space-y-2">
        <li><a className="text-blue-600 underline" href="/admin/events">Manage Events</a></li>
        <li><a className="text-blue-600 underline" href="/admin/bookings">View Bookings</a></li>
        <li><a className="text-blue-600 underline" href="/admin/users">User List</a></li>
      </ul>
    </div>
  );
}
