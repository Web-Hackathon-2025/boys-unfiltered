import { bookings } from "../../services/mockBookings";

export default function ProviderDashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">
        Incoming Requests
      </h1>

      <div className="space-y-4">
        {bookings.map((b) => (
          <div
            key={b.id}
            className="bg-white p-4 rounded shadow flex justify-between items-center"
          >
            <div>
              <p className="font-semibold">{b.customerName}</p>
              <p className="text-sm text-gray-500">
                {b.service} • {b.date}
              </p>
              <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">
                {b.status}
              </span>
            </div>

            <div className="flex gap-2">
              <button className="bg-green-600 text-white px-3 py-1 rounded">
                Accept
              </button>
              <button className="bg-red-600 text-white px-3 py-1 rounded">
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
