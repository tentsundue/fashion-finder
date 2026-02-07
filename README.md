# Fashion Finder (Name WIP)
This is a new project that aims to let users find an assortment of clothes in their price range that are similar to ones they wear or are just interested in. Hopefully, this can be used so that people don't have to break the bank to maintain their style.

## Development Roadmap (subject to change):

### Collect Data:

1. Scrape clothing vendor website (i.e. Uniqlo, H&M, Levi's, etc.)

2. Collect product metadata and store in csv, database in the future 

    - **Structure**: `image_id, product_id, variant_id, category, price, image_url, brand, product_url, currency`

3. Download and save images of each product in our `metadata.csv`


### Setup Indexing for Lookup:
1. Convert each image into a 512-vector representation using the CLIP model. 
   Each vector is stored in a larger embeddings array, located in `embeddings.npy`
   
   _Personal Note_: The way I understand it, each vector is like a list of coordinates. We use these coords to evaluate similarity to our user's image. Closer proximity = better similarity.

2. Map metadata information to the appropriate vector. This will be used for indexing in our search engine.
    - **Structure**: `{ [vector] : (price, currency, brand, product_url, etc.), ... }`


### Build User Search Pipeline:

1. Establish clear input parameters for the user's _clothing item immage_ and _price range_

2. Convert the user's provided image into its vector representation

3. Search using the index established earlier and retrieve the metadata for the appropriate clothing items

4. Return product info to user to browse ez-pz.

### Develop a Web Application Interface:

1. Create a GUI for easy User Interaction

2. Establish an API for backend communication

3. Move current metadata and images to a database

4. Deploy the application

## Tech Stack

### ML:
- CLIP (OpenClip)
- Python (PyTorch)
- Facebook AI Similiarity Search (FAISS)
- NumPy, Pandas

### Backend/API/Database:
- FastAPI, Node, or Express
  - I don't know yet, haven't gotten this far to accurately decide
- Postgres for metadata storage, S3 for image storage (?) 
  - Limiting scope to csvs for now for testing and MVP purposes

### Frontend/UI:
- Probably React w/ TypeScript
  - That's what I'm most familar with but we'll cross that bridge when we get there
- Tailwind or ChakraUI
  - Depends on what I'm feeling like when I get there



# Setup

### __Before Getting Started__: Ensure that your machine has <ins>Python 3.9+</ins> installed.

### Clone the repository
```
git clone https://github.com/tentsundue/fashion-finder.git
cd fashion-finder
```

### Setup the virtual environment (venv)

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```
Note that this would install the CPU version of pytorch if on Windows. 

If you have a GPU and would prefer to use that, then see _https://pytorch.org/get-started/locally/_

Whichever is downloaded doesn't seem to matter much at the moment (because the project is still early WIP)
but it's worth mentioning that `clip_model.py` prioritizes the GPU version if installed, defaulting to CPU if not.


### Download Images from `metadata.csv`
I am currently doing this in my web scraper, which is located in another repository linked in the `References` section below. It builds the metadata for each product across a select portion of clothing vendors and downloads the appropriate images. The folder strucutre is organized a bit differently than how it is in this repo so the script for downloading is not one-to-one at the moment. I will move the script over to this repo once it is refactored, but for now, you will have to clone the _Clothing Website Scraper_ repo, set it up, run the `download_images.py` script and manually move the downloaded images into `data/images/{vendor_name}.

It's just a matter of moving folders but could still take around 5 min depending on how many vendors I have at that moment. As of `Feb 6, 2026`, it's just Uniqlo products.

## References
Clothing Website Scraper, Tenzin Tsundue - https://github.com/tentsundue/clothing-sites-scraper
