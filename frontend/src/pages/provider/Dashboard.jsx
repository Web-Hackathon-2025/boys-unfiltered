import { useBookings } from "../../context/BookingContext";
import { useAuth } from "../../context/AuthContext";

export default function ProviderDashboard() {
  const { bookings, updateStatus } = useBookings();
  const { user } = useAuth();

  // 🔑 only bookings for this provider
  const providerBookings = bookings.filter(
    (b) => b.providerId === user?.id
  );

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">
        Incoming Requests
      </h1>

      {providerBookings.length === 0 && (
        <p className="text-gray-500">
          No incoming requests yet.
        </p>
      )}

      <div className="space-y-4">
        {providerBookings.map((b) => (
          <div
            key={b.id}
            className="bg-white p-4 rounded shadow flex justify-between"
          >
            <div>
              <p className="font-semibold">{b.customerName}</p>
              <p className="text-sm text-gray-500">
                {b.service} • {b.date}
              </p>
              <span className="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-700">
                {b.status}
              </span>
            </div>

            {b.status === "requested" && (
              <div className="flex gap-2">
                <button
                  onClick={() =>
                    updateStatus(b.id, "accepted")
                  }
                  className="bg-green-600 text-white px-3 py-1 rounded"
                >
                  Accept
                </button>
                <button
                  onClick={() =>
                    updateStatus(b.id, "rejected")
                  }
                  className="bg-red-600 text-white px-3 py-1 rounded"
                >
                  Reject
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
