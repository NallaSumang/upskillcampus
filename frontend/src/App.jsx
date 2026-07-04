import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AssetTable from './components/AssetTable';

const API_URL = 'http://localhost:8080/api/assets';

function App() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newAsset, setNewAsset] = useState({ machineName: '', status: 'RUNNING', uptimePercentage: 95.0 });

  const fetchAssets = async () => {
    try {
      setLoading(true);
      const response = await axios.get(API_URL);
      setAssets(response.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching assets:", err);
      setError("Failed to load asset data. Ensure backend is running on port 8080.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  const updateAssetStatus = async (id, newStatus) => {
    try {
      const response = await axios.put(`${API_URL}/${id}/status`, { status: newStatus });
      setAssets(assets.map(asset => asset.id === id ? response.data : asset));
    } catch (err) {
      console.error("Error updating asset status:", err);
      alert("Failed to update status.");
    }
  };

  const addAsset = async (e) => {
    e.preventDefault();
    if (!newAsset.machineName.trim()) return;
    try {
      const response = await axios.post(API_URL, newAsset);
      setAssets([...assets, response.data]);
      setNewAsset({ machineName: '', status: 'RUNNING', uptimePercentage: 95.0 });
      setShowAddForm(false);
    } catch (err) {
      console.error("Error adding asset:", err);
      alert("Failed to add asset.");
    }
  };

  const deleteAsset = async (id) => {
    if (!window.confirm('Are you sure you want to remove this machine?')) return;
    try {
      await axios.delete(`${API_URL}/${id}`);
      setAssets(assets.filter(asset => asset.id !== id));
    } catch (err) {
      console.error("Error deleting asset:", err);
      alert("Failed to delete asset.");
    }
  };

  // Filtered assets
  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.machineName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'ALL' || asset.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  // Dashboard stats
  const totalAssets = assets.length;
  const runningCount = assets.filter(a => a.status === 'RUNNING').length;
  const maintenanceCount = assets.filter(a => a.status === 'MAINTENANCE').length;
  const offlineCount = assets.filter(a => a.status === 'OFFLINE').length;
  const avgUptime = totalAssets > 0 ? (assets.reduce((sum, a) => sum + a.uptimePercentage, 0) / totalAssets).toFixed(1) : 0;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      {/* Header */}
      <header className="max-w-7xl mx-auto mb-8">
        <h1 className="text-3xl font-bold text-white tracking-tight">⚙️ Smart Factory Dashboard</h1>
        <p className="text-gray-400 mt-1">Industrial Asset Management System — Real-time Monitoring</p>
      </header>

      <main className="max-w-7xl mx-auto space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-4">
            <p className="text-gray-400 text-xs uppercase tracking-wide">Total Assets</p>
            <p className="text-2xl font-bold text-white mt-1">{totalAssets}</p>
          </div>
          <div className="bg-gray-800 border border-green-900 rounded-xl p-4">
            <p className="text-green-400 text-xs uppercase tracking-wide">Running</p>
            <p className="text-2xl font-bold text-green-400 mt-1">{runningCount}</p>
          </div>
          <div className="bg-gray-800 border border-yellow-900 rounded-xl p-4">
            <p className="text-yellow-400 text-xs uppercase tracking-wide">Maintenance</p>
            <p className="text-2xl font-bold text-yellow-400 mt-1">{maintenanceCount}</p>
          </div>
          <div className="bg-gray-800 border border-red-900 rounded-xl p-4">
            <p className="text-red-400 text-xs uppercase tracking-wide">Offline</p>
            <p className="text-2xl font-bold text-red-400 mt-1">{offlineCount}</p>
          </div>
          <div className="bg-gray-800 border border-blue-900 rounded-xl p-4">
            <p className="text-blue-400 text-xs uppercase tracking-wide">Avg Uptime</p>
            <p className="text-2xl font-bold text-blue-400 mt-1">{avgUptime}%</p>
          </div>
        </div>

        {/* Controls Row */}
        <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
          <div className="flex gap-3 flex-1">
            {/* Search */}
            <input
              type="text"
              placeholder="Search machines..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-xs"
            />
            {/* Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Statuses</option>
              <option value="RUNNING">Running</option>
              <option value="MAINTENANCE">Maintenance</option>
              <option value="OFFLINE">Offline</option>
            </select>
          </div>
          <div className="flex gap-3">
            <button onClick={fetchAssets} className="bg-gray-700 hover:bg-gray-600 text-white text-sm px-4 py-2 rounded-lg transition-colors">
              🔄 Refresh
            </button>
            <button onClick={() => setShowAddForm(!showAddForm)} className="bg-blue-600 hover:bg-blue-500 text-white text-sm px-4 py-2 rounded-lg transition-colors">
              ➕ Add Machine
            </button>
          </div>
        </div>

        {/* Add Machine Form */}
        {showAddForm && (
          <form onSubmit={addAsset} className="bg-gray-800 border border-gray-700 rounded-xl p-5 flex flex-col sm:flex-row gap-3 items-end">
            <div className="flex-1">
              <label className="block text-xs text-gray-400 mb-1">Machine Name</label>
              <input
                type="text"
                value={newAsset.machineName}
                onChange={(e) => setNewAsset({ ...newAsset, machineName: e.target.value })}
                placeholder="e.g. Industrial Robot B"
                required
                className="bg-gray-900 border border-gray-600 text-gray-100 rounded-lg px-3 py-2 text-sm w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Status</label>
              <select
                value={newAsset.status}
                onChange={(e) => setNewAsset({ ...newAsset, status: e.target.value })}
                className="bg-gray-900 border border-gray-600 text-gray-100 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="RUNNING">Running</option>
                <option value="MAINTENANCE">Maintenance</option>
                <option value="OFFLINE">Offline</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Uptime %</label>
              <input
                type="number"
                min="0" max="100" step="0.1"
                value={newAsset.uptimePercentage}
                onChange={(e) => setNewAsset({ ...newAsset, uptimePercentage: parseFloat(e.target.value) })}
                className="bg-gray-900 border border-gray-600 text-gray-100 rounded-lg px-3 py-2 text-sm w-24 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button type="submit" className="bg-green-600 hover:bg-green-500 text-white text-sm px-5 py-2 rounded-lg transition-colors">
              Save
            </button>
            <button type="button" onClick={() => setShowAddForm(false)} className="bg-gray-600 hover:bg-gray-500 text-white text-sm px-4 py-2 rounded-lg transition-colors">
              Cancel
            </button>
          </form>
        )}

        {/* Content */}
        {loading ? (
          <div className="flex justify-center items-center h-48">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-900/30 text-red-400 p-4 rounded-lg border border-red-800">{error}</div>
        ) : (
          <AssetTable assets={filteredAssets} onUpdateStatus={updateAssetStatus} onDelete={deleteAsset} />
        )}
      </main>
    </div>
  );
}

export default App;
