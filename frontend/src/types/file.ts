export interface File {
  id: string;
  original_filename: string;
  file_type: string;
  size: number;
  uploaded_at: string;
  file: string;
  is_duplicate: boolean;
  duplicate_of: string | null;
}

export interface StorageStatistics {
  total_files: number;
  duplicate_files: number;
  total_size: number;
  saved_size: number;
  last_updated: string;
}

export interface FileFilters {
  search?: string;
  file_type?: string;
  min_size?: number;
  max_size?: number;
  date_filter?: 'today' | 'week' | 'month' | 'custom';
  start_date?: string;
  end_date?: string;
}