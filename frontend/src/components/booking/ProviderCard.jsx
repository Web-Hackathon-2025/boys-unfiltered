import { useNavigate } from "react-router-dom";
import { useState } from "react";
import RequestServiceModal from "./RequestServiceModal";
import { useBookings } from "../../context/BookingContext";

export default function ProviderCard({ provider }) {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const { createBooking } = useBookings();

  const handleConfirm = () => {
    createBooking({
      providerId: provider.id,
      providerName: provider.name,
      service: provider.category,
      customerName: "Rohan",
      date: new Date().toISOString().slice(0, 10),
    });

    setOpen(false);
    setShowAlert(true);

    // auto-hide alert
    setTimeout(() => setShowAlert(false), 3000);
    console.log("Booking created for provider:", provider.id);

  };


  return (
    <>
      {/* Success Alert */}
      {showAlert && (
        <div className="mb-3 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          ✅ Service request sent successfully!
        </div>
      )}

      {/* Provider Card */}
      <div className="bg-white rounded-xl shadow hover:shadow-lg transition p-4">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="font-semibold text-lg">
              {provider.name}
            </h3>
            <p className="text-sm text-gray-500">
              {provider.category} • {provider.location}
            </p>
          </div>

          <span className="text-sm bg-green-100 text-green-700 px-2 py-1 rounded">
            ⭐ {provider.rating}
          </span>
        </div>

        <div className="mt-4 flex justify-between items-center">
          <p className="font-semibold text-blue-600">
            PKR {provider.price}
          </p>

          <div className="flex gap-2">
            <button
              onClick={() => navigate(`/providers/${provider.id}`)}
              className="text-sm border px-3 py-1 rounded hover:bg-gray-100"
            >
              View
            </button>

            <button
              onClick={() => setOpen(true)}
              className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
            >
              Request
            </button>
          </div>
        </div>
      </div>

      {/* Request Modal */}
      {open && (
        <RequestServiceModal
          provider={provider}
          onClose={() => setOpen(false)}
          onConfirm={handleConfirm}
        />
      )}
    </>
  );
}
