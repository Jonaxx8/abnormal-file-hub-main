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