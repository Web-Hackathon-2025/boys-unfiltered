import { useNavigate } from "react-router-dom";
import { useState } from "react";
import RequestServiceModal from "./RequestServiceModal";

export default function ProviderCard({ provider }) {
  const navigate = useNavigate();
    const [open, setOpen] = useState(false);

  const handleConfirm = () => {
    // TODO: Submit request logic
    alert("Request submitted!");
    setOpen(false);
  };

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition p-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold text-lg">{provider.name}</h3>
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
            {open && (
              <RequestServiceModal
                provider={provider}
                onClose={() => setOpen(false)}
                onConfirm={handleConfirm}
              />
            )}
        </div>
      </div>
    </div>
  );
}
