"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { sendRequest } from '@/utils/api'; // Make sure to import the sendRequest function

interface User {
  uid: number;
  gmail: string;
  fname: string;
  lname: string;
  last_login?: string;
}

interface Entry {
  id: number;
  type: string; // 'Income' or 'Expense'
  amount: number;
  date: string;
  description: string;
}

export default function profile() {
  const [user, setUser] = useState<User | null>(null);
  const [history, setHistory] = useState<Entry[]>([]);
  const [incomesum, setIncome] = useState<number>(0);
  const [expensesum, setExpense] = useState<number>(0);
  const [totalsum, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [amount, setAmount] = useState<number>(0); // Price input
  const [description, setDescription] = useState<string>(''); // Description input
  const [type, setType] = useState<string>('Income'); // Type dropdown (Income or Expense)
  
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    } else {
      try {
        const parsedUser: User = JSON.parse(token);
        setUser(parsedUser);
        fetchData(parsedUser.uid);
      } catch (err) {
        console.error("Invalid token format:", err);
        localStorage.removeItem("token");
        router.push("/login");
      }
    }
  }, [router]);

  const fetchData = async (userId: number) => {
    try {
      // Fetch history data
      const historyData = await sendRequest("http://localhost:8000/user/", "POST", {
        action: "history",
        uid: userId,
      });
      const incomesumData = await sendRequest("http://localhost:8000/user/", "POST", {
        action: "incomesum",
        uid: userId
      });
      const expenseData = await sendRequest("http://localhost:8000/user/", "POST", {
        action: "expensesum",
        uid: userId
      });
      const totalSumData = await sendRequest("http://localhost:8000/user/", "POST", {
        action: "total",
        uid: userId
      });

      const mappedHistoryData = historyData.data.map((entry: any, index: number) => ({
        id: index,
        type: entry.type,
        amount: entry.expense,
        date: new Date(entry.date).toLocaleString(),
        description: entry.desc,
      }));

      const totalIncome = incomesumData.data[0]?.totalIncome || 0;
      setIncome(totalIncome);

      const totalExpense = parseFloat(expenseData.data[0]?.totalIncome || expenseData.data[0]?.totalExpense || "0");
      setExpense(isNaN(totalExpense) ? 0 : totalExpense);

      const totalSum = parseFloat(totalSumData.data[0]?.total || "0");
      setTotal(isNaN(totalSum) ? 0 : totalSum);

      setHistory(mappedHistoryData);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to fetch data. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };
  
const toIncome = () => {
  router.push("/income")
}  

const toExpense = () => {
  router.push("/expense")
}

  const handleSubmit = async () => {
    if (amount <= 0 || !description) {
      alert("Please provide a valid amount and description");
      return;
    }

    const action = type === "Income" ? "logincome" : "addexpense";

    try {
      const response = await sendRequest("http://localhost:8000/user/", "POST", {
        action,
        uid: user?.uid,
        amount,
        description,
      });
      console.log("Response from server:", response);
      fetchData(user!.uid); // Refresh the data after submission
    } catch (err) {
      console.error("Error submitting entry:", err);
      setError("Failed to submit data. Please try again.");
    }
  };


  if (loading) {
    return <p className="text-center text-xl">Loading...</p>;
  }

  if (!user) {
    return (
      <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg mt-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-4">
          Error
        </h1>
        <p className="text-lg text-red-600 text-center">User not found.</p>
        <div className="mt-6 flex justify-center">
          <button
            onClick={handleLogout}
            className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg mt-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Dashboard
        </h1>

        <div className="bg-gray-50 p-6 rounded-md shadow-md">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Welcome, {user.fname} {user.lname}!
          </h2>
          
          <div className="mt-4 space-x-4">
            <button
              onClick={() => router.push("/changepassword")}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 transition"
            >
              Change Password
            </button>
            <button
              onClick={() => router.push("/edituser")}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 transition"
            >
              Edit Profile
            </button>
            <button
              onClick={handleLogout}
              className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
