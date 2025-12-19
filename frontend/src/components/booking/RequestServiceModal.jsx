export default function RequestServiceModal({ provider, onClose, onConfirm }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-2">
          Request Service
        </h2>

        <p className="text-gray-600 mb-4">
          {provider.name} — {provider.category}
        </p>

        <label className="block text-sm mb-1">
          Preferred Date
        </label>
        <input
          type="date"
          className="w-full border rounded px-3 py-2 mb-4"
        />

        <label className="block text-sm mb-1">
          Additional Notes
        </label>
        <textarea
          className="w-full border rounded px-3 py-2 mb-4"
          rows="3"
          placeholder="Describe the issue..."
        />

        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded"
          >
            Cancel
          </button>
          <button 
            onClick={onConfirm}
            className="px-4 py-2 bg-blue-600 text-white rounded"
          >
            Confirm Request
          </button>
        </div>
      </div>
    </div>
  );
}
