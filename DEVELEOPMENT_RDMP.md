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

1. Establish clear input parameters for the user's _clothing item image_ and _price range_

2. Convert the user's provided image into its vector representation

3. Search using the index established earlier and retrieve the metadata for the appropriate clothing items

4. Return product info to user to browse ez-pz.

### Develop a Web Application Interface:

1. Create a GUI for easy User Interaction

2. Establish an API for backend communication

3. Move current metadata and images to a database

4. Deploy the application
