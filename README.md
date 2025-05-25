# vk_stav

This repository contains scripts and data for collecting posts and comments from VK.com, processing them, and enriching CoNLL-U formatted text data with metadata from these social media interactions.

## Project Overview

The primary workflow involves:
1.  **Data Acquisition**: Fetching posts and comments from specified VK groups using `main.ipynb`.
2.  **Text Aggregation**: Combining the text content from fetched posts and comments into a single text file using `json_post_comment_processing.py`.
3.  **CoNLL-U Processing & Enrichment**: Enriching CoNLL-U files with metadata (source URL, speaker, date) by matching sentences with the previously fetched VK posts/comments using `conllu.ipynb`.
4.  **Utility**: A script `main.py` is also provided to convert CoNLL-U files into a JSON format.

## File Descriptions

### Python Scripts (`.py`)

*   **`main.py`**:
    *   **Purpose**: Converts a CoNLL-U file into a JSON representation.
    *   **Input**: A CoNLL-U file (e.g., `obr.conllu` in the script).
    *   **Output**: A JSON file (e.g., `output1.json`) containing the parsed sentences with metadata and tokens.

*   **`json_post_comment_processing.py`**:
    *   **Purpose**: Extracts text content from JSON files containing VK posts and comments and aggregates them into a single text file.
    *   **Input**:
        *   `data/posts.json`: JSON file with VK posts.
        *   `data/comments.json`: JSON file with VK comments.
    *   **Output**: `posts_comments.txt`: A text file where each post/comment text is on a new line, and original newlines within texts are replaced by spaces. Texts are separated by a double newline.

*   **`fixed_vk_tools.py`**:
    *   **Purpose**: A utility module for the `vk_api` library. It provides helper functions (`VkTools` class with `get_all_iter`, `get_all`) to more easily retrieve all items from paginated VK API endpoints (e.g., fetching all posts or all comments without manual pagination).
    *   **Usage**: Imported and used by `main.ipynb` for data scraping.

### Jupyter Notebooks (`.ipynb`)

*   **`main.ipynb`**:
    *   **Purpose**: Script for scraping data from VK.com. It searches for VK groups, fetches posts from selected groups, and then fetches comments for those posts.
    *   **Dependencies**: `vk_api`, `pandas`, `fixed_vk_tools.py`, `tqdm`.
    *   **Input**: A VK API access token (`VK_TOKEN`) and a search query for groups (e.g., 'ставрополь').
    *   **Output**:
        *   `data/groups.json`: Information about the searched VK groups.
        *   `data/posts.json`: Fetched posts from the selected groups.
        *   `data/comments.json`: Fetched comments from the posts.

*   **`conllu.ipynb`**:
    *   **Purpose**: Performs two main operations on CoNLL-U files:
        1.  **Modification**: Reads a CoNLL-U file, iterates through tokens, and modifies `deprel` from `nsubj` to `nsubj:pass` if the head token is a passive verb.
        2.  **Enrichment**: Reads JSON files containing original post/comment data (`comments.json`, `posts.json` from the *root directory*) and enriches the CoNLL-U sentences (loaded in the first part) by adding metadata fields like `source`, `speaker`, `date`, and `genre`. This matching relies on the text content of `#newpar` sentences in the CoNLL-U file starting with the text from the JSON entries.
    *   **Dependencies**: `conllu`, `json`, `collections.OrderedDict`.
    *   **Input (Modification Part)**:
        *   `processed_all.conllu.2.2.2.modified` (or any CoNLL-U file specified by `file_path`).
    *   **Output (Modification Part)**:
        *   `processed_all.conllu.2.2.2.modified` (overwrites the input if modifications occur).
    *   **Input (Enrichment Part)**:
        *   The CoNLL-U data (`sentences` variable) from the previous step.
        *   `comments.json` (expected in the root directory).
        *   `posts.json` (expected in the root directory).
    *   **Output (Enrichment Part)**:
        *   `processed_all.conllu.2.2.2.meta_enriched_formatted.conllu`.

## Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/revolt2100/vk_stav
    cd vk_stav
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install required Python libraries:**
    ```bash
    pip install vk_api pandas tqdm conllu
    ```

## Instructions for Launch

The workflow can be broken down into several stages:

### 1. Data Acquisition from VK (using `main.ipynb`)

*   **Action**: Open and run the cells in `main.ipynb`.
*   **Prerequisite**:
    *   You **MUST** obtain a valid VK API access token.
    *   Replace the placeholder `VK_TOKEN` in the notebook with your valid token:
        ```python
        VK_TOKEN = 'YOUR_ACTUAL_VK_API_TOKEN'
        ```
*   **Input**:
    *   VK API Token.
    *   The notebook is configured to search for groups with `q='ставрополь'` and take the top 10. You can modify the query and the number of groups.
*   **Output**:
    *   `data/groups.json`: List of VK groups found.
    *   `data/posts.json`: Posts scraped from these groups (100 posts per group by default).
    *   `data/comments.json`: Comments scraped from the fetched posts (up to 100 comments per post by default).

### 2. Extracting Text from Scraped JSON (using `json_post_comment_processing.py`)

*   **Action**: Run the Python script from your terminal.
    ```bash
    python json_post_comment_processing.py
    ```
*   **Prerequisite**: `data/posts.json` and `data/comments.json` must exist (generated from step 1).
*   **Input**:
    *   `data/posts.json`
    *   `data/comments.json`
*   **Output**:
    *   `posts_comments.txt`: Combined texts from posts and comments.

### 3. CoNLL-U Processing and Enrichment (using `conllu.ipynb`)

*   **Action**: Open and run the cells sequentially in `conllu.ipynb`. This notebook is designed for an environment like Google Colab or a local Jupyter setup.
*   **Prerequisites**:
    *   An initial CoNLL-U file. The notebook uses `processed_all.conllu.2.2.2.modified`.
    *   `comments.json` and `posts.json` files must be present in the **root directory** of the notebook's execution environment (or paths adjusted in the script). 
*   **Workflow within the notebook**:
    1.  **Cell 1 (CoNLL-U Modification)**:
        *   Reads: `processed_all.conllu.2.2.2.modified` (or your specified file).
        *   Modifies `deprel` for `nsubj` of passive verbs to `nsubj:pass`.
        *   Writes: Overwrites `processed_all.conllu.2.2.2.modified` if any changes are made. (The example run showed 0 modifications).
    2.  **Cell 2 (Metadata Enrichment)**:
        *   Reads:
            *   `comments.json` (from root)
            *   `posts.json` (from root)
            *   The `sentences` object (CoNLL-U data) from the previous cell.
        *   Enriches CoNLL-U sentences with `source`, `speaker`, `date`, `genre` metadata by matching text.
        *   Writes: `processed_all.conllu.2.2.2.meta_enriched_formatted.conllu`.
*   **Example**:
    1.  Upload/place `processed_all.conllu.2.2.2.modified` to the expected path.
    2.  Upload/place `comments.json` and `posts.json` (which correspond to the CoNLL-U's source text) to the root.
    3.  Run the cells in `conllu.ipynb`.

### 4. CoNLL-U to JSON Conversion (using `main.py`)

*   **Action**: Run the Python script from your terminal.
    ```bash
    python main.py
    ```
*   **Prerequisite**: A CoNLL-U file named `obr.conllu` should be in the same directory as `main.py`, or you need to modify the filename in the script.
*   **Input**: `obr.conllu` (or the specified CoNLL-U file).
*   **Output**: `output1.json`.

## Input Data Formats
*   **VK API Token**: A string provided by VK.com for API access.
*   **`posts.json` / `comments.json`**:
    *   JSON array of objects.
    *   Each object represents a post or comment.
    *   Key fields for `json_post_comment_processing.py`:
        *   `text`: (string) The content of the post/comment.
    *   Key fields for enrichment in `conllu.ipynb`:
        *   `text`: (string) The content.
        *   `id`: (integer) ID of the post/comment.
        *   `date`: (integer) Unix timestamp of creation.
        *   `from_id`: (integer) User ID of the author.
        *   `owner_id`: (integer, for comments) ID of the group/user wall where the post is.
        *   `post_id`: (integer, for comments) ID of the parent post.
*   **`.conllu` files**: Standard CoNLL-U format. Text sentences are typically preceded by metadata lines starting with `#`.
    *   Example metadata added by `conllu.ipynb`:
        ```conllu
        # newpar
        # sent_id = 1
        # source = vk.com/wall-37725105_5082188
        # speaker = vk.com/id330213862
        # date = 1743681381
        # genre = social
        # text = В закладочку на страницу пожалуй добавлю)
        ```
