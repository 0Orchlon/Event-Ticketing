
// src/app/admin/users/page.tsx
'use client';
import useSWR from 'swr';

export default function UsersPage() {
  const { data, error } = useSWR('users', async () => {
    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'all_users' }) // You must implement this in backend
    });
    return res.json();
  });

  if (error) return <div>Error loading users</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">All Users</h1>
      <ul className="space-y-2">
        {data.map((user: any) => (
          <li key={user.userid} className="border p-4 rounded">
            <p>User ID: {user.userid}</p>
            <p>Email: {user.email}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
