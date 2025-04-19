import React from 'react';
import { FileFilters } from '../types/file';
import { FunnelIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import debounce from 'lodash/debounce';

interface SearchFiltersProps {
  onFiltersChange: (filters: FileFilters) => void;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({ onFiltersChange }) => {
  const [localFilters, setLocalFilters] = React.useState<FileFilters>({
    search: '',
    file_type: '',
    date_filter: undefined,
  });

  // Create debounced filter change handler
  const debouncedOnFiltersChange = React.useMemo(
    () => debounce(onFiltersChange, 300),
    [onFiltersChange]
  );

  React.useEffect(() => {
    return () => {
      debouncedOnFiltersChange.cancel();
    };
  }, [debouncedOnFiltersChange]);

  const handleFilterChange = (key: keyof FileFilters, value: string | number | undefined) => {
    const newFilters = { ...localFilters, [key]: key === 'date_filter' && value === '' ? undefined : value };
    setLocalFilters(newFilters);
    debouncedOnFiltersChange(newFilters);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="space-y-4">
        {/* Search */}
        <div>
          <div className="relative rounded-md shadow-sm">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={localFilters.search || ''}
              className="block w-full rounded-md border-gray-300 pl-10 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              placeholder="Search files..."
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {/* File Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700">File Type</label>
            <select
              value={localFilters.file_type || ''}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              onChange={(e) => handleFilterChange('file_type', e.target.value)}
            >
              <option value="">All Types</option>
              <option value="image/">Images</option>
              <option value="application/pdf">PDF</option>
              <option value="text/">Text</option>
              <option value="application/">Documents</option>
            </select>
          </div>

          {/* Size Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Size Range</label>
            <div className="mt-1 flex space-x-2">
              <input
                type="number"
                placeholder="Min (KB)"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) => handleFilterChange('min_size', e.target.value ? parseInt(e.target.value) * 1024 : undefined)}
              />
              <input
                type="number"
                placeholder="Max (KB)"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) => handleFilterChange('max_size', e.target.value ? parseInt(e.target.value) * 1024 : undefined)}
              />
            </div>
          </div>

          {/* Date Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Upload Date</label>
            <select
              value={localFilters.date_filter || ''}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              onChange={(e) => handleFilterChange('date_filter', e.target.value || undefined)}
            >
              <option value="">All Time</option>
              <option value="today">Today</option>
              <option value="week">Last Week</option>
              <option value="month">Last Month</option>
              <option value="custom">Custom Range</option>
            </select>
          </div>

          {/* Custom Date Range */}
          {localFilters.date_filter === 'custom' && (
            <div>
              <label className="block text-sm font-medium text-gray-700">Custom Range</label>
              <div className="mt-1 flex space-x-2">
                <input
                  type="date"
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  onChange={(e) => handleFilterChange('start_date', e.target.value)}
                />
                <input
                  type="date"
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  onChange={(e) => handleFilterChange('end_date', e.target.value)}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
