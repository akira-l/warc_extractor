# WARC Extractor

## Dependencies

The WARC Extractor depends on the `warcat` library. You can install it using pip:

```bash
pip3 install warcat
```

## Usage

To run the WARC Extractor, use the provided shell script. The script takes the path to a folder containing WARC files as an argument.

### Running the Script

```bash
bash run.sh WARC_FOLDER_PATH
```

For example, if your WARC files are located in the `ACM` directory, you can run:

```bash
bash run.sh ACM
```

This will process the WARC files in the `ACM` folder, such as `ACM/2020-05_ACM_0001.warc.gz`.

## Output

The WARC Extractor generates two types of output, which are saved in separate directories:

1. **Extracted Data**: This directory contains data extracted directly from the WARC files.
   - Directory: `extracted_data`

2. **Flatten Data**: This directory contains data that has been reprocessed to reduce redundant folders and paths.
   - Directory: `flatten_data`
