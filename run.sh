#!/bin/bash

flatten_directories() {
  local dir="$1"
  local target_dir="$2"

  for item in "$dir"/*; do
    if [ -d "$item" ]; then
      flatten_directories "$item" "$target_dir"
    elif [ -f "$item" ]; then
      local file_name=$(basename "$item")
      cp "$item" "$target_dir/$file_name"
    fi
  done
}

rename_files() {
  local dir="$1"
  
  for item in "$dir"/*; do
    if [ -f "$item" ]; then
      file_type=$(file -b --mime-type "$item")
      base_name=$(basename "$item")
      dir_name=$(dirname "$item")

      case "$file_type" in
        "image/jpeg" | "image/png" | "image/gif")
          new_filename="${dir_name}/${base_name%.*}.jpg"
          ;;
        "application/pdf")
          new_filename="${dir_name}/${base_name%.*}.pdf"
          ;;
        "text/html")
          new_filename="${dir_name}/${base_name%.*}.html"
          ;;
        "text/plain")
          new_filename="${dir_name}/${base_name%.*}.txt"
          ;;
        *)
          new_filename="${dir_name}/${base_name}_unknown"
          ;;
      esac

      if [ "$item" != "$new_filename" ]; then
        echo "Renaming $item to $new_filename"
        mv "$item" "$new_filename"
      fi
    fi
  done
}



extract_files() {
  local dir="$1"
  
  for item in "$dir"/*; do
    if [ -d "$item" ]; then
      extract_files "$item"
    elif [ -f "$item" ]; then
      echo "Extracting file: $item"
      #local extract_dir="extracted_data/$(dirname "$item")"
      local extract_dir="extracted_data/$item" 
      #echo "!!! extract $extract_dir" 
      mkdir -p "$extract_dir"
      python3 -m warcat extract "$item" --output-dir "$extract_dir" --progress
      #local flatten_dir="flatten_data/$(dirname "$item")"
      local flatten_dir="flatten_data/$item"
      #echo "!!! flatten $flatten_dir" 
      mkdir -p "$flatten_dir"
      flatten_directories "$extract_dir" "$flatten_dir" 
      rename_files "$flatten_dir"
    fi
  done
}

if [ -z "$1" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

ROOT_DIR="$1"
EXTRACTED_DIR="extracted_data"
FLATTENED_DIR="flatten_data"

mkdir -p "$EXTRACTED_DIR"
mkdir -p "$FLATTENED_DIR"

extract_files "$ROOT_DIR"
#flatten_directories "$EXTRACTED_DIR" "$FLATTENED_DIR"
#rename_files "$FLATTENED_DIR"

echo "Process complete. Files are extracted, flattened, and renamed."

