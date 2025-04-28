# Static Site Generator

This is a simple static site generator project written in Python. It takes markdown files and converts them into HTML.

## Features (In Progress)

- Convert markdown files into HTML
- mark down files are understood to have a new line between each paragraph
- text can either be bold or italic but not both

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/brinwiththevlin/static-site-generator.git
    ```

2. Navigate into the project directory:

    ```bash
    cd static-site-generator
    ```
3. install module
   if installing as a developer
   ```bash
   pip install .[dev]
   ```
   if istalling as user
   ```bash
   pip install .
   ```

### Usage
can convert mnay markdown files to html. each markdown file is requierd to have a title at the top marked by a single hastag then the title
all markdown files and associated files (i.e. images) shuold be placed in static-site-generator/content
then from the root of the project run
```bash
cd path/to/static-site-generator
./main.sh
```
