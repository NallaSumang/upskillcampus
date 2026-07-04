import React from 'react';

const AssetTable = ({ assets, onUpdateStatus, onDelete }) => {
  const getStatusBadge = (status) => {
    const styles = {
      RUNNING: 'bg-green-500/20 text-green-400 border-green-500/30',
      MAINTENANCE: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      OFFLINE: 'bg-red-500/20 text-red-400 border-red-500/30',
    };
    const style = styles[status] || 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    return <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border ${style}`}>{status}</span>;
  };

  const getUptimeColor = (pct) => {
    if (pct >= 95) return 'bg-green-500';
    if (pct >= 80) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-750 text-gray-400 text-xs uppercase tracking-wider border-b border-gray-700">
            <tr>
              <th className="px-5 py-3">ID</th>
              <th className="px-5 py-3">Machine Name</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Uptime</th>
              <th className="px-5 py-3">Set Status</th>
              <th className="px-5 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700/50">
            {assets.map((asset) => (
              <tr key={asset.id} className="hover:bg-gray-700/30 transition-colors">
                <td className="px-5 py-3 text-gray-300 font-mono text-xs">#{asset.id}</td>
                <td className="px-5 py-3 text-white font-medium">{asset.machineName}</td>
                <td className="px-5 py-3">{getStatusBadge(asset.status)}</td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-20 bg-gray-700 rounded-full h-1.5">
                      <div className={`h-1.5 rounded-full ${getUptimeColor(asset.uptimePercentage)}`} style={{ width: `${asset.uptimePercentage}%` }}></div>
                    </div>
                    <span className="text-xs text-gray-400">{asset.uptimePercentage}%</span>
                  </div>
                </td>
                <td className="px-5 py-3">
                  <select
                    value={asset.status}
                    onChange={(e) => onUpdateStatus(asset.id, e.target.value)}
                    className="bg-gray-900 border border-gray-600 text-gray-200 text-xs rounded-lg px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="RUNNING">RUNNING</option>
                    <option value="MAINTENANCE">MAINTENANCE</option>
                    <option value="OFFLINE">OFFLINE</option>
                  </select>
                </td>
                <td className="px-5 py-3 text-right">
                  <button
                    onClick={() => onDelete(asset.id)}
                    className="text-red-400 hover:text-red-300 text-xs hover:underline transition-colors"
                  >
                    🗑 Remove
                  </button>
                </td>
              </tr>
            ))}
            {assets.length === 0 && (
              <tr>
                <td colSpan="6" className="px-5 py-10 text-center text-gray-500">No machines match your search.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssetTable;
