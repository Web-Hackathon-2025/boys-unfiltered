import { useBookings } from "../../context/BookingContext";
import { providers } from "../../services/mockData";

export default function AdminDashboard() {
  const { bookings } = useBookings();

  const totalBookings = bookings.length;
  const activeBookings = bookings.filter(
    (b) => b.status === "requested" || b.status === "accepted"
  ).length;
  const completedBookings = bookings.filter(
    (b) => b.status === "completed"
  ).length;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">
        Admin Dashboard
      </h1>

      {/* STATS */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <StatCard
          title="Total Providers"
          value={providers.length}
        />
        <StatCard
          title="Total Bookings"
          value={totalBookings}
        />
        <StatCard
          title="Active Bookings"
          value={activeBookings}
        />
      </div>

      {/* RECENT BOOKINGS */}
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">
          Recent Bookings
        </h2>

        {bookings.length === 0 ? (
          <p className="text-gray-500">
            No bookings yet.
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-left text-gray-500">
              <tr>
                <th className="pb-2">Customer</th>
                <th className="pb-2">Service</th>
                <th className="pb-2">Provider</th>
                <th className="pb-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {bookings.slice(0, 5).map((b) => (
                <tr key={b.id} className="border-t">
                  <td className="py-2">{b.customerName}</td>
                  <td className="py-2">{b.service}</td>
                  <td className="py-2">{b.providerName}</td>
                  <td className="py-2 capitalize">
                    <StatusBadge status={b.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* ---------------- COMPONENTS ---------------- */

function StatCard({ title, value }) {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <p className="text-sm text-gray-500">
        {title}
      </p>
      <p className="text-2xl font-bold">
        {value}
      </p>
    </div>
  );
}

function StatusBadge({ status }) {
  const colors = {
    requested: "bg-yellow-100 text-yellow-700",
    accepted: "bg-blue-100 text-blue-700",
    completed: "bg-green-100 text-green-700",
    rejected: "bg-red-100 text-red-700",
  };

  return (
    <span
      className={`px-2 py-1 rounded text-xs ${
        colors[status]
      }`}
    >
      {status}
    </span>
  );
}
