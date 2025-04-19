import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fileService } from '../services/fileService';
import { ChartBarIcon } from '@heroicons/react/24/outline';

export const StorageStats = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['storage-stats'],
    queryFn: fileService.getStorageStatistics,
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  if (isLoading || !stats) {
    return (
      <div className="animate-pulse bg-white shadow rounded-lg p-4">
        <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    );
  }

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const savingsPercentage = stats.total_size > 0 
    ? ((stats.saved_size / stats.total_size) * 100).toFixed(1)
    : '0';

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center mb-4">
        <ChartBarIcon className="h-6 w-6 text-primary-600 mr-2" />
        <h2 className="text-xl font-semibold text-gray-900">Storage Statistics</h2>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500">Total Files</p>
          <p className="text-2xl font-semibold text-gray-900">{stats.total_files}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500">Duplicate Files</p>
          <p className="text-2xl font-semibold text-gray-900">{stats.duplicate_files}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500">Total Storage</p>
          <p className="text-2xl font-semibold text-gray-900">{formatSize(stats.total_size)}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500">Storage Saved</p>
          <p className="text-2xl font-semibold text-primary-600">
            {formatSize(stats.saved_size)}
            <span className="text-sm ml-1">({savingsPercentage}%)</span>
          </p>
        </div>
      </div>
    </div>
  );
};
